import React, { useState } from 'react';
import ScoreCard from './ScoreCard';

export default function AnalysisResult({ analysis, onGenerateImage }) {
  const [showCoachGuide, setShowCoachGuide] = useState(false);
  const [editedPrompt, setEditedPrompt] = useState(analysis.expert_prompt);

  const getTotalScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getTotalScoreLabel = (score) => {
    if (score >= 85) return '훌륭해요!';
    if (score >= 70) return '좋아요!';
    if (score >= 50) return '괜찮아요';
    return '개선 필요';
  };

  return (
    <div className="w-full max-w-6xl mx-auto space-y-6">
      {/* Overall Score */}
      <div className="bg-white rounded-xl shadow-lg p-8 text-center">
        <h2 className="text-2xl font-bold mb-4">구도 분석 결과</h2>
        <div className={`text-8xl font-bold mb-2 ${getTotalScoreColor(analysis.total_score)}`}>
          {analysis.total_score.toFixed(1)}
        </div>
        <div className="text-xl text-gray-600 mb-2">
          {getTotalScoreLabel(analysis.total_score)}
        </div>
        <div className="inline-block px-4 py-2 bg-gray-100 rounded-full text-sm text-gray-600">
          장르: {analysis.genre === 'portrait' ? '인물' : analysis.genre === 'landscape' ? '풍경' : '제품'}
        </div>
      </div>

      {/* Individual Rule Scores */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {analysis.rules.map((rule, index) => (
          <ScoreCard
            key={index}
            score={rule.score}
            title={rule.name}
            message={rule.message}
            suggestion={rule.suggestion}
          />
        ))}
      </div>

      {/* Coach Guide */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <button
          onClick={() => setShowCoachGuide(!showCoachGuide)}
          className="w-full flex items-center justify-between text-left"
        >
          <h3 className="text-xl font-bold text-gray-800">
            📚 구도 코치 가이드
          </h3>
          <span className="text-2xl">
            {showCoachGuide ? '▼' : '▶'}
          </span>
        </button>

        {showCoachGuide && (
          <div className="mt-4 prose prose-sm max-w-none">
            <div className="whitespace-pre-line text-gray-700">
              {analysis.coach_guide}
            </div>
          </div>
        )}
      </div>

      {/* Expert Prompt */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">
          🤖 AI 보정 프롬프트
        </h3>
        <p className="text-sm text-gray-600 mb-3">
          아래 프롬프트를 수정하여 원하는 스타일로 커스터마이즈할 수 있습니다.
        </p>
        <textarea
          value={editedPrompt}
          onChange={(e) => setEditedPrompt(e.target.value)}
          className="w-full h-40 p-4 border-2 border-gray-200 rounded-lg focus:border-primary-500 focus:outline-none font-mono text-sm"
        />
        <button
          onClick={() => onGenerateImage(editedPrompt)}
          className="mt-4 w-full bg-primary-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-primary-700 transition-colors duration-200"
        >
          ✨ 나노 바나나로 이미지 생성하기
        </button>
      </div>
    </div>
  );
}
