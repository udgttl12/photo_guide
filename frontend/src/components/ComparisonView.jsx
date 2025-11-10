import React from 'react';
import {
  ReactCompareSlider,
  ReactCompareSliderImage,
} from 'react-compare-slider';

export default function ComparisonView({ originalImage, generatedResult, onReset }) {
  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-6 text-center">
          전/후 비교
        </h2>

        {generatedResult.success ? (
          <div className="space-y-6">
            {generatedResult.image_url ? (
              <div className="rounded-lg overflow-hidden shadow-lg">
                <ReactCompareSlider
                  itemOne={
                    <ReactCompareSliderImage
                      src={originalImage}
                      alt="원본"
                    />
                  }
                  itemTwo={
                    <ReactCompareSliderImage
                      src={generatedResult.image_url}
                      alt="보정됨"
                    />
                  }
                />
              </div>
            ) : (
              <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-6">
                <h3 className="font-semibold text-blue-900 mb-3">
                  AI 분석 결과
                </h3>
                <div className="whitespace-pre-line text-blue-800 text-sm">
                  {generatedResult.suggestions}
                </div>
                {generatedResult.note && (
                  <p className="mt-4 text-xs text-blue-600 italic">
                    {generatedResult.note}
                  </p>
                )}
              </div>
            )}

            <div className="flex gap-4">
              <button
                onClick={onReset}
                className="flex-1 bg-gray-100 text-gray-700 py-3 px-6 rounded-lg font-semibold hover:bg-gray-200 transition-colors duration-200"
              >
                새로운 사진 분석하기
              </button>
              {generatedResult.image_url && (
                <a
                  href={generatedResult.image_url}
                  download="enhanced-photo.jpg"
                  className="flex-1 bg-primary-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-primary-700 transition-colors duration-200 text-center"
                >
                  다운로드
                </a>
              )}
            </div>
          </div>
        ) : (
          <div className="bg-red-50 border-2 border-red-200 rounded-lg p-6">
            <h3 className="font-semibold text-red-900 mb-2">
              오류 발생
            </h3>
            <p className="text-red-700 text-sm">
              {generatedResult.error || '이미지 생성 중 문제가 발생했습니다.'}
            </p>
            <button
              onClick={onReset}
              className="mt-4 bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-700 transition-colors duration-200"
            >
              다시 시도하기
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
