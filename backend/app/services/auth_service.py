"""
Authentication and User Profile Service.
Handles User Registration, Login, bcrypt password hashing, JWT Token generation/verification,
and SQLite persistence for beneficiary accounts and saved schemes.
"""

import json
import os
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.user import UserSignUp, UserLogin, UserResponse, UserUpdate

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = Path(os.getenv("USERS_DB_PATH", str(BASE_DIR / "users.db")))
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "sih26092-super-secret-jwt-key-for-auth-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 Days

security = HTTPBearer(auto_error=False)


class AuthService:
    """Database and Authentication management using SQLite and JWT."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Create users table if not already existing."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL,
                    phone TEXT,
                    category TEXT DEFAULT 'General',
                    state TEXT,
                    district TEXT,
                    annual_income INTEGER,
                    saved_schemes TEXT DEFAULT '[]',
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()

    # Password Utilities
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
        except Exception:
            return False

    # JWT Utilities
    @staticmethod
    def create_access_token(user_id: int, email: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": str(user_id),
            "email": email,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired. Please login again.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    # User CRUD
    def _row_to_user_response(self, row: sqlite3.Row) -> UserResponse:
        saved = []
        try:
            saved = json.loads(row["saved_schemes"] or "[]")
        except Exception:
            saved = []

        return UserResponse(
            id=row["id"],
            full_name=row["full_name"],
            email=row["email"],
            phone=row["phone"],
            category=row["category"],
            state=row["state"],
            district=row["district"],
            annual_income=row["annual_income"],
            saved_schemes=saved,
            created_at=row["created_at"],
        )

    def signup(self, data: UserSignUp) -> Dict[str, Any]:
        """Register a new user account."""
        email_clean = data.email.strip().lower()

        # Check existing
        with self._get_connection() as conn:
            existing = conn.execute("SELECT id FROM users WHERE email = ?", (email_clean,)).fetchone()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="An account with this email address already exists.",
                )

            hashed = self.hash_password(data.password)
            now_iso = datetime.now(timezone.utc).isoformat()

            cur = conn.cursor()
            cur.execute("""
                INSERT INTO users (full_name, email, hashed_password, phone, category, state, district, annual_income, saved_schemes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, '[]', ?)
            """, (
                data.full_name.strip(),
                email_clean,
                hashed,
                data.phone.strip() if data.phone else None,
                data.category.strip() if data.category else "General",
                data.state.strip() if data.state else None,
                data.district.strip() if data.district else None,
                data.annual_income,
                now_iso,
            ))
            conn.commit()
            user_id = cur.lastrowid

            user_row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            user_resp = self._row_to_user_response(user_row)
            token = self.create_access_token(user_id=user_id, email=email_clean)

            return {
                "access_token": token,
                "token_type": "bearer",
                "user": user_resp,
            }

    def login(self, data: UserLogin) -> Dict[str, Any]:
        """Authenticate an existing user."""
        email_clean = data.email.strip().lower()

        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE email = ?", (email_clean,)).fetchone()
            if not row or not self.verify_password(data.password, row["hashed_password"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password.",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            token = self.create_access_token(user_id=row["id"], email=row["email"])
            user_resp = self._row_to_user_response(row)

            return {
                "access_token": token,
                "token_type": "bearer",
                "user": user_resp,
            }

    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            if row:
                return self._row_to_user_response(row)
        return None

    def update_profile(self, user_id: int, data: UserUpdate) -> UserResponse:
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="User not found.")

            fields = []
            values = []
            if data.full_name is not None:
                fields.append("full_name = ?")
                values.append(data.full_name.strip())
            if data.phone is not None:
                fields.append("phone = ?")
                values.append(data.phone.strip())
            if data.category is not None:
                fields.append("category = ?")
                values.append(data.category.strip())
            if data.state is not None:
                fields.append("state = ?")
                values.append(data.state.strip())
            if data.district is not None:
                fields.append("district = ?")
                values.append(data.district.strip())
            if data.annual_income is not None:
                fields.append("annual_income = ?")
                values.append(data.annual_income)

            if fields:
                values.append(user_id)
                conn.execute(f"UPDATE users SET {', '.join(fields)} WHERE id = ?", values)
                conn.commit()

            updated = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return self._row_to_user_response(updated)

    def toggle_saved_scheme(self, user_id: int, scheme_code: str, save: bool) -> List[str]:
        code = scheme_code.strip().upper()
        with self._get_connection() as conn:
            row = conn.execute("SELECT saved_schemes FROM users WHERE id = ?", (user_id,)).fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="User not found.")

            current = []
            try:
                current = json.loads(row["saved_schemes"] or "[]")
            except Exception:
                current = []

            if save and code not in current:
                current.append(code)
            elif not save and code in current:
                current.remove(code)

            conn.execute("UPDATE users SET saved_schemes = ? WHERE id = ?", (json.dumps(current), user_id))
            conn.commit()
            return current


# Global singleton
auth_service = AuthService()


def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> UserResponse:
    """Dependency to retrieve the authenticated user from the Bearer token."""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided. Include 'Authorization: Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = auth_service.decode_token(token)
    user_id = int(payload.get("sub", 0))
    user = auth_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account no longer exists.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
