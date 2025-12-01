@echo off
REM Stock Predictor - 개발 환경 자동 설정 스크립트 (Windows)
REM 사용법: .\scripts\setup.bat

setlocal enabledelayedexpansion

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🚀 Stock Predictor 개발 환경 설정 시작
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM 현재 디렉토리 저장
set DEVKIT_DIR=%CD%
echo 📁 작업 디렉토리: %DEVKIT_DIR%
echo.

REM 1. Git 저장소 클론
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 📦 1/5: Git 저장소 클론 중...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cd ..

if not exist "stock-predictor-backend" (
    echo 🔹 Backend 클론 중...
    git clone git@github.com:redjokerv1-cmd/stock-predictor-backend.git
    echo ✅ Backend 클론 완료
) else (
    echo ⚠️ Backend 이미 존재 (스킵)
)

if not exist "stock-predictor-frontend" (
    echo 🔹 Frontend 클론 중...
    git clone git@github.com:redjokerv1-cmd/stock-predictor-frontend.git
    echo ✅ Frontend 클론 완료
) else (
    echo ⚠️ Frontend 이미 존재 (스킵)
)

if not exist "development-rules" (
    echo 🔹 Development Rules 클론 중...
    git clone git@github.com:redjokerv1-cmd/development-rules.git
    echo ✅ Development Rules 클론 완료
) else (
    echo ⚠️ Development Rules 이미 존재 (스킵)
)

echo.

REM 2. 환경 변수 설정
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🔧 2/5: 환경 변수 설정 중...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

copy "%DEVKIT_DIR%\.env.example\backend.env.example" "stock-predictor-backend\.env" >nul
echo ✅ Backend .env 생성 완료

copy "%DEVKIT_DIR%\.env.example\frontend.env.example" "stock-predictor-frontend\.env" >nul
echo ✅ Frontend .env 생성 완료

echo.
echo ⚠️  다음 파일을 열어 API 키를 입력하세요:
echo    📄 stock-predictor-backend\.env
echo    📄 stock-predictor-frontend\.env
echo.
echo    💡 API 키 발급 방법: docs\API_KEYS_GUIDE.md 참고
echo.

REM 3. Backend 의존성 설치
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 📚 3/5: Backend 의존성 설치 중...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cd stock-predictor-backend

if not exist "venv" (
    echo 🔹 가상 환경 생성 중...
    python -m venv venv
    echo ✅ 가상 환경 생성 완료
)

echo 🔹 의존성 설치 중 (1-2분 소요)...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
echo ✅ Backend 의존성 설치 완료

cd ..
echo.

REM 4. Frontend 의존성 설치
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 📚 4/5: Frontend 의존성 설치 중...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cd stock-predictor-frontend

if not exist "node_modules" (
    echo 🔹 npm 패키지 설치 중 (2-3분 소요)...
    call npm install
    echo ✅ Frontend 의존성 설치 완료
) else (
    echo ⚠️ node_modules 이미 존재 (스킵)
)

cd ..
echo.

REM 5. 환경 검증
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ✅ 5/5: 환경 검증 중...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cd %DEVKIT_DIR%
call scripts\check-health.bat

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🎉 설정 완료!
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 📋 다음 단계:
echo.
echo 1️⃣  API 키 입력 (5분 소요)
echo    📄 stock-predictor-backend\.env
echo    💡 가이드: %DEVKIT_DIR%\docs\API_KEYS_GUIDE.md
echo.
echo 2️⃣  Backend 실행 (Terminal 1)
echo    cd stock-predictor-backend
echo    venv\Scripts\activate
echo    uvicorn api.main:app --reload
echo.
echo 3️⃣  Frontend 실행 (Terminal 2)
echo    cd stock-predictor-frontend
echo    npm run dev
echo.
echo 4️⃣  브라우저에서 확인
echo    Frontend: http://localhost:5173
echo    Backend Docs: http://localhost:8000/docs
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

pause

