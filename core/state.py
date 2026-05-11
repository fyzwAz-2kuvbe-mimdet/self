"""session_state 초기화 및 스키마 정의."""

import streamlit as st


def init_state():
    defaults = {
        "current_step": 1,
        "started": False,
        "completed_steps": [],
        "step_answers": {i: {} for i in range(1, 11)},
        "step_ai_responses": {i: [] for i in range(1, 11)},
        "step_question_index": {i: 0 for i in range(1, 11)},
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def mark_step_complete(step: int):
    if step not in st.session_state.completed_steps:
        st.session_state.completed_steps.append(step)


def save_answer(step: int, question_id: str, answer: str):
    st.session_state.step_answers[step][question_id] = answer


def save_ai_response(step: int, response: str):
    st.session_state.step_ai_responses[step].append(response)


def go_to_step(step: int):
    st.session_state.current_step = step


def get_all_data() -> dict:
    return {
        "completed_steps": st.session_state.completed_steps,
        "answers": st.session_state.step_answers,
        "ai_responses": st.session_state.step_ai_responses,
    }
