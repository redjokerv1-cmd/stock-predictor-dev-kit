# 📦 AI Blackbox - 개발 기록 시스템

**목적**: AI 에이전트가 참조할 수 있는 체계적인 작업 기록

---

## 🎯 용도

이 폴더는 **AI가 읽는 용도**로 설계되었습니다:

1. **작업 기록** (`sessions/`): 날짜별 작업 내용
2. **문제-해결 매핑** (`incidents/`): 발생한 문제와 해결 방법
3. **의사결정 기록** (`decisions/`): 중요한 기술적 결정
4. **검증 결과** (`validations/`): 테스트/검사 결과

---

## 📂 구조

```
blackbox/
├── README.md           # 이 파일
├── sessions/           # 날짜별 작업 세션 기록
│   └── 2025-12-11.json
├── incidents/          # 문제 발생 → 해결 기록
│   └── incident-001.json
├── decisions/          # 기술적 의사결정 기록
│   └── decision-001.json
└── validations/        # 검증/테스트 결과
    └── check-2025-12-11.json
```

---

## 📋 스키마

### Session (작업 기록)

```json
{
  "id": "session-2025-12-11-001",
  "date": "2025-12-11",
  "duration_hours": 4.5,
  "tasks_completed": [
    "포트폴리오 데이터 손실 버그 수정",
    "센티멘트 분석기 메서드명 수정"
  ],
  "files_modified": [
    "frontend/src/utils/storage/adapters/portfolio-adapter.ts",
    "backend/modules/sentiment_analyzer.py"
  ],
  "commits": [
    { "hash": "abc123", "message": "fix: ...", "repo": "frontend" }
  ],
  "issues_encountered": ["incident-001"],
  "next_steps": ["Phase 4 구현"]
}
```

### Incident (문제 기록)

```json
{
  "id": "incident-001",
  "severity": "critical",
  "title": "SentimentAggregator.aggregate 메서드 없음",
  "symptom": "'SentimentAggregator' object has no attribute 'aggregate'",
  "root_cause": "메서드명이 aggregate_sentiments인데 aggregate로 호출",
  "solution": "올바른 메서드명으로 수정",
  "files_fixed": ["backend/modules/sentiment_analyzer.py"],
  "prevention": "새 모듈 사용 시 메서드명 확인 필수",
  "related_rules": ["GEN-004", "LIB-001"],
  "timestamp": "2025-12-11T07:30:00Z"
}
```

### Decision (의사결정)

```json
{
  "id": "decision-001",
  "title": "PostgreSQL/Redis 도입 보류",
  "context": "소규모 프로젝트에서 DB 비용 부담",
  "options": [
    { "name": "PostgreSQL + Redis", "pros": "확장성", "cons": "비용" },
    { "name": "In-memory + LocalStorage", "pros": "무료", "cons": "영속성 제한" }
  ],
  "decision": "현재는 In-memory + LocalStorage 사용",
  "rationale": "10명 미만 사용자에서는 비용 효율성 우선",
  "revisit_when": "사용자 10명 초과 시",
  "timestamp": "2025-12-10T15:00:00Z"
}
```

---

## 🔧 사용법

### 1. AI 에이전트에게 제공

새 세션 시작 시:
```
"blackbox/sessions/ 폴더에서 최근 작업 기록을 확인하고 
 blackbox/incidents/ 에서 비슷한 문제가 있었는지 확인해"
```

### 2. 기록 추가

작업 완료 후:
```
"오늘 작업 내용을 blackbox/sessions/2025-12-11.json에 기록해"
```

### 3. 문제 해결 시

```
"이 문제를 blackbox/incidents/에 기록하고,
 다음에 같은 문제가 생기면 참조할 수 있게 해"
```

---

## 🎯 AI 활용 예시

```python
# AI 프롬프트 예시
"""
1. blackbox/sessions/에서 최근 3일간 작업 확인
2. blackbox/incidents/에서 비슷한 문제 검색
3. blackbox/decisions/에서 관련 의사결정 확인
4. 이를 바탕으로 현재 작업에 적용
"""
```

---

## ⚠️ 주의사항

- 이 폴더의 JSON 파일은 **AI가 읽기 위한 용도**입니다
- 사람이 읽을 문서는 `universal-devkit/reflections/` 또는 `universal-devkit/case-studies/` 사용
- 민감 정보 (API 키, 비밀번호) 절대 기록 금지

