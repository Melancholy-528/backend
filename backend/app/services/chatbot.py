"""
AI Scheme Advisory Chatbot Service powered by Ollama and RAG.
Answers applicant questions about government schemes, eligibility rules,
benefits, and application guidelines using indexed scheme database and document texts.
"""

import re
from typing import List, Dict, Any, Optional, Iterator, Tuple
from pydantic import BaseModel, Field

from app.schemas.scheme import Scheme
from app.services.ollama_service import ollama_service
from app.services.bank_locator import bank_locator, BankRecommendation


class ChatMessage(BaseModel):
    role: str  # "user", "assistant", or "system"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = Field(default_factory=list)
    scheme_code: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    stream: bool = False


class ChatResponse(BaseModel):
    reply: str
    referenced_schemes: List[Dict[str, Any]] = Field(default_factory=list)
    suggested_followups: List[str] = Field(default_factory=list)
    nearby_banking_support: Optional[BankRecommendation] = None
    model_used: str


SYSTEM_PROMPT = """You are the official AI Scheme Advisory Assistant for the SIH26092 platform (Ministry of Social Justice & Empowerment and MSME).
Answer the user's questions clearly, accurately, and concisely using the verified Scheme Context below.
Highlight loan amounts (in ₹ Lakhs/Crores), capital subsidies (%), margin money, and eligibility criteria in bullet points.
If local lending banks or Lead District Banks are provided in the Context for the applicant's location, explicitly name them and guide the applicant on how to approach the branch.
"""


class SchemeChatbot:
    def __init__(self):
        pass

    def retrieve_relevant_context(
        self,
        query: str,
        schemes: List[Scheme],
        documents: List[dict],
        specific_scheme_code: Optional[str] = None,
        max_schemes: int = 2,
    ) -> Tuple[List[Scheme], str]:
        """
        Retrieve concise relevant scheme context to keep prompt evaluation fast and fit in local LLM memory.
        """
        matched_schemes: List[Scheme] = []

        # 1. If user targeted a specific scheme
        if specific_scheme_code:
            target = specific_scheme_code.strip().lower()
            for s in schemes:
                if (s.scheme_code and s.scheme_code.lower() == target) or s.name.lower() == target:
                    matched_schemes.append(s)
                    break

        # 2. Keyword & semantic matching across query
        if not matched_schemes:
            query_lower = query.lower()
            scored: List[Tuple[int, Scheme]] = []
            
            keywords = {
                "sc": ["sc", "scheduled caste"],
                "st": ["st", "scheduled tribe", "tribal"],
                "obc": ["obc", "backward class"],
                "women": ["women", "woman", "female", "mahila"],
                "artisan": ["artisan", "vishwakarma", "craft", "tailor", "tailoring", "garment", "carpenter", "blacksmith", "potter"],
                "vendor": ["vendor", "street vendor", "hawker", "thela", "svanidhi"],
                "safai": ["safai", "sanitation", "cleaner", "sewer"],
                "msme": ["msme", "pmegp", "business", "enterprise", "factory", "shop", "start", "manufacturing", "textile"],
                "mudra": ["mudra", "shishu", "kishore", "tarun"],
                "subsidy": ["subsidy", "margin money", "grant"],
                "general": ["general", "open", "all"],
                "minority": ["minority", "muslim", "christian", "sikh", "parsi", "buddhist"],
                "pwd": ["pwd", "disabled", "divyang", "handicapped"]
            }

            for s in schemes:
                score = 0
                s_name = s.name.lower()
                s_code = (s.scheme_code or "").lower()
                s_desc = (s.description or "").lower()
                s_cats = [c.lower() for c in s.eligible_categories]

                if s_code and s_code in query_lower:
                    score += 50
                if any(part in query_lower for part in s_name.split() if len(part) > 3):
                    score += 30

                for topic, kws in keywords.items():
                    if any(kw in query_lower for kw in kws):
                        if any(topic in cat for cat in s_cats) or topic in s_desc or topic in s_name:
                            score += 25

                for word in query_lower.split():
                    if len(word) > 3:
                        if word in s_name:
                            score += 15
                        if word in s_desc:
                            score += 5

                if score > 0:
                    scored.append((score, s))

            scored.sort(key=lambda x: x[0], reverse=True)
            matched_schemes = [item[1] for item in scored[:max_schemes]]

        # Fallback to top schemes if no match
        if not matched_schemes and schemes:
            matched_schemes = schemes[:2]

        # 3. Build concise, token-efficient context
        context_parts = []
        for s in matched_schemes:
            cats = ", ".join(s.eligible_categories) if s.eligible_categories else "All"
            part = [
                f"### Scheme: {s.name} ({s.scheme_code or 'N/A'})",
                f"- Eligible Categories: {cats}",
            ]
            if s.max_project_cost:
                part.append(f"- Max Loan / Project Limit: ₹{s.max_project_cost:,}")
            if s.subsidy_percentage:
                part.append(f"- Subsidy / Margin Money: {s.subsidy_percentage}%")
            if s.income_limit:
                part.append(f"- Income Limit: ₹{s.income_limit:,}")
            if s.min_age or s.max_age:
                part.append(f"- Age Requirement: {s.min_age or '18'} to {s.max_age or 'No upper limit'} years")
            if s.benefits:
                part.append(f"- Key Benefits: {'; '.join(s.benefits[:2])}")
            if s.source_url:
                part.append(f"- Portal: {s.source_url}")

            context_parts.append("\n".join(part))

        context_string = "\n\n".join(context_parts)
        return matched_schemes, context_string

    def generate_followups(self, query: str, matched_schemes: List[Scheme]) -> List[str]:
        """Generate smart context-aware follow-up question suggestions."""
        if not matched_schemes:
            return [
                "What schemes are available for SC/ST women entrepreneurs?",
                "How can I apply for a collateral-free loan under PMEGP?",
                "What is the maximum loan limit in PM Vishwakarma?",
            ]

        first = matched_schemes[0]
        name = first.name
        code = first.scheme_code or name
        return [
            f"What documents are required to apply for {code}?",
            f"What is the exact subsidy and margin money under {name}?",
            f"Can I apply if my annual family income is above ₹3 Lakhs?",
        ]

    def build_chat_messages(
        self,
        user_message: str,
        context_string: str,
        history: List[ChatMessage],
    ) -> List[Dict[str, str]]:
        """Construct the prompt message array for Ollama, keeping tokens dense."""
        system_content = f"{SYSTEM_PROMPT}\n\nScheme Context:\n{context_string}"
        messages = [{"role": "system", "content": system_content}]

        # Keep last 2 turns of conversation history
        for msg in history[-2:]:
            if msg.role in ["user", "assistant"]:
                cleaned_history = msg.content[:300] + ("..." if len(msg.content) > 300 else "")
                messages.append({"role": msg.role, "content": cleaned_history})

        # Sanitize user prompt to prevent excessive token eval delays on CPU
        cleaned_prompt = user_message.strip()
        if len(cleaned_prompt) > 1200:
            cleaned_prompt = cleaned_prompt[:1200] + "\n...(summary requested)"

        messages.append({"role": "user", "content": cleaned_prompt})
        return messages

    def answer(
        self,
        request: ChatRequest,
        schemes: List[Scheme],
        documents: List[dict],
    ) -> ChatResponse:
        """Generate complete answer to user query with zero-failure guarantee."""
        matched, context_str = self.retrieve_relevant_context(
            query=request.message,
            schemes=schemes,
            documents=documents,
            specific_scheme_code=request.scheme_code,
        )

        # Detect State and District from request or query message
        user_state = request.state
        user_dist = request.district
        if not user_state or not user_dist:
            extracted_loc = bank_locator.extract_location_from_text(request.message)
            user_state = user_state or extracted_loc.get("state")
            user_dist = user_dist or extracted_loc.get("district")

        bank_rec: Optional[BankRecommendation] = None
        if matched and user_state:
            top = matched[0]
            bank_rec = bank_locator.recommend_banks(
                scheme_code=top.scheme_code or "SCHEME",
                scheme_name=top.name,
                state=user_state,
                district=user_dist,
            )
            rrb_names = ", ".join(r["bank_name"] for r in bank_rec.regional_rural_banks) or "Regional Rural Bank"
            banking_context = (
                f"\n\nDesignated Lending Banks in {bank_rec.district}, {bank_rec.state} for {top.name}:\n"
                f"- Designated Lead Bank: {bank_rec.lead_bank_name} (Priority Sector Lending Desk)\n"
                f"- Regional Rural Bank: {rrb_names}\n"
                f"- Lead District Manager: {bank_rec.ldm_office_info}\n"
                f"- Nodal Office: {bank_rec.district_nodal_offices[0].agency} ({bank_rec.district_nodal_offices[0].location})\n"
                f"- Application Step: {bank_rec.application_steps[0]}"
            )
            context_str += banking_context

        followups = self.generate_followups(request.message, matched)
        if bank_rec:
            followups.insert(0, f"Which branch of {bank_rec.lead_bank_name} in {bank_rec.district} handles this loan?")
            followups.append(f"Where is the District Industries Centre (DIC) in {bank_rec.district}?")

        model_name = ollama_service.get_best_model()
        reply: Optional[str] = None
        used_model_label = "rule-based-fallback"

        # Check if Ollama is accessible
        if ollama_service.is_available():
            messages = self.build_chat_messages(request.message, context_str, request.history)
            try:
                reply = ollama_service.chat(messages, model=model_name)
                if reply and len(reply.strip()) >= 15:
                    used_model_label = model_name
                else:
                    reply = None
            except Exception as e:
                print(f"Ollama execution exception: {e}")
                reply = None

        # Seamless fallback if Ollama timed out or failed on a long prompt
        if not reply:
            reply = self._rule_based_fallback(request.message, matched, bank_rec=bank_rec)

        referenced_info = [
            {
                "name": s.name,
                "scheme_code": s.scheme_code,
                "ministry": s.ministry,
                "max_project_cost": s.max_project_cost,
                "subsidy_percentage": s.subsidy_percentage,
                "source_url": s.source_url,
            }
            for s in matched
        ]

        return ChatResponse(
            reply=reply,
            referenced_schemes=referenced_info,
            suggested_followups=followups,
            nearby_banking_support=bank_rec,
            model_used=used_model_label,
        )

    def stream_answer(
        self,
        request: ChatRequest,
        schemes: List[Scheme],
        documents: List[dict],
    ) -> Iterator[str]:
        """Stream answer token by token using Ollama with automatic fallback."""
        matched, context_str = self.retrieve_relevant_context(
            query=request.message,
            schemes=schemes,
            documents=documents,
            specific_scheme_code=request.scheme_code,
        )

        user_state = request.state
        user_dist = request.district
        if not user_state or not user_dist:
            extracted_loc = bank_locator.extract_location_from_text(request.message)
            user_state = user_state or extracted_loc.get("state")
            user_dist = user_dist or extracted_loc.get("district")

        bank_rec: Optional[BankRecommendation] = None
        if matched and user_state:
            top = matched[0]
            bank_rec = bank_locator.recommend_banks(
                scheme_code=top.scheme_code or "SCHEME",
                scheme_name=top.name,
                state=user_state,
                district=user_dist,
            )
            rrb_names = ", ".join(r["bank_name"] for r in bank_rec.regional_rural_banks) or "Regional Rural Bank"
            banking_context = (
                f"\n\nDesignated Lending Banks in {bank_rec.district}, {bank_rec.state} for {top.name}:\n"
                f"- Designated Lead Bank: {bank_rec.lead_bank_name}\n"
                f"- Regional Rural Bank: {rrb_names}\n"
                f"- Lead District Manager: {bank_rec.ldm_office_info}\n"
                f"- Nodal Office: {bank_rec.district_nodal_offices[0].agency} ({bank_rec.district_nodal_offices[0].location})\n"
                f"- Application Step: {bank_rec.application_steps[0]}"
            )
            context_str += banking_context

        if ollama_service.is_available():
            messages = self.build_chat_messages(request.message, context_str, request.history)
            emitted_any = False
            for chunk in ollama_service.stream_chat(messages):
                if chunk and not chunk.startswith("\n[Error") and not chunk.startswith("\n[Stream Error"):
                    emitted_any = True
                    yield chunk
            if not emitted_any:
                fallback = self._rule_based_fallback(request.message, matched, bank_rec=bank_rec)
                yield fallback
        else:
            fallback = self._rule_based_fallback(request.message, matched, bank_rec=bank_rec)
            yield fallback

    def _rule_based_fallback(
        self,
        query: str,
        matched_schemes: List[Scheme],
        bank_rec: Optional[BankRecommendation] = None,
    ) -> str:
        """Structured informative fallback when Ollama is unavailable."""
        if not matched_schemes:
            return (
                "I couldn't find specific schemes matching your query in the database. "
                "You can browse all available schemes using `/schemes` or match your profile with `/match`."
            )

        lines = [
            "Here is the verified guidance based on official government scheme criteria:\n"
        ]
        for s in matched_schemes:
            lines.append(f"### **{s.name}** (`{s.scheme_code or 'N/A'}`)")
            if s.ministry:
                lines.append(f"- **Ministry**: {s.ministry}")
            if s.eligible_categories:
                lines.append(f"- **Eligible Target Group**: {', '.join(s.eligible_categories)}")
            if s.max_project_cost:
                lines.append(f"- **Maximum Project / Loan Limit**: ₹{s.max_project_cost:,}")
            if s.subsidy_percentage:
                lines.append(f"- **Subsidy / Margin Money**: {s.subsidy_percentage}%")
            if s.income_limit:
                lines.append(f"- **Annual Income Ceiling**: ₹{s.income_limit:,}")
            if s.min_age or s.max_age:
                lines.append(f"- **Age Criteria**: {s.min_age or '18'} to {s.max_age or 'No upper limit'} years")
            if s.benefits:
                lines.append("- **Key Benefits**:")
                for b in s.benefits[:3]:
                    lines.append(f"  * {b}")
            if s.source_url:
                lines.append(f"- **Official Portal**: [{s.source_url}]({s.source_url})")
            lines.append("")

        if bank_rec:
            lines.append(f"### 🏦 **Designated Lending Banks & Nodal Support in {bank_rec.district}, {bank_rec.state}**")
            lines.append(f"- **Lead District Bank**: **{bank_rec.lead_bank_name}** ({bank_rec.primary_lending_banks[0]['branch_desk']})")
            if bank_rec.regional_rural_banks:
                lines.append(f"- **Regional Rural Bank (RRB)**: {', '.join(r['bank_name'] for r in bank_rec.regional_rural_banks)}")
            lines.append(f"- **District Nodal Agency**: **{bank_rec.district_nodal_offices[0].agency}** ({bank_rec.district_nodal_offices[0].location})")
            lines.append(f"- **Lead District Manager (LDM) Office**: {bank_rec.ldm_office_info}")
            lines.append("\n**Action Plan to Secure Your Loan**:")
            for step in bank_rec.application_steps[:3]:
                lines.append(f"- {step}")
            lines.append("")

        return "\n".join(lines)


# Singleton chatbot instance
chatbot = SchemeChatbot()
