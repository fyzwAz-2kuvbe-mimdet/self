"""10단계 Phase 인디케이터 — st.button 기반 클릭 네비게이션."""

import streamlit as st
from core.manual_data import PHASE_INFO, WEEK_DATA

_CSS = """
<style>
@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50%       { transform: scale(1.12); opacity: 0.82; }
}
.progress-nav-marker + div[data-testid="stHorizontalBlock"]
  div[data-testid="stButton"] button {
    border-radius: 50% !important;
    width: 36px !important;
    height: 36px !important;
    min-height: 36px !important;
    padding: 0 !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    line-height: 1 !important;
}
</style>
"""


def render_progress(current_step: int, completed_steps: list):
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── 시각적 인디케이터 (HTML, 장식용) ──────────────────────
    rows = []
    for phase_num, phase in PHASE_INFO.items():
        color = phase["color"]
        dots = []
        for i, week in enumerate(phase["weeks"]):
            is_done    = week in completed_steps
            is_current = week == current_step
            if is_done:
                bg, border, fg, lbl = color, color, "white", "✓"
            elif is_current:
                bg, border, fg, lbl = color, color, "white", str(week)
                pass
            else:
                bg, border, fg, lbl = "#f3f4f6", "#d1d5db", "#9ca3af", str(week)
            pulse = "animation:pulse 1.5s ease-in-out infinite;" if is_current else ""
            dots.append(
                f'<span style="display:inline-flex;align-items:center;justify-content:center;'
                f'width:32px;height:32px;border-radius:50%;background:{bg};'
                f'border:2px solid {border};color:{fg};font-size:12px;font-weight:700;{pulse}">'
                f'{lbl}</span>'
            )
            if i < len(phase["weeks"]) - 1:
                lc = color if week in completed_steps else "#e5e7eb"
                dots.append(
                    f'<span style="display:inline-block;width:22px;height:2px;'
                    f'background:{lc};border-radius:2px;vertical-align:middle;margin:0 2px;"></span>'
                )
        rows.append(
            f'<div style="display:flex;align-items:center;gap:4px;margin:4px 0;">'
            f'<span style="font-size:11px;font-weight:700;color:{color};min-width:148px;">'
            f'Phase {phase_num} · {phase["name"]}</span>'
            + "".join(dots) + "</div>"
        )

    title = WEEK_DATA[current_step]["title"]
    st.markdown(
        '<div style="background:#fff;border:1px solid #e5e7eb;border-radius:12px;'
        'padding:12px 18px 8px;margin-bottom:8px;">'
        + "".join(rows)
        + f'<div style="font-size:12px;color:#9ca3af;margin-top:6px;">'
          f'현재 <strong style="color:#111827;">{current_step}주차 — {title}</strong>'
          f'</div></div>',
        unsafe_allow_html=True,
    )

    # ── 클릭 가능한 버튼 행 ───────────────────────────────────
    # CSS 타깃을 위한 마커 div (adjacent sibling selector 용)
    st.markdown('<div class="progress-nav-marker"></div>', unsafe_allow_html=True)

    cols = st.columns(10)
    for week, col in enumerate(cols, start=1):
        phase     = WEEK_DATA[week]["phase"]
        color     = PHASE_INFO[phase]["color"]
        is_done   = week in completed_steps
        is_current = week == current_step
        label     = "✓" if is_done else str(week)

        # 버튼 색상을 개별 CSS로 덮어쓰기
        if is_done or is_current:
            btn_style = (
                f'<style>'
                f'div[data-testid="stHorizontalBlock"] '
                f'div[data-testid="stColumn"]:nth-child({week}) button {{'
                f'background:{color} !important;'
                f'border-color:{color} !important;'
                f'color:white !important;'
                f'}}</style>'
            )
            st.markdown(btn_style, unsafe_allow_html=True)

        with col:
            if st.button(label, key=f"nav_w{week}",
                         help=f"{week}주차 — {WEEK_DATA[week]['title']}"):
                st.session_state.started      = True
                st.session_state.current_step = week
                st.rerun()

    st.divider()
