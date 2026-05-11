"""Streamlit 기본 디자인 제거 및 커스텀 CSS 주입."""

import streamlit as st

CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css" rel="stylesheet">

<style>
:root {
  --bg: #fafafa;
  --card: #ffffff;
  --border: #e5e7eb;
  --text: #111827;
  --text-sub: #6b7280;
  --accent: #3b82f6;
  --success: #10b981;
  --warn: #f59e0b;
  --phase1: #8b5cf6;
  --phase2: #3b82f6;
  --phase3: #10b981;
}

/* Streamlit 기본 흔적 제거 */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stDecoration"] { display: none; }

/* 전체 레이아웃 */
.block-container {
  padding-top: 1.5rem !important;
  padding-bottom: 2rem !important;
  max-width: 800px !important;
}

body, .stApp {
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 16px;
  line-height: 1.6;
  color: var(--text);
  background: var(--bg);
  letter-spacing: -0.01em;
}

/* 카드 */
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  margin-bottom: 16px;
}

/* 스크립트 박스 */
.script-box {
  background: #fffdf6;
  border-left: 4px solid #c9a227;
  border-radius: 0 8px 8px 0;
  padding: 14px 18px;
  margin: 12px 0;
  font-size: 15px;
}
.script-who {
  font-weight: 700;
  font-size: 11px;
  color: #8a6d1c;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  margin-bottom: 4px;
}

/* AI 응답 박스 */
.ai-response {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 8px;
  padding: 14px 18px;
  margin: 10px 0;
  font-size: 15px;
}
.ai-label {
  font-size: 11px;
  font-weight: 700;
  color: #0284c7;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  margin-bottom: 4px;
}

/* 목표 리스트 */
.goal-item {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  margin: 6px 0;
  font-size: 14px;
  color: var(--text-sub);
}
.goal-item::before {
  content: "→ ";
  color: var(--accent);
  font-weight: 600;
}

/* Phase 뱃지 */
.phase-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

/* 경고 박스 */
.warn-box {
  background: #fff5e6;
  border-left: 4px solid #d35400;
  border-radius: 0 8px 8px 0;
  padding: 12px 16px;
  margin: 10px 0;
  font-size: 14px;
}

/* 팁 박스 */
.tip-box {
  background: #e8f4f8;
  border-left: 4px solid var(--accent);
  border-radius: 0 8px 8px 0;
  padding: 12px 16px;
  margin: 10px 0;
  font-size: 14px;
}

/* 버튼 재정의 */
.stButton > button {
  border-radius: 8px !important;
  font-family: 'Pretendard', sans-serif !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  transition: all 0.15s ease !important;
}
.stButton > button:hover {
  filter: brightness(0.93) !important;
  transform: translateY(-1px) !important;
}

/* textarea */
.stTextArea textarea {
  border-radius: 8px !important;
  border-color: var(--border) !important;
  font-family: 'Pretendard', sans-serif !important;
  font-size: 15px !important;
  line-height: 1.6 !important;
}
.stTextArea textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 2px rgba(59,130,246,0.15) !important;
}

/* 진행 인디케이터 */
.progress-container {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 24px;
}
.phase-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 6px 0;
}
.phase-label {
  font-size: 11px;
  font-weight: 700;
  min-width: 140px;
  color: var(--text-sub);
}
.step-dot {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  border: 2px solid var(--border);
  color: var(--text-sub);
  background: var(--bg);
  transition: all 0.2s;
}
.step-dot.done {
  background: var(--success);
  border-color: var(--success);
  color: white;
}
.step-dot.current {
  border-color: currentColor;
  color: white;
  animation: pulse 1.5s ease-in-out infinite;
}
.step-connector {
  width: 20px;
  height: 2px;
  background: var(--border);
  border-radius: 2px;
}
.step-connector.done {
  background: var(--success);
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.08); opacity: 0.85; }
}

/* 주차 헤더 */
.week-header {
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 20px;
  color: white;
}
.week-header .week-num {
  font-size: 11px;
  letter-spacing: 2px;
  opacity: 0.75;
  margin-bottom: 4px;
}
.week-header h2 {
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 4px 0;
  color: white !important;
}
.week-header .tagline {
  font-size: 14px;
  opacity: 0.85;
  font-style: italic;
}

/* 완료 화면 */
.completion-card {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 16px;
  padding: 40px;
  text-align: center;
  color: white;
  margin: 20px 0;
}
.completion-card h1 {
  font-size: 28px;
  margin-bottom: 12px;
  color: white !important;
}

/* API 키 안내 카드 */
.api-warning {
  background: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 12px;
  padding: 24px;
  margin: 20px 0;
}
.api-warning h3 {
  color: #856404;
  margin-bottom: 12px;
}
.api-warning ol {
  color: #533f03;
  padding-left: 20px;
}
.api-warning li {
  margin-bottom: 8px;
}
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)
