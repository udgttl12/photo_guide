import React from 'react';

export default function ScoreCard({ score, title, message, suggestion }) {
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBg = (score) => {
    if (score >= 80) return 'bg-green-50 border-green-200';
    if (score >= 60) return 'bg-yellow-50 border-yellow-200';
    return 'bg-red-50 border-red-200';
  };

  const getScoreEmoji = (score) => {
    if (score >= 80) return '✅';
    if (score >= 60) return '⚠️';
    return '❌';
  };

  return (
    <div className={`p-4 rounded-lg border-2 ${getScoreBg(score)}`}>
      <div className="flex items-start justify-between mb-2">
        <h4 className="font-semibold text-gray-800">{title}</h4>
        <div className="flex items-center gap-2">
          <span className="text-xl">{getScoreEmoji(score)}</span>
          <span className={`text-2xl font-bold ${getScoreColor(score)}`}>
            {score.toFixed(0)}
          </span>
        </div>
      </div>
      <p className="text-sm text-gray-700 mb-2">{message}</p>
      <p className="text-xs text-gray-600 italic">{suggestion}</p>
    </div>
  );
}
