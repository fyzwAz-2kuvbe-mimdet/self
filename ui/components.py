"""카드, 버튼, 스크립트 박스, AI 응답 등 공용 UI 컴포넌트."""

import streamlit as st
from core.manual_data import PHASE_INFO, WEEK_DATA


def render_week_header(step: int):
    week = WEEK_DATA[step]
    phase_num = week["phase"]
    color = PHASE_INFO[phase_num]["color"]
    phase_name = PHASE_INFO[phase_num]["name"]

    st.markdown(
        f'<div class="week-header" style="background:linear-gradient(135deg, {color}cc, {color});">'
        f'<div class="week-num">PHASE {phase_num} · {phase_name} · WEEK {step}</div>'
        f'<h2>{step}주차 — {week["title"]}</h2>'
        f'<div class="tagline">"{week["tagline"]}"</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_goals(step: int):
    week = WEEK_DATA[step]
    st.markdown("**이번 주 목표**")
    goals_html = "".join(f'<div class="goal-item">{g}</div>' for g in week["goals"])
    st.markdown(f'<div style="margin-bottom:16px;">{goals_html}</div>', unsafe_allow_html=True)


def render_script_box(text: str, who: str = "컨설턴트"):
    st.markdown(
        f'<div class="script-box">'
        f'<div class="script-who">{who}</div>'
        f'<div>{text}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_ai_response(text: str):
    st.markdown(
        f'<div class="ai-response">'
        f'<div class="ai-label">AI 코치</div>'
        f'<div>{text}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_tip_box(text: str, title: str = ""):
    title_html = f'<strong>{title}</strong><br>' if title else ""
    st.markdown(
        f'<div class="tip-box">{title_html}{text}</div>',
        unsafe_allow_html=True,
    )


def render_homework(step: int):
    week = WEEK_DATA[step]
    st.markdown(
        f'<div class="card" style="border-left:4px solid #10b981;">'
        f'<strong>이번 주 과제</strong><br><br>'
        f'{week["homework"]}'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_api_key_warning():
    st.markdown(
        '<div class="api-warning">'
        '<h3>API 키 설정이 필요합니다</h3>'
        '<ol>'
        '<li><a href="https://aistudio.google.com" target="_blank">https://aistudio.google.com</a>에서 Gemini API 키를 발급받으세요.</li>'
        '<li>Streamlit Cloud의 앱 → ⋯ → Settings → <strong>Secrets</strong>로 이동.</li>'
        '<li><code>GEMINI_API_KEY = "발급받은_키"</code> 한 줄을 추가하고 저장.</li>'
        '<li>앱을 새로고침하세요.</li>'
        '</ol>'
        '<p style="color:#533f03; margin-top:12px; font-size:13px;">'
        '로컬 개발 시: <code>.streamlit/secrets.toml</code> 파일에 위 내용을 저장하세요.'
        '</p>'
        '</div>',
        unsafe_allow_html=True,
    )
