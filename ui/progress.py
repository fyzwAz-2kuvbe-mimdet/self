"""10단계 Phase 인디케이터 — 클릭 가능한 단계 버튼 포함."""

import streamlit as st
from core.manual_data import PHASE_INFO, WEEK_DATA

_BTN_CSS = """
<style>
.nav-btn-row button {
    padding: 0 !important;
    min-height: 34px !important;
    height: 34px !important;
    border-radius: 50% !important;
    font-size: 13px !important;
    font-weight: 700 !important;
}
</style>
"""


def _dot_html(label: str, color: str, is_done: bool, is_current: bool) -> str:
    if is_done:
        bg = color
        border = color
        text = "white"
        content = "✓"
    elif is_current:
        bg = color
        border = color
        text = "white"
        content = label
    else:
        bg = "#f3f4f6"
        border = "#d1d5db"
        text = "#9ca3af"
        content = label

    pulse = "animation:pulse 1.5s ease-in-out infinite;" if is_current else ""
    return (
        f'<span style="display:inline-flex;align-items:center;justify-content:center;'
        f'width:32px;height:32px;border-radius:50%;background:{bg};border:2px solid {border};'
        f'color:{text};font-size:12px;font-weight:700;cursor:pointer;{pulse}">'
        f'{content}</span>'
    )


def _line_html(done: bool, color: str) -> str:
    bg = color if done else "#e5e7eb"
    return (
        f'<span style="display:inline-block;width:24px;height:2px;'
        f'background:{bg};border-radius:2px;vertical-align:middle;margin:0 2px;"></span>'
    )


def render_progress(current_step: int, completed_steps: list):
    # 시각적 인디케이터 (HTML)
    html = ['<div style="background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:14px 18px;margin-bottom:8px;">']
    for phase_num, phase in PHASE_INFO.items():
        color = phase["color"]
        html.append(
            f'<div style="font-size:11px;font-weight:700;color:{color};'
            f'margin:6px 0 4px;letter-spacing:0.3px;">Phase {phase_num} · {phase["name"]}</div>'
            f'<div style="display:flex;align-items:center;gap:2px;margin-bottom:6px;">'
        )
        weeks = phase["weeks"]
        for i, week in enumerate(weeks):
            html.append(_dot_html(str(week), color, week in completed_steps, week == current_step))
            if i < len(weeks) - 1:
                html.append(_line_html(week in completed_steps, color))
        html.append("</div>")
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)

    # 현재 단계 표시
    title = WEEK_DATA[current_step]["title"]
    st.markdown(
        f'<div style="font-size:12px;color:#9ca3af;margin-bottom:4px;">'
        f'현재 &nbsp;<strong style="color:#111827;">{current_step}주차 — {title}</strong>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # 클릭 네비게이션 버튼 (테스트/이동용)
    with st.expander("단계 이동 (테스트용)", expanded=False):
        st.caption("원하는 주차를 클릭하면 바로 이동합니다.")
        for phase_num, phase in PHASE_INFO.items():
            color = phase["color"]
            cols = st.columns(len(phase["weeks"]))
            for col, week in zip(cols, phase["weeks"]):
                with col:
                    is_current = week == current_step
                    btn_label = f"{'✓ ' if week in completed_steps else ''}{week}주차"
                    if st.button(
                        btn_label,
                        key=f"nav_{week}",
                        type="primary" if is_current else "secondary",
                        use_container_width=True,
                    ):
                        st.session_state.started = True
                        st.session_state.current_step = week
                        st.rerun()

    st.divider()
