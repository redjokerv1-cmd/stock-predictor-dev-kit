#!/bin/bash
# 환경 검증 스크립트

echo "🔍 시스템 요구사항 확인..."
echo ""

# Python 버전 확인
if command -v python &> /dev/null; then
    python_version=$(python --version 2>&1 | awk '{print $2}')
    echo "✅ Python: $python_version"
    
    # Python 3.11+ 권장
    major=$(echo $python_version | cut -d. -f1)
    minor=$(echo $python_version | cut -d. -f2)
    if [ "$major" -ge 3 ] && [ "$minor" -ge 11 ]; then
        echo "   👍 Python 3.11+ (권장)"
    else
        echo "   ⚠️ Python 3.11+ 권장 (현재: $python_version)"
    fi
else
    echo "❌ Python 미설치"
fi

# Node.js 버전 확인
if command -v node &> /dev/null; then
    node_version=$(node --version)
    echo "✅ Node.js: $node_version"
    
    # Node 18+ 권장
    major=$(echo $node_version | cut -d. -f1 | sed 's/v//')
    if [ "$major" -ge 18 ]; then
        echo "   👍 Node.js 18+ (권장)"
    else
        echo "   ⚠️ Node.js 18+ 권장 (현재: $node_version)"
    fi
else
    echo "❌ Node.js 미설치"
fi

# npm 버전 확인
if command -v npm &> /dev/null; then
    npm_version=$(npm --version)
    echo "✅ npm: $npm_version"
else
    echo "❌ npm 미설치"
fi

# Git 확인
if command -v git &> /dev/null; then
    git_version=$(git --version | awk '{print $3}')
    echo "✅ Git: $git_version"
else
    echo "❌ Git 미설치"
fi

echo ""
echo "📁 저장소 확인..."
echo ""

# Backend 확인
if [ -d "../stock-predictor-backend" ]; then
    echo "✅ Backend 저장소 존재"
    
    if [ -f "../stock-predictor-backend/.env" ]; then
        echo "   ✅ .env 파일 존재"
        
        # API 키 설정 확인
        source ../stock-predictor-backend/.env 2>/dev/null
        
        if [ -n "$GEMINI_API_KEY" ] && [ "$GEMINI_API_KEY" != "your-gemini-api-key-here" ]; then
            echo "   ✅ GEMINI_API_KEY 설정됨"
        else
            echo "   ⚠️ GEMINI_API_KEY 미설정 (.env 수정 필요)"
        fi
        
        if [ -n "$KIS_APP_KEY" ] && [ "$KIS_APP_KEY" != "your-kis-app-key" ]; then
            echo "   ✅ KIS_APP_KEY 설정됨"
        else
            echo "   ⚠️ KIS_APP_KEY 미설정 (.env 수정 필요)"
        fi
        
        if [ -n "$YOUTUBE_API_KEY" ] && [ "$YOUTUBE_API_KEY" != "your-youtube-api-key" ]; then
            echo "   ✅ YOUTUBE_API_KEY 설정됨"
        else
            echo "   ⚠️ YOUTUBE_API_KEY 미설정 (.env 수정 필요)"
        fi
        
        if [ -n "$REDDIT_CLIENT_ID" ] && [ "$REDDIT_CLIENT_ID" != "your-reddit-client-id" ]; then
            echo "   ✅ REDDIT_CLIENT_ID 설정됨"
        else
            echo "   ⚠️ REDDIT_CLIENT_ID 미설정 (.env 수정 필요)"
        fi
    else
        echo "   ❌ .env 파일 없음 (setup.sh 실행 필요)"
    fi
    
    if [ -d "../stock-predictor-backend/venv" ]; then
        echo "   ✅ Python 가상 환경 존재"
    else
        echo "   ❌ Python 가상 환경 없음 (setup.sh 실행 필요)"
    fi
else
    echo "❌ Backend 저장소 없음 (setup.sh 실행 필요)"
fi

# Frontend 확인
if [ -d "../stock-predictor-frontend" ]; then
    echo "✅ Frontend 저장소 존재"
    
    if [ -f "../stock-predictor-frontend/.env" ]; then
        echo "   ✅ .env 파일 존재"
    else
        echo "   ❌ .env 파일 없음 (setup.sh 실행 필요)"
    fi
    
    if [ -d "../stock-predictor-frontend/node_modules" ]; then
        echo "   ✅ npm 패키지 설치됨"
    else
        echo "   ❌ npm 패키지 미설치 (setup.sh 실행 필요)"
    fi
else
    echo "❌ Frontend 저장소 없음 (setup.sh 실행 필요)"
fi

# Universal DevKit 확인
if [ -d "../universal-devkit" ]; then
    echo "✅ Universal DevKit 저장소 존재"
else
    echo "⚠️ Universal DevKit 저장소 없음 (선택 사항)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

