"""Google Gemini 2.5 Flash Lite 호출 래퍼 — 재시도/타임아웃/에러 처리 포함."""

import time
import streamlit as st

FALLBACK_MSG = "지금은 AI가 응답할 수 없어. 다음 질문으로 넘어가도 괜찮아."
MODEL_NAME = "gemini-2.5-flash-lite-preview-06-17"
TIMEOUT_SECONDS = 30
MAX_OUTPUT_TOKENS = 200


def _get_client():
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    try:
        from google import genai
        return genai.Client(api_key=api_key)
    except Exception:
        return None


def call_gemini(prompt: str) -> str:
    client = _get_client()
    if client is None:
        return FALLBACK_MSG

    from google.genai import types

    config = types.GenerateContentConfig(
        max_output_tokens=MAX_OUTPUT_TOKENS,
        temperature=0.7,
    )

    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=config,
            )
            return response.text.strip()
        except Exception as e:
            if attempt == 0:
                time.sleep(2)
            else:
                return FALLBACK_MSG
    return FALLBACK_MSG


def check_api_key() -> bool:
    return bool(st.secrets.get("GEMINI_API_KEY", ""))
