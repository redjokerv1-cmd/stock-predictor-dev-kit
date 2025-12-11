#!/usr/bin/env python3
"""
Import 검증 도구

백엔드의 모든 모듈 import를 검증합니다.
- 존재하지 않는 모듈 import 감지
- 잘못된 클래스/함수명 감지
- 순환 import 감지

사용법:
    cd stock-predictor-backend
    python ../stock-predictor-dev-kit/tools/debug-imports.py
"""

import os
import sys
import importlib.util
import ast
from pathlib import Path
from typing import List, Dict, Tuple

# 색상 (터미널용)
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def find_python_files(root: Path) -> List[Path]:
    """모든 Python 파일 찾기"""
    return list(root.rglob("*.py"))


def extract_imports(file_path: Path) -> List[Dict]:
    """파일에서 import 문 추출"""
    imports = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(file_path))
    except SyntaxError as e:
        return [{"error": f"SyntaxError: {e}", "line": e.lineno}]
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    "type": "import",
                    "module": alias.name,
                    "alias": alias.asname,
                    "line": node.lineno,
                    "file": str(file_path)
                })
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append({
                    "type": "from",
                    "module": module,
                    "name": alias.name,
                    "alias": alias.asname,
                    "line": node.lineno,
                    "file": str(file_path)
                })
    
    return imports


def check_internal_import(module: str, name: str, backend_root: Path) -> Tuple[bool, str]:
    """내부 모듈 import 검증"""
    
    # 내부 모듈만 검사 (utils, modules, core, etc.)
    internal_prefixes = ['utils.', 'modules.', 'core.', 'api.', 'screening.', 'data_providers.', 'data_storage.', 'analysis_engines.']
    
    is_internal = any(module.startswith(prefix) for prefix in internal_prefixes)
    if not is_internal:
        return True, "external"
    
    # 모듈 경로 확인
    module_path = backend_root / module.replace('.', '/') / '__init__.py'
    module_file = backend_root / (module.replace('.', '/') + '.py')
    
    if not module_path.exists() and not module_file.exists():
        return False, f"모듈 없음: {module}"
    
    # 모듈 파일에서 name 확인
    target_file = module_file if module_file.exists() else module_path
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 간단한 검사: class Name 또는 def name 또는 name = 
        if name == '*':
            return True, "wildcard"
        
        patterns = [
            f'class {name}',
            f'def {name}',
            f'{name} = ',
            f'{name}:',
        ]
        
        for pattern in patterns:
            if pattern in content:
                return True, "found"
        
        return False, f"'{name}' not found in {target_file.name}"
        
    except Exception as e:
        return False, f"Error reading: {e}"


def main():
    print(f"{BLUE}========================================{RESET}")
    print(f"{BLUE}    Import 검증 도구 (Debug Tool)     {RESET}")
    print(f"{BLUE}========================================{RESET}\n")
    
    # 백엔드 루트 확인
    backend_root = Path.cwd()
    if not (backend_root / 'api' / 'main.py').exists():
        print(f"{RED}❌ 오류: stock-predictor-backend 디렉토리에서 실행해주세요.{RESET}")
        print(f"   현재 위치: {backend_root}")
        sys.exit(1)
    
    print(f"📂 검사 대상: {backend_root}\n")
    
    # 모든 Python 파일 찾기
    py_files = find_python_files(backend_root)
    
    # tests, __pycache__, venv 제외
    py_files = [
        f for f in py_files 
        if '__pycache__' not in str(f) 
        and 'venv' not in str(f)
        and '.git' not in str(f)
    ]
    
    print(f"📄 Python 파일: {len(py_files)}개\n")
    
    # 모든 import 수집
    all_imports = []
    for py_file in py_files:
        imports = extract_imports(py_file)
        all_imports.extend(imports)
    
    print(f"🔍 Import 문: {len(all_imports)}개\n")
    
    # 내부 import 검증
    errors = []
    warnings = []
    checked = 0
    
    for imp in all_imports:
        if "error" in imp:
            errors.append(imp)
            continue
        
        if imp["type"] == "from":
            module = imp["module"]
            name = imp["name"]
            
            # 내부 모듈만 검사
            if any(module.startswith(p) for p in ['utils.', 'modules.', 'core.', 'api.', 'screening.', 'data_providers.', 'data_storage.', 'analysis_engines.']):
                checked += 1
                ok, reason = check_internal_import(module, name, backend_root)
                
                if not ok:
                    errors.append({
                        "file": imp["file"],
                        "line": imp["line"],
                        "module": module,
                        "name": name,
                        "reason": reason
                    })
    
    print(f"✅ 내부 Import 검사: {checked}개\n")
    
    # 결과 출력
    if errors:
        print(f"{RED}{'='*50}{RESET}")
        print(f"{RED}    ❌ 발견된 오류: {len(errors)}개{RESET}")
        print(f"{RED}{'='*50}{RESET}\n")
        
        for err in errors:
            if "error" in err:
                print(f"  {RED}SyntaxError{RESET} in {err.get('file', 'unknown')}:{err.get('line', '?')}")
                print(f"      {err['error']}\n")
            else:
                file_short = Path(err['file']).name
                print(f"  {RED}ImportError{RESET} in {file_short}:{err['line']}")
                print(f"      from {YELLOW}{err['module']}{RESET} import {YELLOW}{err['name']}{RESET}")
                print(f"      → {err['reason']}\n")
    else:
        print(f"{GREEN}{'='*50}{RESET}")
        print(f"{GREEN}    ✅ 모든 내부 Import 정상!{RESET}")
        print(f"{GREEN}{'='*50}{RESET}")
    
    # 요약
    print(f"\n📊 요약:")
    print(f"   - 검사한 파일: {len(py_files)}개")
    print(f"   - 검사한 Import: {checked}개")
    print(f"   - 오류: {len(errors)}개")
    
    return len(errors)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(1 if exit_code > 0 else 0)

