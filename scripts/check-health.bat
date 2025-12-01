@echo off
REM 환경 검증 스크립트 (Windows)

echo 🔍 시스템 요구사항 확인...
echo.

REM Python 버전 확인
python --version >nul 2>&1
if %errorlevel% == 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
    echo ✅ Python: !python_version!
) else (
    echo ❌ Python 미설치
)

REM Node.js 버전 확인
node --version >nul 2>&1
if %errorlevel% == 0 (
    for /f %%i in ('node --version') do set node_version=%%i
    echo ✅ Node.js: !node_version!
) else (
    echo ❌ Node.js 미설치
)

REM npm 버전 확인
npm --version >nul 2>&1
if %errorlevel% == 0 (
    for /f %%i in ('npm --version') do set npm_version=%%i
    echo ✅ npm: !npm_version!
) else (
    echo ❌ npm 미설치
)

REM Git 확인
git --version >nul 2>&1
if %errorlevel% == 0 (
    for /f "tokens=3" %%i in ('git --version') do set git_version=%%i
    echo ✅ Git: !git_version!
) else (
    echo ❌ Git 미설치
)

echo.
echo 📁 저장소 확인...
echo.

REM Backend 확인
if exist "..\stock-predictor-backend" (
    echo ✅ Backend 저장소 존재
    
    if exist "..\stock-predictor-backend\.env" (
        echo    ✅ .env 파일 존재
    ) else (
        echo    ❌ .env 파일 없음 (setup.bat 실행 필요)
    )
    
    if exist "..\stock-predictor-backend\venv" (
        echo    ✅ Python 가상 환경 존재
    ) else (
        echo    ❌ Python 가상 환경 없음 (setup.bat 실행 필요)
    )
) else (
    echo ❌ Backend 저장소 없음 (setup.bat 실행 필요)
)

REM Frontend 확인
if exist "..\stock-predictor-frontend" (
    echo ✅ Frontend 저장소 존재
    
    if exist "..\stock-predictor-frontend\.env" (
        echo    ✅ .env 파일 존재
    ) else (
        echo    ❌ .env 파일 없음 (setup.bat 실행 필요)
    )
    
    if exist "..\stock-predictor-frontend\node_modules" (
        echo    ✅ npm 패키지 설치됨
    ) else (
        echo    ❌ npm 패키지 미설치 (setup.bat 실행 필요)
    )
) else (
    echo ❌ Frontend 저장소 없음 (setup.bat 실행 필요)
)

REM Development Rules 확인
if exist "..\development-rules" (
    echo ✅ Development Rules 저장소 존재
) else (
    echo ⚠️ Development Rules 저장소 없음 (선택 사항)
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

