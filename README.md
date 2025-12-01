# 🚀 Stock Predictor - Developer Kit

**새 PC에서 5분 안에 개발 환경 완성!**

이 저장소는 Stock Predictor 프로젝트의 개발 환경을 자동으로 구성해주는 도구 모음입니다.

---

## ⚡ Quick Start

### 1️⃣ 이 저장소 클론

```bash
git clone git@github.com:redjokerv1-cmd/stock-predictor-dev-kit.git
cd stock-predictor-dev-kit
```

### 2️⃣ 자동 설정 실행

**Unix/Linux/Mac:**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

**Windows (PowerShell):**
```powershell
.\scripts\setup.bat
```

**자동으로 수행되는 작업:**
- ✅ Backend/Frontend 저장소 자동 클론
- ✅ Development Rules 저장소 클론
- ✅ 환경 변수 템플릿 복사 (.env 생성)
- ✅ Python 가상 환경 생성
- ✅ Backend 의존성 설치 (pip install)
- ✅ Frontend 의존성 설치 (npm install)
- ✅ 환경 검증 (Python, Node.js 버전 확인)

### 3️⃣ API 키 발급 및 입력

1. [API 키 발급 가이드](docs/API_KEYS_GUIDE.md) 참고 (5분 소요)
2. `stock-predictor-backend/.env` 파일 열기
3. 다음 API 키 입력:
   - `GEMINI_API_KEY` (필수)
   - `KIS_APP_KEY`, `KIS_APP_SECRET` (필수)
   - `YOUTUBE_API_KEY` (필수)
   - `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET` (필수)

### 4️⃣ 실행

**Terminal 1: Backend**
```bash
cd stock-predictor-backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn api.main:app --reload
```

**Terminal 2: Frontend**
```bash
cd stock-predictor-frontend
npm run dev
```

### 5️⃣ 브라우저에서 확인

- **Frontend**: http://localhost:5173
- **Backend API Docs**: http://localhost:8000/docs
- **Backend Health**: http://localhost:8000/api/health

---

## 📦 포함된 내용

### 🗂️ 저장소 구조

```
stock-predictor-dev-kit/
├── env-templates/              # 환경 변수 템플릿
│   ├── backend.env.example     # Backend 환경 변수
│   ├── frontend.env.example    # Frontend 환경 변수
│   └── railway.env.example     # Railway 배포용
├── scripts/
│   ├── setup.sh                # Unix/Linux/Mac 자동 설정
│   ├── setup.bat               # Windows 자동 설정
│   ├── check-health.sh         # 환경 검증 (Unix)
│   └── check-health.bat        # 환경 검증 (Windows)
├── docs/
│   ├── API_KEYS_GUIDE.md       # API 키 발급 방법
│   ├── SETUP_GUIDE.md          # 상세 설정 가이드
│   ├── TROUBLESHOOTING.md      # 문제 해결
│   └── ARCHITECTURE.md         # 프로젝트 구조
├── tools/
│   └── (향후 추가 예정)
└── README.md                   # 이 파일
```

### 🎯 주요 기능

| 기능 | 설명 |
|------|------|
| **원클릭 환경 구성** | setup.sh/bat 실행으로 모든 설정 자동화 |
| **환경 변수 템플릿** | 주석으로 상세 설명된 .env.example |
| **헬스 체크** | Python, Node.js 버전 및 API 키 설정 확인 |
| **API 키 가이드** | 각 API 발급 방법 및 링크 제공 |
| **문제 해결 가이드** | 흔한 에러 및 해결 방법 정리 |

---

## 🛠️ 시스템 요구사항

### 필수

- **Python**: 3.11+ (권장)
- **Node.js**: 18+ (권장)
- **Git**: 최신 버전
- **npm**: 9+ (Node.js와 함께 설치됨)

### 확인 방법

```bash
python --version  # 3.11 이상
node --version    # 18 이상
npm --version     # 9 이상
git --version     # 최신
```

---

## 📖 문서

- [API 키 발급 방법](docs/API_KEYS_GUIDE.md) - Gemini, KIS, YouTube, Reddit API 발급 가이드
- [상세 설정 가이드](docs/SETUP_GUIDE.md) - 수동 설정 방법
- [프로젝트 구조](docs/ARCHITECTURE.md) - 전체 아키텍처 설명
- [문제 해결](docs/TROUBLESHOOTING.md) - 흔한 에러 해결 방법
- [개발 규칙](https://github.com/redjokerv1-cmd/development-rules) - 코딩 가이드라인

---

## 🔧 수동 설정 (고급)

자동 스크립트를 사용하지 않으려면:

### 1. 저장소 클론

```bash
git clone git@github.com:redjokerv1-cmd/stock-predictor-backend.git
git clone git@github.com:redjokerv1-cmd/stock-predictor-frontend.git
git clone git@github.com:redjokerv1-cmd/development-rules.git
```

### 2. 환경 변수 설정

```bash
cp stock-predictor-dev-kit/env-templates/backend.env.example stock-predictor-backend/.env
cp stock-predictor-dev-kit/env-templates/frontend.env.example stock-predictor-frontend/.env
```

### 3. Backend 설정

```bash
cd stock-predictor-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Frontend 설정

```bash
cd stock-predictor-frontend
npm install
```

자세한 내용은 [상세 설정 가이드](docs/SETUP_GUIDE.md)를 참고하세요.

---

## ⚠️ 문제 해결

### Python not found

- Python 3.11+ 설치: https://www.python.org/downloads/
- PATH 환경 변수 확인

### Node.js not found

- Node.js 18+ 설치: https://nodejs.org/
- LTS 버전 권장

### Git authentication failed

- SSH 키 설정: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- 또는 HTTPS 방식으로 클론

### API 키 발급 문제

- [API 키 발급 가이드](docs/API_KEYS_GUIDE.md) 참고
- 각 API 별 발급 소요 시간:
  - Gemini: 1분
  - KIS: 5분 (계좌 발급 포함)
  - YouTube: 3분
  - Reddit: 2분

자세한 문제 해결 방법: [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## 🚀 배포

### Backend (Railway)

```bash
cd stock-predictor-backend
git push origin main
# Railway가 자동으로 감지하여 배포
```

### Frontend (Vercel)

```bash
cd stock-predictor-frontend
npm run build
git push origin main
# Vercel이 자동으로 감지하여 배포
```

배포용 환경 변수는 `env-templates/railway.env.example` 참고

---

## 🤝 기여

이 Dev Kit 개선 아이디어가 있으시면:

1. Issue 생성
2. Pull Request 제출
3. [Development Rules](https://github.com/redjokerv1-cmd/development-rules) 준수

---

## 📞 지원

- **문서**: [docs/](docs/)
- **문제 해결**: [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **개발 규칙**: https://github.com/redjokerv1-cmd/development-rules

---

## 📝 라이선스

MIT License

---

**🎉 Happy Coding!**

새 PC에서도 5분 안에 개발 시작!

