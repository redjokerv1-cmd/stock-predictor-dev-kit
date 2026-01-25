# Stock Predictor - GraphRAG 업그레이드 계획

**작성일**: 2026-01-25
**기반**: Semantica 분석 (universal-devkit/research/semantica-integration-analysis.md)

---

## 목표

기존 숫자 기반 분석에 **공급망 지식 그래프**를 추가하여:
- 2차, 3차 수혜주 자동 발굴
- 뉴스 기반 관계 추론
- 환각률 15% 이하 달성

---

## 새로운 모듈

### 1. SupplyChainGraph

```python
# core/supply_chain_graph.py

@dataclass
class CompanyEntity:
    id: str
    name: str
    aliases: List[str]  # 삼성전자, Samsung, 005930
    sector: str
    market: str

@dataclass  
class SupplyRelation:
    source: str      # 공급사
    target: str      # 수요사
    relation_type: str  # supplies, competes, partners
    product: str     # 반도체, 배터리
    confidence: float
    source_doc: str

class SupplyChainGraph:
    def extract_from_text(self, text: str) -> List[SupplyRelation]
    def find_beneficiaries(self, company: str, hops: int = 2) -> List[Dict]
    def get_supply_chain(self, company: str) -> Dict
```

### 2. NewsNERExtractor

```python
# core/news_ner.py

class NewsNERExtractor:
    """Gemini API로 뉴스에서 기업/관계 추출"""
    
    def extract(self, news_text: str) -> Dict:
        # Returns:
        # {
        #   "entities": [{"name": "삼성전자", "type": "company", "ticker": "005930.KS"}],
        #   "relations": [{"source": "삼성전자", "target": "엔비디아", "type": "supplies"}]
        # }
```

### 3. StockGraphRAG

```python
# core/graph_rag.py

class StockGraphRAG:
    """하이브리드 검색 (Vector + Graph)"""
    
    def query(self, question: str) -> Dict
    def find_hidden_beneficiaries(self, event: str) -> List[Dict]
```

---

## 사용 예시

```python
# "엔비디아 실적 호조" 시나리오

graph_rag = StockGraphRAG(supply_graph, vector_store)

result = graph_rag.find_hidden_beneficiaries("엔비디아 실적 호조")

# 결과:
# 1차 수혜: 삼성전자 (HBM 공급), SK하이닉스
# 2차 수혜: 한미반도체 (장비), 원익IPS
# 3차 수혜: 솔브레인 (소재), SK머티리얼즈
```

---

## API 엔드포인트

```python
# v3_endpoints.py (예정)

@router.get("/supply-chain/{ticker}")
async def get_supply_chain(ticker: str):
    """공급망 시각화 데이터"""
    
@router.post("/graph-query")
async def graph_query(question: str):
    """GraphRAG 질의"""
    
@router.get("/beneficiaries/{event}")
async def find_beneficiaries(event: str, hops: int = 2):
    """수혜주 발굴"""
```

---

## 프론트엔드 연동

```tsx
// components/SupplyChainGraph.tsx
// vis.js 또는 D3.js로 공급망 시각화

// 기능:
// - 노드 클릭 시 기업 상세 정보
// - 관계 타입별 색상 구분
// - 수혜 경로 하이라이트
```

---

## 구현 우선순위

1. [ ] `SupplyChainGraph` 기본 구조
2. [ ] 삼성전자/SK하이닉스 샘플 데이터 입력
3. [ ] `NewsNERExtractor` (Gemini 연동)
4. [ ] `StockGraphRAG` 하이브리드 검색
5. [ ] API 엔드포인트
6. [ ] 프론트엔드 시각화

---

## 예상 성과

| 지표 | 현재 | 목표 |
|------|------|------|
| 수혜주 발굴 | 1차만 | 2~3차 연결 |
| 분석 깊이 | PER/PBR | + 공급망 관계 |
| 추천 근거 | 숫자 | 숫자 + 관계 |

---

*참고: universal-devkit/research/semantica-integration-analysis.md*
