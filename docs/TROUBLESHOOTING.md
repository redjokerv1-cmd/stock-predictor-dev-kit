# 🔧 문제 해결 가이드

Stock Predictor 개발 환경 구성 시 자주 발생하는 문제와 해결 방법입니다.

---

## 🐍 Python 관련 문제

### Python not found

**증상:**
```
'python' is not recognized as an internal or external command
```

**해결:**
1. Python 3.11+ 설치: https://www.python.org/downloads/
2. 설치 시 "Add Python to PATH" 체크
3. 터미널 재시작

**확인:**
```bash
python --version  # 3.11 이상이어야 함
```

---

### venv 생성 실패

**증상:**
```
Error: No module named venv
```

**해결 (Ubuntu/Debian):**
```bash
sudo apt install python3.11-venv
```

**해결 (Windows):**
- Python 재설치 시 "pip" 옵션 체크

---

### pip install 실패

**증상:**
```
ERROR: Could not find a version that satisfies the requirement...
```

**해결:**
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 캐시 삭제 후 재시도
pip cache purge
pip install -r requirements.txt
```

---

## 📦 Node.js 관련 문제

### Node.js not found

**증상:**
```
'node' is not recognized as an internal or external command
```

**해결:**
1. Node.js 18+ 설치: https://nodejs.org/
2. LTS 버전 권장
3. 터미널 재시작

**확인:**
```bash
node --version  # 18 이상
npm --version   # 9 이상
```

---

### npm install 실패

**증상:**
```
npm ERR! code ENOENT
npm ERR! syscall open
```

**해결:**
```bash
# npm 캐시 삭제
npm cache clean --force

# node_modules 삭제 후 재설치
rm -rf node_modules package-lock.json  # Windows: rmdir /s node_modules, del package-lock.json
npm install
```

---

### EACCES: permission denied

**증상:**
```
npm ERR! code EACCES
npm ERR! errno -13
```

**해결 (Unix/Linux/Mac):**
```bash
# npm 전역 디렉토리 권한 변경
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) /usr/local/lib/node_modules
```

**해결 (Windows):**
- 관리자 권한으로 PowerShell 실행

---

## 🔑 API 키 관련 문제

### Gemini API: "API key not valid"

**원인:**
- 잘못된 API 키
- API가 활성화되지 않음

**해결:**
1. Google AI Studio에서 새 키 생성
2. Google Cloud Console에서 "Generative Language API" 활성화 확인
3. `.env` 파일에 공백 없이 복사

---

### KIS API: "인증 실패"

**원인:**
- 모의투자 계좌 미발급
- APP Key/Secret 순서 바뀜

**해결:**
1. https://apiportal.koreainvestment.com 에서 모의투자 신청
2. `.env` 파일 확인:
   ```bash
   KIS_APP_KEY=앱키_여기
   KIS_APP_SECRET=시크릿_여기
   ```

---

### YouTube API: "quotaExceeded"

**원인:**
- 하루 할당량 (10,000 단위) 초과

**해결:**
- 내일까지 대기 (자정에 리셋)
- 또는 Google Cloud Console에서 할당량 증가 요청

---

### Reddit API: "invalid_client"

**원인:**
- App type이 "script"가 아님
- Client ID/Secret 잘못됨

**해결:**
1. https://www.reddit.com/prefs/apps 에서 앱 삭제
2. 새 앱 생성 시 **"script"** 타입 선택
3. `.env` 파일에 Client ID (짧은 것), Secret (긴 것) 순서 확인

---

## 🌐 Git 관련 문제

### git clone: Permission denied (publickey)

**증상:**
```
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.
```

**해결:**

**방법 1: SSH 키 설정 (권장)**
```bash
# SSH 키 생성
ssh-keygen -t ed25519 -C "your_email@example.com"

# 공개키 복사
cat ~/.ssh/id_ed25519.pub  # Windows: type %USERPROFILE%\.ssh\id_ed25519.pub

# GitHub에 등록
# https://github.com/settings/keys
```

**방법 2: HTTPS로 클론**
```bash
git clone https://github.com/redjokerv1-cmd/stock-predictor-backend.git
git clone https://github.com/redjokerv1-cmd/stock-predictor-frontend.git
```

---

### git: command not found

**해결:**
1. Git 설치: https://git-scm.com/downloads
2. 터미널 재시작

---

## 🚀 실행 관련 문제

### Backend: ModuleNotFoundError

**증상:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**해결:**
```bash
# 가상 환경 활성화 확인!
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 재설치
pip install -r requirements.txt
```

---

### Backend: uvicorn: command not found

**원인:**
- 가상 환경 미활성화

**해결:**
```bash
# 가상 환경 활성화
source venv/bin/activate  # Windows: venv\Scripts\activate

# uvicorn 재설치
pip install uvicorn
```

---

### Backend: Port 8000 already in use

**증상:**
```
ERROR:    [Errno 48] Address already in use
```

**해결:**

**Unix/Linux/Mac:**
```bash
# 8000 포트 사용 프로세스 찾기
lsof -i:8000

# 프로세스 종료
kill -9 <PID>
```

**Windows:**
```powershell
# 8000 포트 사용 프로세스 찾기
netstat -ano | findstr :8000

# 프로세스 종료
taskkill /PID <PID> /F
```

**또는 다른 포트 사용:**
```bash
uvicorn api.main:app --port 8001
```

---

### Frontend: VITE_API_URL not defined

**증상:**
```
Uncaught ReferenceError: VITE_API_URL is not defined
```

**해결:**
1. `stock-predictor-frontend/.env` 파일 존재 확인
2. 파일 내용:
   ```bash
   VITE_API_URL=http://localhost:8000/api
   ```
3. Frontend 재시작 (npm run dev)

---

### Frontend: Failed to fetch

**증상:**
```
TypeError: Failed to fetch
```

**원인:**
- Backend가 실행되지 않음
- CORS 설정 문제

**해결:**
1. Backend 실행 확인:
   ```bash
   curl http://localhost:8000/api/health
   # {"status":"healthy","version":"2.0.0"}
   ```
2. Backend `.env`의 `ALLOWED_ORIGINS` 확인

---

## 🖥️ 운영체제별 문제

### Windows: PowerShell Execution Policy

**증상:**
```
... cannot be loaded because running scripts is disabled on this system
```

**해결:**
```powershell
# 관리자 권한 PowerShell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Mac: zsh: command not found

**해결:**
```bash
# ~/.zshrc에 PATH 추가
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

### Linux: apt install 권한 오류

**해결:**
```bash
# sudo 권한 필요
sudo apt update
sudo apt install python3.11 python3.11-venv
```

---

## 📊 데이터 관련 문제

### yfinance: No data found

**증상:**
```
No data found, symbol may be delisted
```

**원인:**
- 잘못된 티커 심볼
- 시장 휴장일

**해결:**
- 티커 확인: 삼성전자는 `005930.KS` (한국), Apple은 `AAPL` (미국)
- 시장 시간 확인

---

### KIS API: 빈 응답

**원인:**
- API 키 미설정
- 모의투자 계좌 미발급

**해결:**
- [API 키 가이드](API_KEYS_GUIDE.md) 재확인

---

## 🔥 긴급 복구

### 전체 재설정

**모든 것을 삭제하고 처음부터:**

```bash
# 저장소 삭제
rm -rf stock-predictor-backend
rm -rf stock-predictor-frontend
rm -rf development-rules

# Dev Kit에서 setup 재실행
cd stock-predictor-dev-kit
./scripts/setup.sh  # Windows: .\scripts\setup.bat
```

---

## 📞 추가 지원

- **문서**: [docs/](../)
- **API 가이드**: [API_KEYS_GUIDE.md](API_KEYS_GUIDE.md)
- **개발 규칙**: https://github.com/redjokerv1-cmd/development-rules

**해결되지 않은 문제:**
- GitHub Issue 생성: https://github.com/redjokerv1-cmd/stock-predictor-dev-kit/issues

---

**🎯 대부분의 문제는 위 가이드로 해결됩니다!**

해결되지 않으면 Issue를 생성해주세요.

