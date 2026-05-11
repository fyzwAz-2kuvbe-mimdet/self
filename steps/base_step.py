"""공통 세션 렌더러 — 모든 주차가 이 함수를 사용한다."""

import streamlit as st
from core.manual_data import WEEK_DATA
from core.state import save_answer, save_ai_response, mark_step_complete, go_to_step
from core.llm import call_gemini
from core.prompts import build_prompt, build_summary_prompt
from ui.components import (
    render_week_header,
    render_goals,
    render_script_box,
    render_ai_response,
    render_homework,
    render_tip_box,
)


def render_step(step: int):
    week = WEEK_DATA[step]
    answers = st.session_state.step_answers[step]
    ai_responses = st.session_state.step_ai_responses[step]

    render_week_header(step)
    render_goals(step)

    st.divider()

    render_script_box(week["intro_script"])

    st.markdown("### 오늘 세션 질문")

    all_answered = True
    for i, q in enumerate(week["questions"]):
        qid = q["id"]
        st.markdown(f"**{i + 1}. {q['label']}**")

        saved_val = answers.get(qid, "")
        user_input = st.text_area(
            label=f"답변 {i + 1}",
            value=saved_val,
            placeholder=q.get("placeholder", "여기에 적어줘..."),
            height=150,
            key=f"step{step}_q{qid}",
            label_visibility="collapsed",
        )

        if user_input.strip():
            save_answer(step, qid, user_input)
        else:
            all_answered = False

        if user_input.strip():
            col1, col2 = st.columns([1, 5])
            with col1:
                ask_btn = st.button(
                    "AI 질문 받기",
                    key=f"ask_{step}_{qid}",
                    use_container_width=True,
                )
            if ask_btn:
                with st.spinner("생각 중..."):
                    prompt = build_prompt(step, qid, user_input)
                    resp = call_gemini(prompt)
                    save_ai_response(step, resp)
                    st.session_state[f"last_ai_{step}_{qid}"] = resp

            last_resp = st.session_state.get(f"last_ai_{step}_{qid}", "")
            if last_resp:
                render_ai_response(last_resp)

        st.markdown("")

    st.divider()
    render_homework(step)

    st.markdown("### 이번 주 마치기")
    col_a, col_b = st.columns(2)

    with col_a:
        finish_btn = st.button(
            f"{'이번 단계 완료 →' if step < 10 else '10주 완료!'}",
            key=f"finish_{step}",
            type="primary",
            use_container_width=True,
        )

    with col_b:
        if step > 1:
            back_btn = st.button(
                "← 이전 주차",
                key=f"back_{step}",
                use_container_width=True,
            )
            if back_btn:
                go_to_step(step - 1)
                st.rerun()

    if finish_btn:
        with st.spinner("세션 정리 중..."):
            summary_prompt = build_summary_prompt(step, answers)
            summary = call_gemini(summary_prompt)
            st.session_state[f"session_summary_{step}"] = summary

        mark_step_complete(step)
        if step < 10:
            go_to_step(step + 1)
        else:
            st.session_state.current_step = 10
        st.rerun()

    summary = st.session_state.get(f"session_summary_{step}", "")
    if summary and step in st.session_state.completed_steps:
        render_tip_box(summary, "세션 요약 (컨설턴트용)")
