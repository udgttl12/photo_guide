import React, { useState } from 'react';
import Upload from './components/Upload';
import AnalysisResult from './components/AnalysisResult';
import ComparisonView from './components/ComparisonView';
import { analyzeComposition, generateNanoBanana } from './services/api';

function App() {
  const [step, setStep] = useState('upload'); // upload, analysis, comparison
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentFile, setCurrentFile] = useState(null);
  const [originalImage, setOriginalImage] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [generatedResult, setGeneratedResult] = useState(null);

  const handleAnalyze = async (file, genre) => {
    setLoading(true);
    setError(null);
    setCurrentFile(file);

    // Create preview URL
    const reader = new FileReader();
    reader.onload = () => {
      setOriginalImage(reader.result);
    };
    reader.readAsDataURL(file);

    try {
      const result = await analyzeComposition(file, genre);
      setAnalysisResult(result);
      setStep('analysis');
    } catch (err) {
      setError(err.response?.data?.detail || '분석 중 오류가 발생했습니다.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateImage = async (prompt) => {
    setLoading(true);
    setError(null);

    try {
      const result = await generateNanoBanana(currentFile, prompt);
      setGeneratedResult(result);
      setStep('comparison');
    } catch (err) {
      setError(err.response?.data?.detail || '이미지 생성 중 오류가 발생했습니다.');
      console.error('Generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setStep('upload');
    setCurrentFile(null);
    setOriginalImage(null);
    setAnalysisResult(null);
    setGeneratedResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="text-4xl">📸</div>
              <div>
                <h1 className="text-2xl font-bold text-gray-800">
                  Photo Guide
                </h1>
                <p className="text-sm text-gray-600">
                  AI 기반 사진 구도 피드백 서비스
                </p>
              </div>
            </div>
            {step !== 'upload' && (
              <button
                onClick={handleReset}
                className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors duration-200"
              >
                처음으로
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Loading Overlay */}
        {loading && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-8 flex flex-col items-center gap-4">
              <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600"></div>
              <p className="text-lg font-semibold text-gray-700">
                {step === 'upload' ? '사진을 분석하는 중...' : 'AI가 이미지를 생성하는 중...'}
              </p>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="max-w-2xl mx-auto mb-6 bg-red-50 border-2 border-red-200 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <span className="text-2xl">⚠️</span>
              <div>
                <h3 className="font-semibold text-red-900">오류 발생</h3>
                <p className="text-red-700 text-sm mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Step Content */}
        {step === 'upload' && <Upload onAnalyze={handleAnalyze} />}

        {step === 'analysis' && analysisResult && (
          <AnalysisResult
            analysis={analysisResult}
            onGenerateImage={handleGenerateImage}
          />
        )}

        {step === 'comparison' && generatedResult && (
          <ComparisonView
            originalImage={originalImage}
            generatedResult={generatedResult}
            onReset={handleReset}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="container mx-auto px-4 py-6 text-center text-sm text-gray-600">
          <p>
            Photo Guide MVP - 사진 구도 피드백 & 나노 바나나 보정 서비스
          </p>
          <p className="mt-2 text-xs text-gray-500">
            Powered by OpenCV & Google Gemini
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
