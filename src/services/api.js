const API_BASE_URL = "http://localhost:8000";

export const matchSchemes = async (userData) => {
  const response = await fetch(`${API_BASE_URL}/match`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }

  return await response.json();
};


/* ================= AI CHAT ================= */

export const sendChatMessage = async (message) => {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: message,
    }),
  });

  if (!response.ok) {
    throw new Error(`Chat API Error: ${response.status}`);
  }

  return await response.json();
};

export const getNearbyBanks = async (schemeCode, state, district) => {
  const params = new URLSearchParams({
    scheme_code: schemeCode,
    state: state,
  });

  if (district) {
    params.append("district", district);
  }

  const response = await fetch(
    `${API_BASE_URL}/banks/nearby?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error(`Bank API Error: ${response.status}`);
  }

  return await response.json();
};