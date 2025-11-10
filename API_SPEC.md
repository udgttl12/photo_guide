# 📘 Photo Guide API 명세서

**Version:** 1.0.0
**Base URL:** `http://localhost:8000/api/v1`
**Protocol:** HTTP/HTTPS

---

## 📋 목차

1. [개요](#개요)
2. [인증](#인증)
3. [에러 처리](#에러-처리)
4. [API 엔드포인트](#api-엔드포인트)
   - [구도 분석](#1-구도-분석-api)
   - [나노 바나나 생성](#2-나노-바나나-이미지-생성-api)
   - [헬스 체크](#3-헬스-체크)
5. [데이터 모델](#데이터-모델)
6. [예제 코드](#예제-코드)

---

## 개요

Photo Guide API는 AI 기반 사진 구도 분석 및 개선 제안 서비스를 제공합니다.

### 주요 기능
- 사진 구도 자동 분석 (Rule of Thirds, Horizon, Exposure, Sharpness)
- 장르별 맞춤 평가 (인물, 풍경, 제품)
- AI 기반 개선 제안 (Google Gemini API)
- 초보자를 위한 구도 코치 가이드

### 기술 스택
- **Framework:** FastAPI
- **Image Processing:** OpenCV
- **AI:** Google Gemini 2.0 Flash
- **Validation:** Pydantic

---

## 인증

현재 MVP 버전에서는 인증이 필요하지 않습니다. 추후 API 키 기반 인증이 추가될 예정입니다.

---

## 에러 처리

### 표준 에러 응답 형식

```json
{
  "detail": "에러 메시지"
}
```

### HTTP 상태 코드

| 코드 | 의미 | 설명 |
|------|------|------|
| 200 | OK | 요청 성공 |
| 400 | Bad Request | 잘못된 요청 (파일 형식, 파라미터 등) |
| 422 | Unprocessable Entity | 요청 형식은 맞지만 처리 불가 (Validation 오류) |
| 500 | Internal Server Error | 서버 내부 오류 |

### 일반적인 에러 케이스

```json
// 파일 형식 오류
{
  "detail": "File must be an image"
}

// 파일 크기 초과
{
  "detail": "File too large. Max size: 10MB"
}

// 이미지 로드 실패
{
  "detail": "Failed to load image: /path/to/file.jpg"
}

// 분석 실패
{
  "detail": "Analysis failed: [상세 오류 메시지]"
}
```

---

## API 엔드포인트

### 1. 구도 분석 API

사진의 구도를 분석하고 점수와 개선 제안을 제공합니다.

#### 기본 정보

```
POST /api/v1/analyze-composition
Content-Type: multipart/form-data
```

#### 요청 파라미터

| 파라미터 | 타입 | 필수 | 설명 | 기본값 |
|---------|------|------|------|--------|
| file | File | ✅ | 분석할 이미지 파일 (JPG, PNG, WEBP) | - |
| genre | String | ✅ | 사진 장르 (`portrait`, `landscape`, `product`) | `portrait` |

#### 파일 제한사항

- **최대 크기:** 10MB
- **지원 형식:** `.jpg`, `.jpeg`, `.png`, `.webp`
- **권장 해상도:** 1000×1000px 이상

#### 응답 (200 OK)

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
    {
      "name": "Horizon Level",
      "score": 95.0,
      "message": "Horizon is perfectly level",
      "suggestion": "Great job keeping the horizon straight"
    },
    {
      "name": "Exposure",
      "score": 72.3,
      "message": "Exposure issues detected: minor shadow clipping",
      "suggestion": "Increase exposure or lift shadows"
    },
    {
      "name": "Sharpness",
      "score": 68.9,
      "message": "Image sharpness is moderate",
      "suggestion": "Consider using faster shutter speed or better focus"
    }
  ],
  "coach_guide": "👍 Good job! Your photo has solid composition with room for minor improvements.\n\n💡 **Exposure - Shadows**: Your shadows are too dark (clipping). Try increasing exposure or using fill light to reveal more detail in dark areas.\n\n🔍 **Sharpness**: Your image appears soft or blurry. Make sure to:\n  - Focus carefully on your subject\n  - Use a faster shutter speed (1/focal_length minimum)\n  - Hold the camera steady or use a tripod\n  - Check if your lens is clean",
  "expert_prompt": "Improve this portrait photograph with the following adjustments:\n\n- lift shadows and recover detail in dark areas\n- enhance sharpness and clarity, add micro-contrast to bring out details\n- ensure flattering skin tones and natural colors\n- optimize lighting on face with proper catchlights in eyes\n\nMaintain natural, photographic quality. Avoid over-processing. Target style: professional portrait photography.",
  "metadata": {
    "file_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "filename": "my_photo.jpg",
    "image_size": {
      "width": 4000,
      "height": 3000
    },
    "weights": {
      "rule_of_thirds": 0.35,
      "horizon": 0.1,
      "exposure": 0.35,
      "sharpness": 0.2
    },
    "raw_results": {
      "rule_of_thirds": {
        "power_points": [[1333, 1000], [2667, 1000], [1333, 2000], [2667, 2000]],
        "interest_scores": [0.145, 0.238, 0.167, 0.189]
      },
      "horizon": {
        "angle": 0.5,
        "has_horizon": true,
        "line_count": 3
      },
      "exposure": {
        "mean_brightness": 118.3,
        "dynamic_range": 45.2,
        "shadow_clipping": 9.23,
        "highlight_clipping": 2.15
      },
      "sharpness": {
        "laplacian_variance": 342.67,
        "normalized_variance": 285.56,
        "quality": "moderate"
      }
    }
  }
}
```

#### 장르별 분석 차이

**Portrait (인물)**
- Rule of Thirds: 35% 가중치
- Exposure: 35% 가중치
- Sharpness: 20% 가중치
- Horizon: 10% 가중치

**Landscape (풍경)**
- Horizon: 35% 가중치
- Rule of Thirds: 30% 가중치
- Exposure: 25% 가중치
- Sharpness: 10% 가중치

**Product (제품)**
- Sharpness: 40% 가중치
- Exposure: 35% 가중치
- Rule of Thirds: 20% 가중치
- Horizon: 5% 가중치

#### cURL 예제

```bash
curl -X POST "http://localhost:8000/api/v1/analyze-composition" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/photo.jpg" \
  -F "genre=portrait"
```

#### Python 예제

```python
import requests

url = "http://localhost:8000/api/v1/analyze-composition"
files = {"file": open("photo.jpg", "rb")}
data = {"genre": "landscape"}

response = requests.post(url, files=files, data=data)
result = response.json()

print(f"Total Score: {result['total_score']}")
for rule in result['rules']:
    print(f"{rule['name']}: {rule['score']} - {rule['message']}")
```

---

### 2. 나노 바나나 이미지 생성 API

Google Gemini API를 사용하여 이미지 개선 제안을 생성합니다.

#### 기본 정보

```
POST /api/v1/generate-nanobanana
Content-Type: multipart/form-data
```

#### 요청 파라미터

| 파라미터 | 타입 | 필수 | 설명 | 기본값 |
|---------|------|------|------|--------|
| file | File | ✅ | 원본 이미지 파일 | - |
| prompt | String | ✅ | 개선 지시사항 (보통 analyze API의 expert_prompt 사용) | - |
| style | String | ❌ | 스타일 프리셋 (`natural`, `vivid`, `dramatic`) | `natural` |
| strength | Float | ❌ | 수정 강도 (0.0 ~ 1.0) | `0.7` |

#### 스타일 프리셋

**natural (자연스러운)**
- 미묘한 개선, 자연스러운 사진 느낌 유지
- 일상 사진, SNS 업로드용 추천

**vivid (선명한)**
- 색상 및 대비 강화
- 여행 사진, 풍경 사진 추천

**dramatic (드라마틱)**
- 극적인 조명 및 톤
- 예술 사진, 무드 있는 작품용 추천

#### 수정 강도

| 값 | 설명 |
|----|------|
| 0.1 - 0.3 | 매우 미묘한 변화 (거의 눈에 띄지 않음) |
| 0.4 - 0.6 | 보통 수준 변화 (균형잡힌 개선) |
| 0.7 - 0.8 | 명확한 변화 (자연스러움 유지) |
| 0.9 - 1.0 | 강력한 변화 (확실한 개선) |

#### 응답 (200 OK)

```json
{
  "success": true,
  "image_url": "/outputs/a1b2c3d4-e5f6-7890-abcd-ef1234567890_output.jpg",
  "metadata": {
    "file_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "original_filename": "my_photo.jpg",
    "style": "natural",
    "strength": 0.7,
    "suggestions": "Based on the analysis, I recommend the following specific adjustments:\n\n1. Exposure: Increase overall exposure by +0.5 EV to brighten shadows\n2. Shadows: Lift shadow slider to +25 to recover detail in dark areas\n3. Sharpness: Apply selective sharpening (Amount: 40, Radius: 1.0, Detail: 25)\n4. Focus: The subject's eyes appear slightly soft - ensure critical focus on the eyes\n5. Color: Warm up skin tones by +5 on temperature slider\n\nThe composition already follows rule of thirds well with the subject positioned at the right power point. The horizon is level at 0.5° which is excellent.",
    "note": "Image generation coming soon - currently showing AI analysis and suggestions"
  }
}
```

**Note:** 현재 MVP에서는 실제 이미지 생성 대신 AI의 상세한 개선 제안을 텍스트로 제공합니다.

#### 응답 (실패 시)

```json
{
  "success": false,
  "image_url": null,
  "error": "Generation failed: API timeout",
  "metadata": {}
}
```

#### cURL 예제

```bash
curl -X POST "http://localhost:8000/api/v1/generate-nanobanana" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/photo.jpg" \
  -F "prompt=Improve exposure and sharpness while maintaining natural look" \
  -F "style=natural" \
  -F "strength=0.7"
```

#### JavaScript (Axios) 예제

```javascript
import axios from 'axios';

const formData = new FormData();
formData.append('file', fileObject);
formData.append('prompt', expertPrompt);
formData.append('style', 'vivid');
formData.append('strength', 0.8);

const response = await axios.post(
  'http://localhost:8000/api/v1/generate-nanobanana',
  formData,
  {
    headers: { 'Content-Type': 'multipart/form-data' }
  }
);

console.log(response.data.suggestions);
```

---

### 3. 헬스 체크

서버 상태를 확인합니다.

#### 기본 정보

```
GET /health
GET /api/v1/health
```

#### 응답 (200 OK)

```json
{
  "status": "healthy"
}
```

#### cURL 예제

```bash
curl -X GET "http://localhost:8000/health"
```

---

## 데이터 모델

### GenreType (Enum)

```python
class GenreType(str, Enum):
    PORTRAIT = "portrait"   # 인물
    LANDSCAPE = "landscape" # 풍경
    PRODUCT = "product"     # 제품
```

### RuleScore (Object)

개별 구도 규칙의 점수와 피드백

```typescript
{
  name: string;        // 규칙 이름
  score: number;       // 점수 (0-100)
  message: string;     // 진단 메시지
  suggestion: string;  // 개선 제안
}
```

### CompositionAnalysis (Object)

전체 구도 분석 결과

```typescript
{
  total_score: number;              // 총점 (0-100)
  genre: "portrait" | "landscape" | "product";
  rules: RuleScore[];               // 규칙별 점수 배열
  coach_guide: string;              // 초보자용 가이드 (마크다운)
  expert_prompt: string;            // AI 보정용 프롬프트
  metadata: {
    file_id: string;
    filename: string;
    image_size: {
      width: number;
      height: number;
    };
    weights: {                      // 장르별 가중치
      rule_of_thirds: number;
      horizon: number;
      exposure: number;
      sharpness: number;
    };
    raw_results: object;            // 원본 분석 데이터
  };
}
```

### GenerateResponse (Object)

이미지 생성 결과

```typescript
{
  success: boolean;
  image_url: string | null;         // 생성된 이미지 URL
  error: string | null;             // 에러 메시지 (실패 시)
  metadata: {
    file_id: string;
    original_filename: string;
    style: string;
    strength: number;
    suggestions: string;            // AI 제안 (텍스트)
    note: string;
  };
}
```

---

## 예제 코드

### 전체 워크플로우 (Python)

```python
import requests
from pathlib import Path

# API Base URL
BASE_URL = "http://localhost:8000/api/v1"

# 1. 사진 업로드 및 구도 분석
def analyze_photo(image_path: str, genre: str = "portrait"):
    url = f"{BASE_URL}/analyze-composition"

    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {'genre': genre}
        response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Analysis failed: {response.json()['detail']}")

# 2. AI 개선 제안 생성
def generate_suggestions(image_path: str, prompt: str, style: str = "natural"):
    url = f"{BASE_URL}/generate-nanobanana"

    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {
            'prompt': prompt,
            'style': style,
            'strength': 0.7
        }
        response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Generation failed: {response.json()['detail']}")

# 사용 예제
if __name__ == "__main__":
    image_path = "my_photo.jpg"

    # Step 1: 구도 분석
    print("📸 Analyzing composition...")
    analysis = analyze_photo(image_path, genre="portrait")

    print(f"📊 Total Score: {analysis['total_score']}/100")
    print(f"🎭 Genre: {analysis['genre']}")
    print("\n📋 Rule Scores:")
    for rule in analysis['rules']:
        print(f"  - {rule['name']}: {rule['score']:.1f}/100")
        print(f"    💬 {rule['message']}")
        print(f"    💡 {rule['suggestion']}\n")

    print("📚 Coach Guide:")
    print(analysis['coach_guide'])

    # Step 2: AI 개선 제안
    print("\n\n🤖 Generating AI suggestions...")
    result = generate_suggestions(
        image_path,
        prompt=analysis['expert_prompt'],
        style="natural"
    )

    if result['success']:
        print("✨ AI Suggestions:")
        print(result['metadata']['suggestions'])
    else:
        print(f"❌ Generation failed: {result['error']}")
```

### React 통합 예제

```javascript
import { useState } from 'react';
import { analyzeComposition, generateNanoBanana } from './services/api';

function PhotoAnalyzer() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const analyzePhoto = async () => {
    if (!file) return;

    setLoading(true);
    try {
      const result = await analyzeComposition(file, 'portrait');
      setAnalysis(result);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateEnhancement = async () => {
    if (!file || !analysis) return;

    setLoading(true);
    try {
      const result = await generateNanoBanana(
        file,
        analysis.expert_prompt,
        'natural',
        0.7
      );
      console.log('Suggestions:', result.metadata.suggestions);
    } catch (error) {
      console.error('Generation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} accept="image/*" />
      <button onClick={analyzePhoto} disabled={!file || loading}>
        Analyze
      </button>

      {analysis && (
        <div>
          <h2>Score: {analysis.total_score}/100</h2>
          <button onClick={generateEnhancement}>
            Get AI Suggestions
          </button>
        </div>
      )}
    </div>
  );
}
```

---

## 제한사항 및 참고사항

### 현재 제한사항
1. **이미지 생성**: MVP에서는 실제 이미지 생성 대신 텍스트 제안 제공
2. **인증**: 현재 인증 미지원 (향후 API 키 추가 예정)
3. **Rate Limiting**: 현재 미적용
4. **배치 처리**: 한 번에 하나의 이미지만 처리 가능

### 권장사항
1. **이미지 품질**: 최소 1000×1000px 이상 권장
2. **파일 형식**: JPEG 또는 PNG 권장 (압축률 균형)
3. **장르 선택**: 정확한 분석을 위해 올바른 장르 선택
4. **프롬프트 수정**: expert_prompt를 커스터마이즈하여 원하는 스타일 지정 가능

### 성능 지표
- **구도 분석 응답 시간**: < 2초 (일반적으로 0.5-1초)
- **AI 생성 응답 시간**: < 30초 (Gemini API 의존)
- **최대 파일 크기**: 10MB
- **동시 처리**: FastAPI의 비동기 처리로 여러 요청 동시 처리 가능

---

## 버전 히스토리

### v1.0.0 (2024-11)
- 초기 MVP 릴리스
- 구도 분석 API (4가지 규칙)
- 장르별 가중치 시스템
- Google Gemini 통합
- OpenAPI/Swagger 문서 자동 생성

---

## 추가 리소스

- **OpenAPI 문서**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc (대안 문서 뷰어)
- **GitHub**: https://github.com/udgttl12/photo_guide
- **기획 문서**: [mvp_spec.md](./mvp_spec.md)

---

## 문의 및 지원

버그 리포트나 기능 제안은 GitHub Issues를 이용해주세요:
https://github.com/udgttl12/photo_guide/issues
