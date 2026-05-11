"""10단계 Phase 인디케이터 — 상단 고정, Phase 단위 그룹화."""

import streamlit as st
from core.manual_data import PHASE_INFO, WEEK_DATA


def render_progress(current_step: int, completed_steps: list):
    html_parts = ['<div class="progress-container">']

    for phase_num, phase in PHASE_INFO.items():
        color = phase["color"]
        phase_name = phase["name"]
        weeks = phase["weeks"]

        html_parts.append(
            f'<div class="phase-row">'
            f'<span class="phase-label" style="color:{color}; font-weight:700;">'
            f'Phase {phase_num} · {phase_name}</span>'
        )

        for i, week in enumerate(weeks):
            if week in completed_steps:
                dot_class = "step-dot done"
                label = "✓"
            elif week == current_step:
                dot_class = f"step-dot current"
                label = str(week)
                style = f'style="background:{color}; border-color:{color};"'
            else:
                dot_class = "step-dot"
                label = str(week)
                style = ""

            if week in completed_steps:
                html_parts.append(f'<span class="{dot_class}">{label}</span>')
            elif week == current_step:
                html_parts.append(f'<span class="{dot_class}" {style}>{label}</span>')
            else:
                html_parts.append(f'<span class="{dot_class}">{label}</span>')

            if i < len(weeks) - 1:
                connector_class = "step-connector done" if week in completed_steps else "step-connector"
                html_parts.append(f'<span class="{connector_class}"></span>')

        html_parts.append('</div>')

    html_parts.append('</div>')
    st.markdown("\n".join(html_parts), unsafe_allow_html=True)
