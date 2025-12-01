#!/bin/bash
# Stock Predictor - 개발 환경 자동 설정 스크립트
# 사용법: chmod +x scripts/setup.sh && ./scripts/setup.sh

set -e  # 에러 발생 시 즉시 중단

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Stock Predictor 개발 환경 설정 시작"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 현재 디렉토리 확인
DEVKIT_DIR=$(pwd)
echo "📁 작업 디렉토리: $DEVKIT_DIR"
echo ""

# 1. Git 저장소 클론
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 1/5: Git 저장소 클론 중..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd ..

if [ ! -d "stock-predictor-backend" ]; then
    echo "🔹 Backend 클론 중..."
    git clone git@github.com:redjokerv1-cmd/stock-predictor-backend.git
    echo "✅ Backend 클론 완료"
else
    echo "⚠️ Backend 이미 존재 (스킵)"
fi

if [ ! -d "stock-predictor-frontend" ]; then
    echo "🔹 Frontend 클론 중..."
    git clone git@github.com:redjokerv1-cmd/stock-predictor-frontend.git
    echo "✅ Frontend 클론 완료"
else
    echo "⚠️ Frontend 이미 존재 (스킵)"
fi

if [ ! -d "development-rules" ]; then
    echo "🔹 Development Rules 클론 중..."
    git clone git@github.com:redjokerv1-cmd/development-rules.git
    echo "✅ Development Rules 클론 완료"
else
    echo "⚠️ Development Rules 이미 존재 (스킵)"
fi

echo ""

# 2. 환경 변수 설정
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 2/5: 환경 변수 설정 중..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cp $DEVKIT_DIR/.env.example/backend.env.example stock-predictor-backend/.env
echo "✅ Backend .env 생성 완료"

cp $DEVKIT_DIR/.env.example/frontend.env.example stock-predictor-frontend/.env
echo "✅ Frontend .env 생성 완료"

echo ""
echo "⚠️  다음 파일을 열어 API 키를 입력하세요:"
echo "   📄 stock-predictor-backend/.env"
echo "   📄 stock-predictor-frontend/.env"
echo ""
echo "   💡 API 키 발급 방법: docs/API_KEYS_GUIDE.md 참고"
echo ""

# 3. Backend 의존성 설치
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📚 3/5: Backend 의존성 설치 중..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd stock-predictor-backend

if [ ! -d "venv" ]; then
    echo "🔹 가상 환경 생성 중..."
    python -m venv venv
    echo "✅ 가상 환경 생성 완료"
fi

echo "🔹 의존성 설치 중 (1-2분 소요)..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✅ Backend 의존성 설치 완료"

cd ..
echo ""

# 4. Frontend 의존성 설치
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📚 4/5: Frontend 의존성 설치 중..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd stock-predictor-frontend

if [ ! -d "node_modules" ]; then
    echo "🔹 npm 패키지 설치 중 (2-3분 소요)..."
    npm install
    echo "✅ Frontend 의존성 설치 완료"
else
    echo "⚠️ node_modules 이미 존재 (스킵)"
fi

cd ..
echo ""

# 5. 환경 검증
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 5/5: 환경 검증 중..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd $DEVKIT_DIR
bash scripts/check-health.sh

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 설정 완료!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 다음 단계:"
echo ""
echo "1️⃣  API 키 입력 (5분 소요)"
echo "   📄 stock-predictor-backend/.env"
echo "   💡 가이드: $DEVKIT_DIR/docs/API_KEYS_GUIDE.md"
echo ""
echo "2️⃣  Backend 실행 (Terminal 1)"
echo "   cd stock-predictor-backend"
echo "   source venv/bin/activate"
echo "   uvicorn api.main:app --reload"
echo ""
echo "3️⃣  Frontend 실행 (Terminal 2)"
echo "   cd stock-predictor-frontend"
echo "   npm run dev"
echo ""
echo "4️⃣  브라우저에서 확인"
echo "   Frontend: http://localhost:5173"
echo "   Backend Docs: http://localhost:8000/docs"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

