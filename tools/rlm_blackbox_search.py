"""
RLM-Based Blackbox Search Tool

에러 발생 시 과거 incidents, knowhow, sessions에서
RLM 패턴으로 유사 사례를 검색

Author: Human + AI (동료로서 함께)
Created: 2026-01-20
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SearchResult:
    """검색 결과"""
    source: str           # "incident", "knowhow", "session"
    file: str
    relevance_score: float
    matched_keywords: List[str]
    title: str
    solution: Optional[str] = None
    prevention: Optional[str] = None
    data: Dict = field(default_factory=dict)


class RLMBlackboxSearch:
    """
    RLM 기반 Blackbox 검색
    
    RLM 패턴:
    1. 에러 메시지에서 키워드 추출 (프로그래밍적)
    2. 각 소스(incidents, knowhow, sessions)에서 필터링
    3. 관련성 점수 계산
    4. 결과 집계 및 순위화
    """
    
    def __init__(self, blackbox_path: str = None):
        self.blackbox_path = Path(blackbox_path) if blackbox_path else self._find_blackbox()
        self.index: Dict[str, List[Dict]] = {}
        
        if self.blackbox_path and self.blackbox_path.exists():
            self._build_index()
    
    def _find_blackbox(self) -> Optional[Path]:
        """Blackbox 경로 자동 탐지"""
        possible_paths = [
            Path(__file__).parent.parent / "blackbox",
            Path("F:/AI/projects-hub/stock-predictor-dev-kit/blackbox"),
            Path.cwd() / "blackbox",
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        return None
    
    def _build_index(self):
        """JSON 파일 인덱싱"""
        sources = ["incidents", "knowhow", "sessions"]
        
        for source in sources:
            source_path = self.blackbox_path / source
            if not source_path.exists():
                continue
            
            self.index[source] = []
            
            for json_file in source_path.glob("*.json"):
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        self.index[source].append({
                            "file": str(json_file.name),
                            "path": str(json_file),
                            "data": data
                        })
                except Exception as e:
                    print(f"[WARN] Failed to load {json_file}: {e}")
    
    def search(self, error_message: str, top_n: int = 5) -> List[SearchResult]:
        """
        에러 메시지로 검색
        
        RLM 패턴:
        1. 키워드 추출
        2. 각 소스에서 매칭
        3. 점수 계산 및 정렬
        """
        keywords = self._extract_keywords(error_message)
        results: List[SearchResult] = []
        
        # 각 소스에서 검색
        for source, items in self.index.items():
            for item in items:
                matched = self._match_item(item["data"], keywords, source)
                if matched:
                    matched.file = item["file"]
                    matched.source = source
                    results.append(matched)
        
        # 점수순 정렬
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return results[:top_n]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """에러 메시지에서 키워드 추출"""
        keywords = []
        
        # 에러 타입 추출
        error_types = re.findall(r"([A-Z][a-z]+Error|Exception|Failed)", text)
        keywords.extend(error_types)
        
        # 메서드/함수명 추출
        methods = re.findall(r"'([a-zA-Z_][a-zA-Z0-9_]*)'", text)
        keywords.extend(methods)
        
        # 클래스명 추출
        classes = re.findall(r"([A-Z][a-zA-Z]+)", text)
        keywords.extend([c for c in classes if len(c) > 3])
        
        # 파일 경로 추출
        files = re.findall(r"([a-z_]+\.py)", text)
        keywords.extend(files)
        
        # 중복 제거 및 소문자화
        keywords = list(set(k.lower() for k in keywords))
        
        return keywords[:15]  # 상위 15개
    
    def _match_item(self, data: Dict, keywords: List[str], source: str) -> Optional[SearchResult]:
        """항목과 키워드 매칭"""
        # JSON을 문자열로 변환
        data_str = json.dumps(data, ensure_ascii=False).lower()
        
        matched_keywords = []
        for kw in keywords:
            if kw in data_str:
                matched_keywords.append(kw)
        
        if not matched_keywords:
            return None
        
        # 관련성 점수 계산
        score = len(matched_keywords) / max(len(keywords), 1)
        
        # 특정 필드에서 매칭되면 가중치
        if source == "incidents":
            if any(kw in str(data.get("symptom", "")).lower() for kw in keywords):
                score += 0.3
            if any(kw in str(data.get("error_log", "")).lower() for kw in keywords):
                score += 0.2
        elif source == "knowhow":
            if any(kw in str(data.get("pattern", "")).lower() for kw in keywords):
                score += 0.3
        
        # 결과 생성
        title = data.get("title") or data.get("pattern") or data.get("date", "Unknown")
        
        solution = None
        if "solution" in data:
            if isinstance(data["solution"], dict):
                solution = data["solution"].get("description")
            else:
                solution = str(data["solution"])
        
        prevention = None
        if "prevention" in data:
            if isinstance(data["prevention"], dict):
                prevention = data["prevention"].get("rule")
            else:
                prevention = str(data["prevention"])
        
        return SearchResult(
            source=source,
            file="",
            relevance_score=min(score, 1.0),
            matched_keywords=matched_keywords,
            title=title,
            solution=solution,
            prevention=prevention,
            data=data
        )
    
    def get_prevention_checklist(self, error_message: str) -> List[str]:
        """에러 방지 체크리스트 생성"""
        results = self.search(error_message, top_n=3)
        
        checklist = []
        for result in results:
            if result.prevention:
                checklist.append(f"[{result.source}] {result.prevention}")
            
            # incidents의 check_command
            if result.source == "incidents":
                prevention = result.data.get("prevention", {})
                if isinstance(prevention, dict) and "check_command" in prevention:
                    checklist.append(f"[CHECK] {prevention['check_command']}")
        
        return checklist
    
    def get_stats(self) -> Dict:
        """통계"""
        return {
            "sources": list(self.index.keys()),
            "total_items": sum(len(items) for items in self.index.values()),
            "by_source": {source: len(items) for source, items in self.index.items()}
        }


# ============================================================================
# Quick Access
# ============================================================================

def search_blackbox(error: str, top_n: int = 5) -> List[SearchResult]:
    """빠른 검색"""
    searcher = RLMBlackboxSearch()
    return searcher.search(error, top_n)


def get_prevention(error: str) -> List[str]:
    """방지 체크리스트"""
    searcher = RLMBlackboxSearch()
    return searcher.get_prevention_checklist(error)


# ============================================================================
# Self-Test
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("[RLM] Blackbox Search Tool")
    print("=" * 60)
    
    searcher = RLMBlackboxSearch()
    
    if not searcher.blackbox_path:
        print("[ERROR] Blackbox not found!")
        exit(1)
    
    print(f"\n[OK] Blackbox found at: {searcher.blackbox_path}")
    
    stats = searcher.get_stats()
    print(f"\n[STATS]")
    print(f"   Total items: {stats['total_items']}")
    for source, count in stats['by_source'].items():
        print(f"   - {source}: {count}")
    
    # 테스트 검색
    test_error = "'SentimentAggregator' object has no attribute 'aggregate'"
    
    print(f"\n" + "=" * 60)
    print(f"[TEST] Searching for: {test_error[:50]}...")
    print("=" * 60)
    
    results = searcher.search(test_error)
    
    print(f"\n[RESULTS] Found {len(results)} matches:")
    for i, result in enumerate(results, 1):
        print(f"\n   {i}. [{result.source}] {result.title}")
        print(f"      Score: {result.relevance_score:.2f}")
        print(f"      Keywords: {', '.join(result.matched_keywords[:5])}")
        if result.solution:
            print(f"      Solution: {result.solution[:60]}...")
        if result.prevention:
            print(f"      Prevention: {result.prevention[:60]}...")
    
    # 체크리스트
    print(f"\n" + "=" * 60)
    print("[CHECKLIST] Prevention checklist:")
    print("=" * 60)
    
    checklist = searcher.get_prevention_checklist(test_error)
    for item in checklist:
        print(f"   - {item}")
    
    print("\n[OK] Blackbox Search is ready!")
    print("=" * 60)
