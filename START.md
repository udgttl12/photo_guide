# 🚀 Photo Guide 시작 가이드

Photo Guide를 실행하는 방법을 단계별로 안내합니다.

---

## 📋 목차

1. [사전 준비](#사전-준비)
2. [빠른 시작 (Docker 사용)](#빠른-시작-docker-사용)
3. [로컬 개발 환경 설정](#로컬-개발-환경-설정)
4. [환경 변수 설정](#환경-변수-설정)
5. [실행 확인](#실행-확인)
6. [문제 해결](#문제-해결)

---

## 사전 준비

### 필수 요구사항

#### Option 1: Docker 사용 (권장)
- **Docker Desktop** 또는 Docker Engine 설치
  - Windows/Mac: [Docker Desktop 다운로드](https://www.docker.com/products/docker-desktop/)
  - Linux: [Docker Engine 설치](https://docs.docker.com/engine/install/)
- **Docker Compose** (Docker Desktop에 포함)

#### Option 2: 로컬 개발
- **Python 3.11+** ([다운로드](https://www.python.org/downloads/))
- **Node.js 18+** ([다운로드](https://nodejs.org/))
- **Git** ([다운로드](https://git-scm.com/downloads))

### 선택 사항
- **Google Gemini API Key** (나노 바나나 기능 사용 시)
  - [Google AI Studio](https://aistudio.google.com/app/apikey)에서 무료로 발급 가능

---

## 빠른 시작 (Docker 사용)

가장 쉽고 빠른 방법입니다. Docker만 설치되어 있으면 됩니다.

### 1️⃣ 저장소 클론

```bash
# 터미널(또는 명령 프롬프트) 열기
git clone https://github.com/udgttl12/photo_guide.git
cd photo_guide
```

### 2️⃣ 환경 변수 설정

```bash
# backend 디렉토리로 이동
cd backend

# .env.example을 .env로 복사
cp .env.example .env

# .env 파일 편집 (메모장, VSCode 등으로 열기)
```

`.env` 파일을 열고 다음 내용을 수정:

```env
# Google Gemini API Key (선택사항)
GOOGLE_API_KEY=your_actual_api_key_here

# 나머지는 기본값 사용
ALLOWED_ORIGINS=http://localhost:3000,http://localhost
```

**Google API Key가 없다면?**
- 구도 분석 기능은 정상 작동합니다
- 나노 바나나 생성 기능만 제한됩니다
- 나중에 추가 가능합니다

### 3️⃣ Docker로 실행

```bash
# 프로젝트 루트 디렉토리로 돌아가기
cd ..

# Docker Compose로 빌드 및 실행
docker-compose up --build
```

**처음 실행 시**
- 이미지 빌드에 5-10분 소요 (인터넷 속도에 따라 다름)
- 의존성 다운로드 및 설치가 진행됩니다
- 다음부터는 몇 초만에 실행됩니다

**실행 중 로그 예시:**
```
backend_1   | INFO:     Application startup complete.
backend_1   | INFO:     Uvicorn running on http://0.0.0.0:8000
frontend_1  | Listening on 80
```

### 4️⃣ 브라우저에서 접속

✅ **프론트엔드**: http://localhost
- 사용자 UI가 나타납니다

✅ **백엔드 API 문서**: http://localhost:8000/docs
- Swagger UI에서 API를 테스트할 수 있습니다

### 5️⃣ 종료하기

터미널에서 `Ctrl + C`를 누르거나:

```bash
docker-compose down
```

**컨테이너와 데이터 모두 삭제하려면:**
```bash
docker-compose down -v
```

---

## 로컬 개발 환경 설정

Docker 없이 로컬에서 직접 실행하는 방법입니다. 개발 시 유용합니다.

### 백엔드 설정 (Python)

#### 1️⃣ 저장소 클론 및 이동

```bash
git clone https://github.com/udgttl12/photo_guide.git
cd photo_guide/backend
```

#### 2️⃣ 가상환경 생성

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

가상환경이 활성화되면 터미널에 `(venv)`가 표시됩니다.

#### 3️⃣ 의존성 설치

```bash
pip install -r requirements.txt
```

**설치 시간**: 2-5분 (OpenCV 등 큰 패키지 포함)

#### 4️⃣ 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# 편집기로 .env 열고 Google API Key 입력
```

#### 5️⃣ 서버 실행

```bash
# 개발 모드로 실행 (코드 변경 시 자동 재시작)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**실행 확인:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ 백엔드 준비 완료: http://localhost:8000

---

### 프론트엔드 설정 (React)

#### 1️⃣ 새 터미널 열기

백엔드를 실행한 터미널은 그대로 두고, 새 터미널을 엽니다.

```bash
cd photo_guide/frontend
```

#### 2️⃣ 의존성 설치

```bash
npm install
```

**설치 시간**: 1-3분

#### 3️⃣ 개발 서버 실행

```bash
npm run dev
```

**실행 확인:**
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

✅ 프론트엔드 준비 완료: http://localhost:3000

---

## 환경 변수 설정

### backend/.env 파일 상세 설명

```env
# ============================================
# Google Gemini API 설정
# ============================================
# AI 이미지 분석을 위한 API 키
# 발급 방법: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY=your_api_key_here

# ============================================
# CORS 설정
# ============================================
# 프론트엔드 접근 허용 URL (쉼표로 구분)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost

# ============================================
# 애플리케이션 설정
# ============================================
APP_NAME=Photo Guide API
APP_VERSION=1.0.0
API_PREFIX=/api/v1

# ============================================
# 파일 업로드 설정
# ============================================
# 최대 업로드 크기 (바이트 단위, 10MB)
MAX_UPLOAD_SIZE=10485760

# 업로드 및 출력 디렉토리
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs

# ============================================
# Gemini 모델 설정
# ============================================
# 사용할 Gemini 모델
GEMINI_MODEL=gemini-2.0-flash-exp

# ============================================
# 타임아웃 설정
# ============================================
# 구도 분석 타임아웃 (초)
ANALYSIS_TIMEOUT=5

# 이미지 생성 타임아웃 (초)
GENERATION_TIMEOUT=30
```

### Google API Key 발급 방법

1. [Google AI Studio](https://aistudio.google.com/app/apikey) 접속
2. Google 계정으로 로그인
3. "Get API Key" 클릭
4. "Create API Key" 선택
5. 생성된 키를 복사하여 `.env` 파일에 붙여넣기

**무료 사용량:**
- Gemini 2.0 Flash: 분당 15회 요청
- 일일 1,500회 요청 제한
- 개발 및 테스트에 충분합니다

---

## 실행 확인

### ✅ 체크리스트

#### 백엔드 확인

1. **헬스 체크**
   ```bash
   curl http://localhost:8000/health
   ```

   응답:
   ```json
   {"status": "healthy"}
   ```

2. **API 문서 접속**
   - 브라우저에서 http://localhost:8000/docs 열기
   - Swagger UI가 표시되어야 합니다

3. **테스트 이미지 분석**
   - Swagger UI에서 `/api/v1/analyze-composition` 엔드포인트 선택
   - "Try it out" 클릭
   - 이미지 파일 업로드 및 장르 선택
   - "Execute" 클릭
   - 200 응답과 분석 결과 확인

#### 프론트엔드 확인

1. **페이지 로드**
   - http://localhost:3000 (로컬 개발) 또는 http://localhost (Docker) 접속
   - "Photo Guide" 제목과 업로드 영역이 보여야 합니다

2. **이미지 업로드**
   - 사진 파일을 드래그 앤 드롭하거나 클릭하여 선택
   - 미리보기가 표시되어야 합니다

3. **장르 선택**
   - 인물/풍경/제품 버튼이 정상 작동해야 합니다

4. **분석 실행**
   - "구도 분석 시작" 버튼 클릭
   - 분석 결과와 점수가 표시되어야 합니다

---

## 문제 해결

### Docker 관련 문제

#### ❌ "Cannot connect to the Docker daemon"

**원인**: Docker가 실행되지 않음

**해결방법:**
- Windows/Mac: Docker Desktop 실행
- Linux: `sudo systemctl start docker`

#### ❌ "port is already allocated"

**원인**: 포트가 이미 사용 중

**해결방법:**
```bash
# 포트 사용 프로세스 확인
# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :80

# Mac/Linux
lsof -i :8000
lsof -i :80

# 프로세스 종료 또는 docker-compose.yml에서 포트 변경
```

**포트 변경 방법** (`docker-compose.yml`):
```yaml
services:
  backend:
    ports:
      - "8001:8000"  # 8000 대신 8001 사용

  frontend:
    ports:
      - "3001:80"    # 80 대신 3001 사용
```

#### ❌ "failed to build"

**원인**: 네트워크 문제 또는 디스크 공간 부족

**해결방법:**
```bash
# 캐시 없이 재빌드
docker-compose build --no-cache

# 오래된 이미지 정리
docker system prune -a
```

---

### 백엔드 관련 문제

#### ❌ "ModuleNotFoundError: No module named 'cv2'"

**원인**: OpenCV 설치 실패

**해결방법:**
```bash
# 가상환경이 활성화된 상태에서
pip install opencv-python opencv-contrib-python
```

#### ❌ "GOOGLE_API_KEY not configured"

**원인**: 환경 변수 미설정

**해결방법:**
1. `backend/.env` 파일 존재 확인
2. `GOOGLE_API_KEY=` 값 확인
3. 서버 재시작

#### ❌ "Failed to load image"

**원인**: 업로드된 파일 권한 또는 형식 문제

**해결방법:**
```bash
# uploads 디렉토리 권한 확인
cd backend
mkdir -p uploads outputs
chmod 755 uploads outputs

# 지원 형식: JPG, PNG, WEBP
```

---

### 프론트엔드 관련 문제

#### ❌ "npm ERR! ENOENT"

**원인**: package.json 파일 없음 또는 경로 오류

**해결방법:**
```bash
# 올바른 디렉토리 확인
cd photo_guide/frontend
ls package.json  # 파일이 보여야 함

# 재설치
rm -rf node_modules package-lock.json
npm install
```

#### ❌ "Network Error" 또는 CORS 오류

**원인**: 백엔드 서버가 실행되지 않거나 CORS 설정 문제

**해결방법:**
1. 백엔드 서버 실행 확인: http://localhost:8000/health
2. `backend/.env`의 `ALLOWED_ORIGINS` 확인:
   ```env
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
   ```
3. 백엔드 재시작

#### ❌ Vite 개발 서버가 시작되지 않음

**원인**: Node.js 버전 문제

**해결방법:**
```bash
# Node.js 버전 확인 (18+ 필요)
node --version

# 버전이 낮으면 업데이트
# https://nodejs.org/ 에서 최신 LTS 버전 다운로드
```

---

### 일반적인 문제

#### ❌ 이미지 분석이 느림 (> 5초)

**원인**: 대용량 이미지 또는 시스템 리소스 부족

**해결방법:**
- 이미지 크기 축소 (권장: 1000×1000px ~ 4000×4000px)
- 파일 크기 압축 (권장: < 5MB)
- 다른 프로그램 종료하여 메모리 확보

#### ❌ 나노 바나나 생성이 실패

**원인**: Google API Key 문제 또는 API 할당량 초과

**해결방법:**
1. API Key 유효성 확인
2. [Google AI Studio](https://aistudio.google.com/)에서 할당량 확인
3. 무료 할당량: 분당 15회, 일일 1,500회

#### ❌ 브라우저 콘솔에 에러 표시

**해결방법:**
```bash
# 브라우저 개발자 도구 열기 (F12)
# Console 탭에서 에러 메시지 확인

# 일반적인 해결책:
1. 브라우저 캐시 삭제 (Ctrl + Shift + Delete)
2. 하드 새로고침 (Ctrl + Shift + R)
3. 시크릿/프라이빗 모드에서 테스트
```

---

## 추가 명령어

### Docker 관련

```bash
# 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f backend   # 백엔드 로그
docker-compose logs -f frontend  # 프론트엔드 로그

# 컨테이너 재시작
docker-compose restart

# 특정 서비스만 재시작
docker-compose restart backend

# 백그라운드 실행
docker-compose up -d

# 모든 컨테이너 및 볼륨 삭제
docker-compose down -v
```

### 개발 환경 관련

```bash
# 백엔드: 가상환경 비활성화
deactivate

# 백엔드: 의존성 업데이트
pip install --upgrade -r requirements.txt

# 프론트엔드: 빌드 (프로덕션)
npm run build

# 프론트엔드: 빌드 미리보기
npm run preview
```

---

## 다음 단계

### 1. 첫 사진 분석하기
- 샘플 이미지로 테스트
- 다양한 장르 (인물/풍경/제품) 시도
- 점수와 피드백 확인

### 2. API 탐색하기
- http://localhost:8000/docs 에서 Swagger UI 탐색
- 각 엔드포인트 직접 테스트
- API_SPEC.md 문서 읽기

### 3. 코드 커스터마이징
- 가중치 조정: `backend/app/core/composition/analyzer.py`
- UI 스타일: `frontend/src/index.css`
- 새로운 구도 규칙 추가

### 4. 배포 준비
- Docker로 프로덕션 빌드
- 환경 변수 보안 강화
- Cloud Run, AWS, Azure 등에 배포

---

## 도움말 및 지원

### 문서
- **프로젝트 개요**: [README.md](./README.md)
- **API 명세서**: [API_SPEC.md](./API_SPEC.md)
- **기획 문서**: [mvp_spec.md](./mvp_spec.md)

### 온라인 리소스
- **GitHub Issues**: https://github.com/udgttl12/photo_guide/issues
- **FastAPI 문서**: https://fastapi.tiangolo.com/
- **React 문서**: https://react.dev/
- **Docker 문서**: https://docs.docker.com/

### 커뮤니티
- 버그를 발견하셨나요? GitHub Issue로 리포트해주세요
- 기능 제안이 있으신가요? Discussion을 열어주세요
- 기여하고 싶으신가요? Pull Request를 보내주세요

---

**🎉 설정 완료! 이제 Photo Guide를 사용할 준비가 되었습니다!**
