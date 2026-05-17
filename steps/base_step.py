"""공통 세션 렌더러 — 질문 한 개씩 순차 표시, 완료 버튼으로 다음 질문 진행."""

import streamlit as st
from core.manual_data import WEEK_DATA, PHASE_INFO
from core.state import save_answer, save_ai_response, mark_step_complete, go_to_step
from core.llm import call_gemini
from core.prompts import build_prompt, build_summary_prompt
from ui.components import render_week_header, render_goals, render_script_box, render_homework

_STEP_CSS = """
<style>
/* 질문 카드 진입 애니메이션 */
@keyframes slideUp {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}
.question-card {
  animation: slideUp 0.35s ease both;
  background: #fff;
  border: 1.5px solid #e5e7eb;
  border-radius: 14px;
  padding: 24px 26px 20px;
  margin: 16px 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.q-index {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 8px;
}
.q-label {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  line-height: 1.55;
  margin-bottom: 16px;
  white-space: pre-wrap;
}
/* textarea 흰 배경 강제 */
.question-card textarea,
section[data-testid="stMain"] textarea {
  background: #ffffff !important;
  color: #111827 !important;
  border: 1.5px solid #d1d5db !important;
  border-radius: 8px !important;
  font-size: 15px !important;
  line-height: 1.6 !important;
  padding: 10px 14px !important;
}
section[data-testid="stMain"] textarea:focus {
  border-color: #3b82f6 !important;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
  outline: none !important;
}
/* AI 응답 버블 */
.ai-bubble {
  animation: slideUp 0.3s ease both;
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 10px;
  padding: 12px 16px;
  margin-top: 10px;
  font-size: 14px;
  color: #0c4a6e;
  line-height: 1.6;
}
.ai-bubble-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.8px;
  color: #0284c7;
  margin-bottom: 5px;
  text-transform: uppercase;
}
/* 완료된 질문 미리보기 */
.done-q {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 12px 16px;
  margin: 6px 0;
  opacity: 0.8;
}
.done-q-label {
  font-size: 11px;
  color: #6b7280;
  margin-bottom: 3px;
}
.done-q-answer {
  font-size: 14px;
  color: #374151;
  white-space: pre-wrap;
}
/* 단계 완료 카드 */
.finish-card {
  background: linear-gradient(135deg,#f0fdf4,#dcfce7);
  border: 1.5px solid #86efac;
  border-radius: 14px;
  padding: 24px;
  text-align: center;
  margin-top: 20px;
  animation: slideUp 0.35s ease both;
}
</style>
"""


def _phase_color(step: int) -> str:
    phase = WEEK_DATA[step]["phase"]
    return PHASE_INFO[phase]["color"]


def render_step(step: int):
    st.markdown(_STEP_CSS, unsafe_allow_html=True)

    week      = WEEK_DATA[step]
    questions = week["questions"]
    answers   = st.session_state.step_answers[step]
    color     = _phase_color(step)

    # 현재 진행 중인 질문 인덱스
    q_idx_key = f"q_idx_{step}"
    if q_idx_key not in st.session_state:
        st.session_state[q_idx_key] = 0
    cur_idx = st.session_state[q_idx_key]

    render_week_header(step)
    render_goals(step)
    st.markdown("<div style='margin:8px 0;'></div>", unsafe_allow_html=True)
    render_script_box(week["intro_script"])
    st.markdown("<div style='margin:12px 0;'></div>", unsafe_allow_html=True)

    # ── 완료된 질문 미리보기 ──────────────────────────────────
    for i in range(cur_idx):
        q   = questions[i]
        ans = answers.get(q["id"], "")
        st.markdown(
            f'<div class="done-q">'
            f'<div class="done-q-label">Q{i+1}. {q["label"][:60]}{"…" if len(q["label"])>60 else ""}</div>'
            f'<div class="done-q-answer">{ans[:120]}{"…" if len(ans)>120 else ""}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── 현재 질문 카드 ────────────────────────────────────────
    if cur_idx < len(questions):
        q   = questions[cur_idx]
        qid = q["id"]

        st.markdown(
            f'<div class="question-card">'
            f'<div class="q-index" style="color:{color};">질문 {cur_idx+1} / {len(questions)}</div>'
            f'<div class="q-label">{q["label"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        saved = answers.get(qid, "")
        user_input = st.text_area(
            label="답변",
            value=saved,
            placeholder=q.get("placeholder", "여기에 적어줘..."),
            height=160,
            key=f"ta_{step}_{qid}",
            label_visibility="collapsed",
        )

        if user_input.strip():
            save_answer(step, qid, user_input)

        # AI 질문 받기 + 다음 버튼
        col_ai, col_next = st.columns([1, 1])

        with col_ai:
            if st.button("💬 AI 질문 받기", key=f"ai_{step}_{qid}",
                         use_container_width=True):
                if user_input.strip():
                    with st.spinner("생각 중..."):
                        prompt = build_prompt(step, qid, user_input)
                        resp   = call_gemini(prompt)
                        st.session_state[f"air_{step}_{qid}"] = resp
                else:
                    st.warning("먼저 답변을 입력해줘.")

        with col_next:
            is_last = (cur_idx == len(questions) - 1)
            next_label = "✅ 모든 질문 완료" if is_last else "다음 질문 →"
            if st.button(next_label, key=f"next_{step}_{qid}",
                         type="primary", use_container_width=True):
                if user_input.strip():
                    save_answer(step, qid, user_input)
                    st.session_state[q_idx_key] = cur_idx + 1
                    st.rerun()
                else:
                    st.warning("답변을 입력한 후 넘어갈 수 있어.")

        # AI 응답 표시
        ai_resp = st.session_state.get(f"air_{step}_{qid}", "")
        if ai_resp:
            st.markdown(
                f'<div class="ai-bubble">'
                f'<div class="ai-bubble-label">AI 코치</div>'
                f'{ai_resp}</div>',
                unsafe_allow_html=True,
            )

    # ── 모든 질문 완료 → 단계 마무리 화면 ───────────────────
    else:
        st.markdown(
            f'<div class="finish-card">'
            f'<div style="font-size:32px;margin-bottom:8px;">🎉</div>'
            f'<div style="font-size:18px;font-weight:700;color:#166534;margin-bottom:6px;">'
            f'{step}주차 질문을 모두 마쳤어!</div>'
            f'<div style="font-size:14px;color:#15803d;">아래 과제를 확인하고 다음 단계로 넘어가자.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        render_homework(step)

        st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns([1, 1, 1])

        with col_a:
            if st.button("↩ 답변 다시 보기", key=f"review_{step}",
                         use_container_width=True):
                st.session_state[q_idx_key] = 0
                st.rerun()

        with col_b:
            if step > 1:
                if st.button("← 이전 주차", key=f"back_{step}",
                             use_container_width=True):
                    go_to_step(step - 1)
                    st.rerun()

        with col_c:
            finish_label = "10주 완료! 🎊" if step == 10 else f"{step + 1}주차로 →"
            if st.button(finish_label, key=f"finish_{step}",
                         type="primary", use_container_width=True):
                with st.spinner("세션 정리 중..."):
                    summary = call_gemini(build_summary_prompt(step, answers))
                    st.session_state[f"session_summary_{step}"] = summary
                mark_step_complete(step)
                if step < 10:
                    st.session_state[f"q_idx_{step + 1}"] = 0
                    go_to_step(step + 1)
                else:
                    st.session_state.current_step = 10
                st.rerun()
