# 프로젝트 인계 문서 — 10주 자기주도 문제해결 컨설팅 웹앱

## 프로젝트 개요

Google Gemini 2.5 Flash Lite 기반 Streamlit 웹앱.  
사용자가 10주 동안 자기주도적으로 문제를 정의하고 해결책을 결정하는 훈련 프로그램.  
AI는 답을 가르치지 않고 소크라테스식 질문만 던짐.

- **로컬 경로**: `C:\Users\user\self-directed-consulting\`
- **GitHub**: `https://github.com/fyzwAz-2kuvbe-mimdet/self.git`
- **배포 대상**: Streamlit Community Cloud (https://share.streamlit.io)

---

## 로컬 실행

```powershell
cd C:\Users\user\self-directed-consulting

# 의존성 설치 (pip 대신 python -m pip 사용 — Windows PATH 이슈)
python -m pip install -r requirements.txt

# API 키 설정 (최초 1회)
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
# secrets.toml 열어 실제 Gemini API 키 입력

# 실행
python -m streamlit run streamlit_app.py
```

**API 키 발급**: https://aistudio.google.com (무료)

---

## 디렉토리 구조

```
self-directed-consulting/
├── streamlit_app.py          # 진입점 + 라우터
├── requirements.txt          # streamlit>=1.36, google-genai>=0.3.0
├── .gitignore                # secrets.toml 제외
├── .streamlit/
│   ├── secrets.toml          # 실제 API 키 (커밋 금지!)
│   └── secrets.toml.example  # 예시만 커밋
├── core/
│   ├── llm.py                # Gemini 호출 래퍼
│   ├── prompts.py            # 프롬프트 조립
│   ├── state.py              # session_state 관리
│   └── manual_data.py        # 10주차 매뉴얼 데이터
├── steps/
│   ├── base_step.py          # 핵심 렌더러 (질문 1개씩 순차)
│   ├── step01_week1.py       # → render_step(1)
│   ├── step02_week2.py       # → render_step(2)
│   └── ... (step03~step10)
└── ui/
    ├── styles.py             # 전역 CSS
    ├── components.py         # 공용 컴포넌트
    └── progress.py           # 10단계 진행 인디케이터
```

---

## 핵심 아키텍처

### 라우팅 (streamlit_app.py)

```python
is_landing = not st.session_state.started   # 랜딩/세션 분기
if is_landing: render_landing(); return
render_progress(current, completed)
if current == 10 and 10 in completed: render_completion(); return
importlib.import_module(STEP_MODULES[current]).render()
```

### 세션 상태 스키마 (core/state.py)

```python
{
  "current_step": 1,            # 현재 보고 있는 주차 (1~10)
  "started": False,             # 랜딩 → 세션 진입 플래그
  "completed_steps": [],        # 완료된 주차 번호 목록
  "step_answers": {1:{}, 2:{}, ...},        # 주차별 {question_id: 답변}
  "step_ai_responses": {1:[], 2:[], ...},   # 주차별 AI 응답 목록
  "step_question_index": {1:0, 2:0, ...},   # (초기화용, 실제는 q_idx_N 사용)
}
# 런타임 추가 키:
#   q_idx_{step}     : 주차별 현재 질문 인덱스
#   air_{step}_{qid} : 질문별 AI 응답 캐시
#   session_summary_{step} : 주차 완료 시 AI 요약
```

### 질문 순차 표시 로직 (steps/base_step.py)

```python
q_idx_key = f"q_idx_{step}"
cur_idx = st.session_state.get(q_idx_key, 0)

# 완료 질문 → 축약 미리보기(.done-q)
for i in range(cur_idx): ...

# 현재 질문 → 카드 + textarea + 버튼
if cur_idx < len(questions):
    # [💬 AI질문받기] [다음질문→ / ✅모든질문완료]

# 전체 완료 → 🎉 + 과제 + [↩다시보기 | ←이전 | 다음주차→]
else: ...
```

### 네비게이션 패턴 (ui/progress.py)

**HTML `<a>` 태그 절대 사용 금지** — 브라우저 풀 리로드 시 새 WebSocket 세션 생성, 상태 소실.  
반드시 `st.button + st.rerun()` 방식 사용.

```python
cols = st.columns(10)
for week, col in enumerate(cols, start=1):
    with col:
        if st.button(label, key=f"nav_w{week}"):
            st.session_state.started = True
            st.session_state.current_step = week
            st.rerun()
```

---

## 데이터 구조

### WEEK_DATA (core/manual_data.py)

```python
WEEK_DATA = {
  1: {
    "phase": 1,
    "title": "문제 정의",
    "tagline": "...",
    "goals": ["목표1", "목표2", ...],
    "intro_script": "컨설턴트 도입 멘트...",
    "questions": [
      {"id": "w1q1", "label": "질문 내용", "placeholder": "힌트 텍스트"},
      ...
    ],
    "homework": ["과제1", "과제2", ...],
    "common_problems": ["흔한 문제 패턴1", ...],
  },
  ...
}

PHASE_INFO = {
  1: {"name": "문제 정의", "color": "#8b5cf6", "weeks": [1,2,3]},
  2: {"name": "해결책 설계", "color": "#3b82f6", "weeks": [4,5,6,7]},
  3: {"name": "실행 & 회고", "color": "#10b981", "weeks": [8,9,10]},
}
```

### 주차별 질문 수
| 주차 | 질문 수 |
|------|---------|
| 1    | 3       |
| 2    | 4       |
| 3    | 3       |
| 4    | 4       |
| 5    | 3       |
| 6    | 4       |
| 7    | 4       |
| 8    | 3       |
| 9    | 4       |
| 10   | 4       |

### 외부 연동용 JSON 스키마

```json
{
  "completed_steps": [1, 2],
  "answers": {
    "1": {"w1q1": "답변 텍스트", "w1q2": "...", "w1q3": "..."},
    "2": {"w2q1": "...", ...}
  },
  "ai_responses": {
    "1": ["AI 응답1", "AI 응답2"],
    "2": []
  }
}
```
`get_all_data()` (core/state.py) 호출로 이 구조 획득 가능.

---

## LLM 설정 (core/llm.py)

```python
MODEL_NAME = "gemini-2.5-flash-lite-preview-06-17"
MAX_OUTPUT_TOKENS = 200    # 짧고 날카로운 질문만 생성
# 30초 타임아웃, 1회 재시도
# API 키: st.secrets["GEMINI_API_KEY"]
```

AI 컨설턴트 규칙 (`CONSULTANT_RULES` in manual_data.py):
- 답 절대 제시 금지
- 질문 1개씩만
- "잘했어요" 류 칭찬 금지
- 침묵/저항 존중
- 과정만 평가

---

## GitHub 업로드

```powershell
cd C:\Users\user\self-directed-consulting
git add .
git commit -m "feat: 질문 순차 팝업 + 네비게이션 버튼 수정"
git push
```

**주의**: `secrets.toml`은 `.gitignore`에 포함됨 → 커밋되지 않음. Streamlit Cloud에는 앱 설정에서 별도 입력.

---

## Streamlit Cloud 배포

1. https://share.streamlit.io 접속
2. New app → Repository: `fyzwAz-2kuvbe-mimdet/self`, Branch: `main`, File: `streamlit_app.py`
3. Settings → Secrets 탭 → `GEMINI_API_KEY = "AIza..."` 입력 후 저장
4. Deploy 클릭

---

## 알려진 이슈 & 주의사항

| 이슈 | 원인 | 해결 |
|------|------|------|
| `pip` 명령 인식 안 됨 | Windows PATH | `python -m pip` 사용 |
| 버튼 클릭 후 화면 변화 없음 | `st.session_state` 업데이트 후 `st.rerun()` 누락 | 항상 `st.rerun()` 호출 |
| textarea 다크 배경 | Streamlit 기본 테마 | CSS `!important` 오버라이드 |
| HTML `<a>` 네비 작동 안 됨 | 새 WebSocket 세션 생성 | `st.button + st.rerun()` 방식 |
| `git remote add` 오류 | 이미 등록됨 | `git remote set-url origin [URL]` |

---

## 미완료 작업

- [ ] 최신 변경사항 GitHub 푸시 (progress.py + base_step.py 재작성분)
- [ ] Streamlit Cloud 배포 및 실제 URL 확인
- [ ] AI 응답 실 환경 테스트 (Gemini API 키 필요)
