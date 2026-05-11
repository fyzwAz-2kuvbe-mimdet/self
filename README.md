# 10주 자기주도 문제해결 컨설팅 웹앱

Onsight 능력 훈련 프로그램 — Google Gemini 2.5 Flash Lite 기반 컨설팅 도구

## 로컬 실행

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. API 키 설정
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# secrets.toml 파일을 열어 실제 API 키 입력

# 3. 실행
streamlit run streamlit_app.py
```

`.streamlit/secrets.toml` 내용:
```toml
GEMINI_API_KEY = "AIza..."
```

## GitHub → Streamlit Cloud 배포

### 1. GitHub 저장소 생성
`self-directed-consulting` 이름으로 public 저장소를 만든다.

### 2. 로컬에서 푸시
```bash
git init
git add .
git commit -m "init: 10주 자기주도 컨설팅 웹앱"
git branch -M main
git remote add origin https://github.com/<USERNAME>/self-directed-consulting.git
git push -u origin main
```

### 3. Streamlit Community Cloud 접속
https://share.streamlit.io 에 접속한다.

### 4. 앱 배포
- **New app** 클릭
- Repository: `<USERNAME>/self-directed-consulting`
- Branch: `main`
- Main file path: `streamlit_app.py`

### 5. Secrets 설정
- 앱 페이지 → `⋯` → **Settings** → **Secrets** 탭
- 다음 내용 입력 후 저장:
```toml
GEMINI_API_KEY = "AIza..."
```

### 6. 배포
**Deploy** 클릭. 약 1~2분 후 URL 발급.

## API 키 발급
https://aistudio.google.com 에서 무료로 발급 가능.

## 디렉토리 구조
```
self-directed-consulting/
├── streamlit_app.py        # 진입점
├── requirements.txt
├── core/
│   ├── llm.py              # Gemini 호출
│   ├── prompts.py          # 단계별 프롬프트
│   ├── state.py            # session_state 관리
│   └── manual_data.py      # 매뉴얼 10주차 데이터
├── steps/
│   ├── base_step.py        # 공통 렌더러
│   └── step01~10_weekN.py  # 주차별 화면
└── ui/
    ├── styles.py           # CSS
    ├── components.py       # 공용 컴포넌트
    └── progress.py         # 진행 인디케이터
```
