#!/usr/bin/env python3
"""
API 엔드포인트 테스트 도구

백엔드 API의 모든 엔드포인트를 테스트합니다.
- Health Check
- 종목 검색
- 분석 API
- V2 API

사용법:
    python debug-api.py [URL]
    
예시:
    python debug-api.py                           # 로컬 (localhost:8000)
    python debug-api.py https://your-backend.up.railway.app
"""

import sys
import json
import time
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# 색상
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def test_endpoint(base_url: str, path: str, method: str = 'GET', data: dict = None, timeout: int = 30) -> dict:
    """엔드포인트 테스트"""
    url = f"{base_url}{path}"
    
    start = time.time()
    
    try:
        if data:
            req = Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method=method
            )
        else:
            req = Request(url, method=method)
        
        with urlopen(req, timeout=timeout) as response:
            elapsed = time.time() - start
            body = json.loads(response.read().decode('utf-8'))
            
            return {
                "success": True,
                "status": response.status,
                "elapsed": f"{elapsed:.2f}s",
                "body": body
            }
    
    except HTTPError as e:
        elapsed = time.time() - start
        try:
            body = json.loads(e.read().decode('utf-8'))
        except:
            body = e.reason
        
        return {
            "success": False,
            "status": e.code,
            "elapsed": f"{elapsed:.2f}s",
            "error": body
        }
    
    except URLError as e:
        return {
            "success": False,
            "status": 0,
            "elapsed": "-",
            "error": str(e.reason)
        }
    
    except Exception as e:
        return {
            "success": False,
            "status": 0,
            "elapsed": "-",
            "error": str(e)
        }


def print_result(name: str, result: dict):
    """결과 출력"""
    if result["success"]:
        status_color = GREEN
        icon = "✅"
    else:
        status_color = RED
        icon = "❌"
    
    print(f"  {icon} {name}")
    print(f"     Status: {status_color}{result['status']}{RESET}")
    print(f"     Time: {result['elapsed']}")
    
    if not result["success"]:
        print(f"     Error: {RED}{result.get('error', 'Unknown')}{RESET}")
    
    print()


def main():
    print(f"{BLUE}========================================{RESET}")
    print(f"{BLUE}     API 엔드포인트 테스트 도구       {RESET}")
    print(f"{BLUE}========================================{RESET}\n")
    
    # 기본 URL
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    # 후행 슬래시 제거
    base_url = base_url.rstrip('/')
    
    print(f"🌐 대상 서버: {base_url}\n")
    
    # 테스트 케이스
    tests = [
        # 기본
        ("Health Check", "/", "GET", None),
        ("API Health", "/api/health", "GET", None),
        
        # 종목 검색
        ("종목 검색 (삼성)", "/api/stocks/search?q=삼성&max_items=5", "GET", None),
        ("종목 검색 (AAPL)", "/api/stocks/search?q=AAPL&max_items=5", "GET", None),
        
        # 시장 데이터
        ("시장 지수", "/api/market/indices", "GET", None),
        ("환율", "/api/market/exchange", "GET", None),
        
        # V2 API
        ("V2 Health", "/api/v2/health", "GET", None),
        ("V2 Engines", "/api/v2/engines", "GET", None),
        
        # 분석 (시간이 오래 걸림)
        ("분석 (SK하이닉스)", "/api/analyze", "POST", {"ticker": "000660.KS", "period": "1mo"}),
    ]
    
    # 테스트 실행
    results = []
    success_count = 0
    
    for name, path, method, data in tests:
        print(f"🔍 Testing: {name}...")
        result = test_endpoint(base_url, path, method, data)
        print_result(name, result)
        
        results.append((name, result))
        if result["success"]:
            success_count += 1
    
    # 요약
    print(f"{BLUE}========================================{RESET}")
    print(f"📊 요약: {success_count}/{len(tests)} 성공")
    
    if success_count == len(tests):
        print(f"{GREEN}✅ 모든 테스트 통과!{RESET}")
    else:
        failed = [name for name, r in results if not r["success"]]
        print(f"{RED}❌ 실패: {', '.join(failed)}{RESET}")
    
    print(f"{BLUE}========================================{RESET}")
    
    return 0 if success_count == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())

