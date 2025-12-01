# 🔑 API 키 발급 가이드

Stock Predictor는 다음 4가지 API를 사용합니다. 모두 **무료 플랜**으로 개인 프로젝트에 충분합니다.

**총 소요 시간: 약 11분**

---

## 1. Gemini API (Google AI Studio) - 1분

### 📌 용도
- AI 기반 주식 분석 리포트 생성
- 뉴스, 재무제표, 기술적 분석을 종합하여 AI 의견 제공

### 📊 무료 할당량
- **분당**: 15회
- **하루**: 1,500회
- **월**: 무제한 (Rate Limit 내)

→ 개인 프로젝트에 충분함

### 🔗 발급 방법

1. **Google AI Studio 접속**
   - https://aistudio.google.com/app/apikey

2. **Google 계정 로그인**
   - Gmail 계정 사용

3. **API Key 생성**
   - "Create API Key" 버튼 클릭
   - 프로젝트 선택 (없으면 자동 생성됨)

4. **API Key 복사**
   - 생성된 키를 복사 (예: `AIzaSyC1234567890abcdefg...`)

5. **`.env` 파일에 입력**
   ```bash
   GEMINI_API_KEY=AIzaSyC1234567890abcdefg...
   ```

### ⚠️ 주의사항
- API 키는 절대 Git에 커밋하지 말 것!
- `.gitignore`에 `.env`가 포함되어 있는지 확인

---

## 2. KIS API (한국투자증권) - 5분

### 📌 용도
- 실시간 주가 조회
- 호가 정보
- 투자자별 매매 동향 (외국인/기관)
- 코스피/나스닥 지수

### 📊 무료 할당량
- **모의투자 계좌**: 무료, 무제한
- **실전 계좌**: 월 300만 건 (충분함)

→ 모의투자 계좌 권장

### 🔗 발급 방법

1. **한국투자증권 API 포털 접속**
   - https://apiportal.koreainvestment.com

2. **회원가입 및 로그인**
   - 일반 회원가입 (증권 계좌 없어도 가능)

3. **모의투자 신청**
   - 상단 메뉴: "모의투자신청"
   - "모의투자 신청하기" 클릭
   - 약관 동의 후 신청

4. **앱 등록**
   - 상단 메뉴: "MY API"
   - "앱 등록" 버튼 클릭
   - 앱 이름: `Stock Predictor` (자유)
   - 앱 설명: 주식 분석 프로그램

5. **API Key 복사**
   - `APP Key` 복사
   - `APP Secret` 복사

6. **`.env` 파일에 입력**
   ```bash
   KIS_APP_KEY=your-kis-app-key
   KIS_APP_SECRET=your-kis-app-secret
   ```

### ⚠️ 주의사항
- **모의투자 계좌**를 발급받아야 함 (실전 계좌 X)
- APP Key와 APP Secret 모두 필요
- 실전 투자 기능은 사용하지 않음 (데이터 조회만)

---

## 3. YouTube Data API v3 - 3분

### 📌 용도
- 증권 전문가 유튜브 영상 조회
- 영상 자막 분석 (종목 언급 추출)

### 📊 무료 할당량
- **하루**: 10,000 단위
- 영상 1개 조회: 약 3단위
- **하루 약 3,000개 영상 조회 가능**

→ 개인 프로젝트에 충분함

### 🔗 발급 방법

1. **Google Cloud Console 접속**
   - https://console.cloud.google.com/

2. **프로젝트 생성**
   - 상단 프로젝트 선택 → "새 프로젝트"
   - 프로젝트 이름: `Stock Predictor` (자유)

3. **YouTube Data API v3 활성화**
   - 검색창에 "YouTube Data API v3" 검색
   - "사용" 버튼 클릭

4. **API 키 생성**
   - 좌측 메뉴: "사용자 인증 정보"
   - "사용자 인증 정보 만들기" → "API 키"
   - 키 생성 완료

5. **API 키 제한 (선택, 권장)**
   - 생성된 키 옆 편집 버튼
   - "API 제한사항" → "키 제한"
   - "YouTube Data API v3" 선택
   - 저장

6. **`.env` 파일에 입력**
   ```bash
   YOUTUBE_API_KEY=AIzaSyD9876543210...
   ```

### ⚠️ 주의사항
- Gemini API 키와는 다른 키입니다!
- API 제한을 걸어두면 보안에 더 안전함

---

## 4. Reddit API - 2분

### 📌 용도
- r/stocks, r/investing 등 커뮤니티 게시물 분석
- 시장 센티멘트 파악

### 📊 무료 할당량
- **분당**: 60회
- **하루**: 무제한 (Rate Limit 내)

→ 개인 프로젝트에 충분함

### 🔗 발급 방법

1. **Reddit 앱 등록 페이지 접속**
   - https://www.reddit.com/prefs/apps

2. **Reddit 계정 로그인**
   - 계정이 없으면 회원가입

3. **앱 생성**
   - 하단 "create another app" 또는 "are you a developer? create an app" 클릭
   
   **입력 정보:**
   - **name**: `Stock Predictor` (자유)
   - **App type**: **script** ⚠️ 중요! (installed app X)
   - **description**: Stock analysis tool (자유)
   - **about url**: (비워도 됨)
   - **redirect uri**: `http://localhost:8000` (필수, 아무 값이나)

4. **API 키 확인**
   - 생성된 앱 아래:
     - **Client ID**: 앱 이름 아래 작은 글씨 (14자리)
     - **Client Secret**: "secret" 옆 값

5. **`.env` 파일에 입력**
   ```bash
   REDDIT_CLIENT_ID=abc123def456...
   REDDIT_CLIENT_SECRET=xyz789uvw456...
   ```

### ⚠️ 주의사항
- **App type은 반드시 "script"** 선택!
- "web app" 또는 "installed app" 선택 시 작동하지 않음
- Client ID는 짧고 (14자), Secret은 긺 (27자)

---

## ✅ 전체 체크리스트

발급 완료 후 `.env` 파일 확인:

```bash
# 1. Gemini API
GEMINI_API_KEY=AIzaSyC1234567890abcdefg...

# 2. KIS API
KIS_APP_KEY=your-kis-app-key
KIS_APP_SECRET=your-kis-app-secret

# 3. YouTube API
YOUTUBE_API_KEY=AIzaSyD9876543210...

# 4. Reddit API
REDDIT_CLIENT_ID=abc123def456...
REDDIT_CLIENT_SECRET=xyz789uvw456...
```

### 검증 방법

```bash
# Backend로 이동
cd stock-predictor-backend

# 환경 확인 스크립트 실행
source venv/bin/activate  # Windows: venv\Scripts\activate
python -c "from core.config import settings; print('✅ 환경 변수 로드 성공')"
```

에러 없이 "✅ 환경 변수 로드 성공" 메시지가 나오면 완료!

---

## 🆘 문제 해결

### Gemini API: "API key not valid"
- 키를 다시 복사했는지 확인
- 공백이 포함되지 않았는지 확인
- Google Cloud Console에서 "Generative Language API" 활성화 확인

### KIS API: "인증 실패"
- 모의투자 계좌를 발급받았는지 확인
- APP Key와 APP Secret 순서가 바뀌지 않았는지 확인

### YouTube API: "The request cannot be completed"
- Google Cloud Console에서 YouTube Data API v3가 활성화되었는지 확인
- 프로젝트가 올바르게 선택되었는지 확인

### Reddit API: "invalid_client"
- App type이 "script"인지 확인
- Client ID와 Secret이 바뀌지 않았는지 확인

---

## 📚 추가 자료

- [Gemini API 공식 문서](https://ai.google.dev/docs)
- [KIS API 가이드](https://apiportal.koreainvestment.com/apiservice/oauth2)
- [YouTube Data API 문서](https://developers.google.com/youtube/v3)
- [Reddit API 문서](https://www.reddit.com/dev/api)

---

**🎉 모든 API 키 발급 완료!**

이제 [README.md](../README.md)로 돌아가서 실행 단계를 진행하세요.

