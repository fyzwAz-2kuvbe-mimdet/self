"""진입점 — 라우터, Phase 인디케이터, API 키 확인."""

import json
import streamlit as st

from core.state import init_state, get_all_data
from core.llm import check_api_key
from ui.styles import inject_css
from ui.progress import render_progress
from ui.components import render_api_key_warning

st.set_page_config(
    page_title="10주 자기주도 문제해결 컨설팅",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_css()
init_state()


STEP_MODULES = {
    1: "steps.step01_week1",
    2: "steps.step02_week2",
    3: "steps.step03_week3",
    4: "steps.step04_week4",
    5: "steps.step05_week5",
    6: "steps.step06_week6",
    7: "steps.step07_week7",
    8: "steps.step08_week8",
    9: "steps.step09_week9",
    10: "steps.step10_week10",
}


def render_landing():
    st.markdown(
        '<div style="text-align:center; padding:40px 0 24px;">'
        '<h1 style="font-size:28px; font-weight:700; color:#111827;">10주 자기주도 문제해결 컨설팅</h1>'
        '<p style="color:#6b7280; font-size:15px; max-width:520px; margin:0 auto 24px;">'
        '스스로 문제를 정의하고 해결책을 결정해보는<br>10주 과정에 오신 걸 환영해요.'
        '</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("1주차 시작하기 →", type="primary", use_container_width=True):
            st.session_state.started = True
            st.rerun()

    st.markdown(
        '<div class="tip-box" style="margin-top:32px; text-align:center;">'
        '<strong>이 프로그램에서 AI는</strong><br>'
        '답을 가르치지 않아요. 결정을 빼앗지 않아요.<br>'
        '네가 스스로 생각할 수 있도록 질문만 던져요.'
        '</div>',
        unsafe_allow_html=True,
    )


def render_completion():
    st.markdown(
        '<div class="completion-card">'
        '<div style="font-size:48px; margin-bottom:12px;"></div>'
        '<h1>10주 완료!</h1>'
        '<p style="font-size:16px; opacity:0.9;">컨설턴트 없이 혼자 가는 한 달이 시작됩니다.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### 결정노트 전체 기록 다운로드")
    data = get_all_data()
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    st.download_button(
        label="JSON으로 내보내기",
        data=json_str.encode("utf-8"),
        file_name="self_directed_consulting_record.json",
        mime="application/json",
    )

    st.markdown("---")
    if st.button("처음부터 다시 시작", use_container_width=False):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


def main():
    if not check_api_key():
        render_api_key_warning()
        st.markdown("---")
        st.info("API 키 없이도 화면을 탐색할 수 있습니다. AI 응답만 작동하지 않습니다.")

    current = st.session_state.current_step
    completed = st.session_state.completed_steps

    is_landing = not st.session_state.started

    if is_landing:
        render_landing()
        return

    render_progress(current, completed)

    if current == 10 and 10 in completed:
        render_completion()
        return

    import importlib
    module = importlib.import_module(STEP_MODULES[current])
    module.render()


if __name__ == "__main__":
    main()
