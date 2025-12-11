#!/usr/bin/env python3
"""
🔧 종합 시스템 검사 도구 (Full System Check)

모든 검사를 한 번에 수행합니다:
1. Git 상태 확인
2. Import 검증 (백엔드)
3. 타입 검사 (프론트엔드)
4. 빌드 테스트
5. API 헬스체크
6. 테스트 실행

사용법:
    cd stock-predictor-dev-kit
    python tools/full-check.py [--local | --prod]
    
    --local: 로컬 환경 검사 (기본값)
    --prod:  프로덕션 환경 검사
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

# 색상
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


class SystemChecker:
    """종합 시스템 검사기"""
    
    def __init__(self, mode: str = 'local'):
        self.mode = mode
        self.results = []
        self.start_time = datetime.now()
        
        # 경로 설정
        self.dev_kit_root = Path(__file__).parent.parent
        self.project_root = self.dev_kit_root.parent
        self.backend_root = self.project_root / 'stock-predictor-backend'
        self.frontend_root = self.project_root / 'stock-predictor-frontend'
        
        # 배포 URL
        self.prod_backend_url = "https://web-production-805a.up.railway.app"
        self.prod_frontend_url = "https://stock-predictor-frontend-blush.vercel.app"
    
    def log(self, message: str, level: str = 'info'):
        """로그 출력"""
        colors = {
            'info': CYAN,
            'success': GREEN,
            'warning': YELLOW,
            'error': RED,
            'header': BLUE + BOLD
        }
        print(f"{colors.get(level, '')}{message}{RESET}")
    
    def run_command(self, cmd: list, cwd: Path = None, timeout: int = 300) -> tuple:
        """명령 실행"""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=(os.name == 'nt')  # Windows에서는 shell=True
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Timeout"
        except Exception as e:
            return False, "", str(e)
    
    def add_result(self, name: str, passed: bool, details: str = ""):
        """결과 추가"""
        self.results.append({
            'name': name,
            'passed': passed,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
        
        status = f"{GREEN}✅ PASS{RESET}" if passed else f"{RED}❌ FAIL{RESET}"
        self.log(f"  {status} {name}")
        
        if not passed and details:
            for line in details.split('\n')[:5]:
                self.log(f"      {line}", 'error')
    
    # ========================================
    # 검사 항목들
    # ========================================
    
    def check_git_status(self):
        """Git 상태 확인"""
        self.log("\n📁 Git 상태 확인", 'header')
        
        for name, path in [('Backend', self.backend_root), ('Frontend', self.frontend_root)]:
            if not path.exists():
                self.add_result(f"{name} Git", False, "디렉토리 없음")
                continue
            
            success, stdout, stderr = self.run_command(['git', 'status', '--porcelain'], cwd=path)
            
            if success:
                if stdout.strip():
                    self.add_result(f"{name} Git", False, f"커밋되지 않은 변경: {len(stdout.strip().split(chr(10)))}개")
                else:
                    self.add_result(f"{name} Git", True)
            else:
                self.add_result(f"{name} Git", False, stderr)
    
    def check_imports(self):
        """Import 검증"""
        self.log("\n🔍 Import 검증 (Backend)", 'header')
        
        import_checker = self.dev_kit_root / 'tools' / 'debug-imports.py'
        
        if not import_checker.exists():
            self.add_result("Import 검증", False, "debug-imports.py 없음")
            return
        
        success, stdout, stderr = self.run_command(
            [sys.executable, str(import_checker)],
            cwd=self.backend_root
        )
        
        if "모든 내부 Import 정상" in stdout:
            self.add_result("Import 검증", True)
        else:
            # 오류 개수 추출
            error_count = stdout.count("ImportError")
            self.add_result("Import 검증", False, f"{error_count}개 오류 발견")
    
    def check_typescript(self):
        """TypeScript 타입 검사"""
        self.log("\n📘 TypeScript 검사 (Frontend)", 'header')
        
        if not self.frontend_root.exists():
            self.add_result("TypeScript 검사", False, "디렉토리 없음")
            return
        
        # npm이 설치되어 있는지 확인
        success, stdout, _ = self.run_command(['npm', '--version'])
        if not success:
            self.add_result("TypeScript 검사", False, "npm not found")
            return
        
        # 타입 검사
        success, stdout, stderr = self.run_command(
            ['npm', 'run', 'type-check'] if os.name != 'nt' else ['npm.cmd', 'run', 'type-check'],
            cwd=self.frontend_root,
            timeout=120
        )
        
        if success:
            self.add_result("TypeScript 검사", True)
        else:
            # package.json에 type-check 스크립트가 없을 수 있음
            if "Missing script" in stderr or "missing script" in stderr.lower():
                # tsc 직접 실행 시도
                success, stdout, stderr = self.run_command(
                    ['npx', 'tsc', '--noEmit'] if os.name != 'nt' else ['npx.cmd', 'tsc', '--noEmit'],
                    cwd=self.frontend_root,
                    timeout=120
                )
                if success or "error TS" not in stderr:
                    self.add_result("TypeScript 검사", True)
                else:
                    error_count = stderr.count("error TS")
                    self.add_result("TypeScript 검사", False, f"{error_count}개 타입 에러")
            else:
                self.add_result("TypeScript 검사", False, stderr[:200])
    
    def check_build(self):
        """빌드 테스트"""
        self.log("\n🏗️ 빌드 테스트", 'header')
        
        # Frontend 빌드
        if self.frontend_root.exists():
            success, stdout, stderr = self.run_command(
                ['npm', 'run', 'build'] if os.name != 'nt' else ['npm.cmd', 'run', 'build'],
                cwd=self.frontend_root,
                timeout=180
            )
            
            if success or "built in" in stdout:
                self.add_result("Frontend 빌드", True)
            else:
                self.add_result("Frontend 빌드", False, stderr[:200])
    
    def check_tests(self):
        """테스트 실행"""
        self.log("\n🧪 테스트 실행", 'header')
        
        if not self.backend_root.exists():
            self.add_result("Backend 테스트", False, "디렉토리 없음")
            return
        
        # pytest 실행
        success, stdout, stderr = self.run_command(
            [sys.executable, '-m', 'pytest', '--tb=no', '-q'],
            cwd=self.backend_root,
            timeout=300
        )
        
        if success:
            # 통과 개수 추출
            if "passed" in stdout:
                self.add_result("Backend 테스트", True, stdout.split('\n')[-2])
            else:
                self.add_result("Backend 테스트", True)
        else:
            if "failed" in stdout:
                failed_count = stdout.count("FAILED")
                self.add_result("Backend 테스트", False, f"{failed_count}개 실패")
            else:
                self.add_result("Backend 테스트", False, stderr[:200])
    
    def check_api_health(self):
        """API 헬스체크"""
        self.log("\n🌐 API 헬스체크", 'header')
        
        import urllib.request
        import urllib.error
        
        urls = []
        if self.mode == 'prod':
            urls = [
                (f"{self.prod_backend_url}/", "Backend Health"),
                (f"{self.prod_backend_url}/api/v2/health", "V2 API Health"),
            ]
        else:
            urls = [
                ("http://localhost:8000/", "Backend Health (Local)"),
                ("http://localhost:8000/api/v2/health", "V2 API Health (Local)"),
            ]
        
        for url, name in urls:
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    if response.status == 200:
                        self.add_result(name, True)
                    else:
                        self.add_result(name, False, f"Status: {response.status}")
            except urllib.error.URLError as e:
                if self.mode == 'local':
                    self.add_result(name, False, "서버 미실행 (로컬)")
                else:
                    self.add_result(name, False, str(e.reason))
            except Exception as e:
                self.add_result(name, False, str(e))
    
    def check_dependencies(self):
        """의존성 확인"""
        self.log("\n📦 의존성 확인", 'header')
        
        # Backend requirements.txt 확인
        req_file = self.backend_root / 'requirements.txt'
        if req_file.exists():
            with open(req_file, 'r') as f:
                lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
            self.add_result("Backend requirements.txt", True, f"{len(lines)}개 패키지")
        else:
            self.add_result("Backend requirements.txt", False, "파일 없음")
        
        # Frontend package.json 확인
        pkg_file = self.frontend_root / 'package.json'
        if pkg_file.exists():
            with open(pkg_file, 'r') as f:
                pkg = json.load(f)
            deps = len(pkg.get('dependencies', {})) + len(pkg.get('devDependencies', {}))
            self.add_result("Frontend package.json", True, f"{deps}개 패키지")
        else:
            self.add_result("Frontend package.json", False, "파일 없음")
    
    # ========================================
    # 실행
    # ========================================
    
    def run(self):
        """전체 검사 실행"""
        self.log(f"\n{'='*60}", 'header')
        self.log(f"   🔧 종합 시스템 검사 (Full System Check)", 'header')
        self.log(f"   모드: {'🏠 Local' if self.mode == 'local' else '🌐 Production'}", 'header')
        self.log(f"{'='*60}", 'header')
        
        # 검사 실행
        self.check_dependencies()
        self.check_git_status()
        self.check_imports()
        self.check_typescript()
        self.check_build()
        self.check_tests()
        self.check_api_health()
        
        # 결과 요약
        elapsed = (datetime.now() - self.start_time).total_seconds()
        passed = sum(1 for r in self.results if r['passed'])
        total = len(self.results)
        
        self.log(f"\n{'='*60}", 'header')
        self.log(f"   📊 검사 결과: {passed}/{total} 통과", 'header')
        self.log(f"   ⏱️ 소요 시간: {elapsed:.1f}초", 'header')
        self.log(f"{'='*60}", 'header')
        
        if passed == total:
            self.log("\n✅ 모든 검사 통과! 배포 준비 완료.", 'success')
        else:
            self.log(f"\n❌ {total - passed}개 검사 실패. 위 오류를 확인하세요.", 'error')
        
        # 결과 저장
        result_file = self.dev_kit_root / 'tools' / '.last-check-result.json'
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': self.start_time.isoformat(),
                'mode': self.mode,
                'passed': passed,
                'total': total,
                'elapsed_seconds': elapsed,
                'results': self.results
            }, f, indent=2, ensure_ascii=False)
        
        return passed == total


def main():
    mode = 'prod' if '--prod' in sys.argv else 'local'
    
    checker = SystemChecker(mode=mode)
    success = checker.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

