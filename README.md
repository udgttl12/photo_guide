# 📸 Photo Guide - AI 사진 구도 피드백 서비스

Gemini 2.0 Flash (나노 바나나)를 이용한 지능형 사진 구도 분석 및 보정 제안 서비스

## 🎯 프로젝트 개요

Photo Guide는 사진 입문자와 취미 사진가들을 위한 AI 기반 구도 피드백 서비스입니다. OpenCV를 활용한 구도 분석과 Google Gemini API를 통한 AI 보정 제안을 제공합니다.

### 주요 기능

- ✅ **구도 분석**: 룰 오브 서즈, 수평선, 노출, 선명도 분석
- 🎨 **장르별 평가**: 인물, 풍경, 제품 사진에 최적화된 가중치 적용
- 📚 **구도 코치**: 초보자를 위한 쉬운 설명과 개선 제안
- 🤖 **AI 보정 프롬프트**: Gemini API를 활용한 전문가급 개선 가이드
- 🔄 **전/후 비교**: 원본과 개선 제안의 시각적 비교

## 🏗️ 기술 스택

### 백엔드
- **FastAPI**: 고성능 Python 웹 프레임워크
- **OpenCV**: 이미지 처리 및 구도 분석
- **Google Gemini API**: AI 기반 이미지 분석 및 개선 제안
- **Pydantic**: 데이터 검증 및 설정 관리

### 프론트엔드
- **React**: 사용자 인터페이스
- **Vite**: 빠른 개발 환경
- **Tailwind CSS**: 유틸리티 기반 스타일링
- **React Dropzone**: 드래그 앤 드롭 파일 업로드
- **React Compare Slider**: 전/후 이미지 비교

### 배포
- **Docker**: 컨테이너화
- **Docker Compose**: 멀티 컨테이너 오케스트레이션

## 📁 프로젝트 구조

```
photo_guide/
├── backend/
│   ├── app/
│   │   ├── api/                 # API 엔드포인트
│   │   │   ├── analyze.py       # 구도 분석 API
│   │   │   └── generate.py      # 이미지 생성 API
│   │   ├── core/
│   │   │   ├── config.py        # 설정
│   │   │   └── composition/     # 구도 분석 모듈
│   │   │       ├── analyzer.py  # 통합 분석기
│   │   │       ├── rule_of_thirds.py
│   │   │       ├── horizon.py
│   │   │       ├── exposure.py
│   │   │       └── sharpness.py
│   │   ├── services/
│   │   │   └── gemini_client.py # Gemini API 클라이언트
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic 모델
│   │   └── main.py              # FastAPI 앱
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/          # React 컴포넌트
│   │   │   ├── Upload.jsx
│   │   │   ├── AnalysisResult.jsx
│   │   │   ├── ScoreCard.jsx
│   │   │   └── ComparisonView.jsx
│   │   ├── services/
│   │   │   └── api.js           # API 클라이언트
│   │   └── App.jsx
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
└── mvp_spec.md                  # 기획 문서
```

## 🚀 시작하기

### 사전 요구사항

- Docker & Docker Compose
- Google Gemini API Key

### 설치 및 실행

1. **저장소 클론**
```bash
git clone https://github.com/udgttl12/photo_guide.git
cd photo_guide
```

2. **환경 변수 설정**
```bash
# backend/.env 파일 생성
cd backend
cp .env.example .env
```

`.env` 파일을 열고 Google API Key를 설정:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

3. **Docker Compose로 실행**
```bash
# 프로젝트 루트 디렉토리에서
docker-compose up --build
```

4. **브라우저에서 접속**
- 프론트엔드: http://localhost
- 백엔드 API 문서: http://localhost:8000/docs

### 로컬 개발 환경 (Docker 없이)

#### 백엔드
```bash
cd backend

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일에 GOOGLE_API_KEY 설정

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

#### 프론트엔드
```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

## 📖 API 문서

### 구도 분석 API

**POST** `/api/v1/analyze-composition`

사진 구도를 분석하고 점수와 피드백을 제공합니다.

**Request:**
- `file`: 이미지 파일 (multipart/form-data)
- `genre`: 장르 선택 (portrait | landscape | product)

**Response:**
```json
{
  "total_score": 78.5,
  "genre": "portrait",
  "rules": [
    {
      "name": "Rule of Thirds",
      "score": 85.0,
      "message": "Good use of Rule of Thirds",
      "suggestion": "Consider positioning key elements closer to power points"
    },
    ...
  ],
  "coach_guide": "초보자를 위한 구도 설명...",
  "expert_prompt": "AI 보정을 위한 전문가 프롬프트...",
  "metadata": {...}
}
```

### 나노 바나나 생성 API

**POST** `/api/v1/generate-nanobanana`

Gemini API를 사용하여 이미지 개선 제안을 생성합니다.

**Request:**
- `file`: 원본 이미지 파일
- `prompt`: 개선 지시사항
- `style`: 스타일 (natural | vivid | dramatic)
- `strength`: 수정 강도 (0.0 - 1.0)

**Response:**
```json
{
  "success": true,
  "suggestions": "AI의 개선 제안...",
  "note": "상세 설명",
  "metadata": {...}
}
```

## 🔍 구도 분석 알고리즘

### 1. Rule of Thirds (룰 오브 서즈)
- 이미지를 3×3 그리드로 분할
- 4개의 교차점(power points) 주변의 관심 영역 감지
- Canny Edge Detection으로 주요 요소 위치 분석

### 2. Horizon Analysis (수평선 분석)
- Hough Line Transform으로 직선 검출
- 수평선 기울기 측정 (±30도 이내)
- 1도 미만: 완벽, 2도 이상: 개선 필요

### 3. Exposure Analysis (노출 분석)
- 히스토그램 분석
- Shadow clipping (0-10 범위)
- Highlight clipping (245-255 범위)
- Dynamic range 평가

### 4. Sharpness Analysis (선명도 분석)
- Laplacian variance 계산
- 이미지 크기로 정규화
- 500+ : 매우 선명, 100-500: 양호, <100: 흐림

### 장르별 가중치

| 규칙 | 인물 | 풍경 | 제품 |
|------|------|------|------|
| Rule of Thirds | 35% | 30% | 20% |
| Horizon | 10% | 35% | 5% |
| Exposure | 35% | 25% | 35% |
| Sharpness | 20% | 10% | 40% |

## 🎨 사용자 플로우

1. **사진 업로드**: 드래그 앤 드롭 또는 클릭하여 이미지 업로드
2. **장르 선택**: 인물, 풍경, 제품 중 선택
3. **분석 실행**: AI가 구도를 분석하고 점수 산출
4. **결과 확인**:
   - 총점 및 규칙별 점수
   - 구도 코치 가이드 (초보자용)
   - AI 보정 프롬프트 (수정 가능)
5. **나노 바나나 생성**: Gemini로 개선 제안 받기
6. **비교 확인**: 전/후 슬라이더로 비교

## 🛠️ 개발 로드맵

### ✅ MVP (완료)
- [x] 기본 구도 분석 (룰 오브 서즈, 수평선, 노출, 선명도)
- [x] 장르별 가중치 시스템
- [x] FastAPI 백엔드
- [x] React 프론트엔드
- [x] Gemini API 연동
- [x] Docker 컨테이너화

### 🔄 향후 개선 사항
- [ ] 실제 이미지 생성 (현재는 텍스트 제안만 제공)
- [ ] 헤드룸/룩룸 분석 (인물 사진)
- [ ] 색상 이론 분석
- [ ] 사용자 히스토리 저장
- [ ] 배치 처리 (여러 이미지 동시 분석)
- [ ] 커스텀 규칙 추가 기능
- [ ] 소셜 공유 기능
- [ ] 모바일 앱 개발

## 🤝 기여하기

버그 리포트, 기능 제안, 풀 리퀘스트를 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 👥 만든 사람

- GitHub: [@udgttl12](https://github.com/udgttl12)

## 🙏 감사의 말

- [OpenCV](https://opencv.org/) - 컴퓨터 비전 라이브러리
- [Google Gemini](https://deepmind.google/technologies/gemini/) - AI 이미지 분석
- [FastAPI](https://fastapi.tiangolo.com/) - 웹 프레임워크
- [React](https://react.dev/) - UI 라이브러리

---

**Note**: 이 프로젝트는 MVP 단계입니다. Gemini API의 이미지 생성 기능은 현재 텍스트 기반 제안을 제공하며, 향후 실제 이미지 생성 기능이 추가될 예정입니다.
