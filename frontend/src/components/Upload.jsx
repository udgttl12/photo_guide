import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

const GENRES = [
  { value: 'portrait', label: '인물', icon: '👤' },
  { value: 'landscape', label: '풍경', icon: '🌄' },
  { value: 'product', label: '제품', icon: '📦' },
];

export default function Upload({ onAnalyze }) {
  const [selectedGenre, setSelectedGenre] = useState('portrait');
  const [preview, setPreview] = useState(null);
  const [file, setFile] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const uploadedFile = acceptedFiles[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      const reader = new FileReader();
      reader.onload = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(uploadedFile);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp'],
    },
    maxFiles: 1,
  });

  const handleAnalyze = () => {
    if (file) {
      onAnalyze(file, selectedGenre);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6">
      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-12 text-center cursor-pointer
          transition-colors duration-200
          ${
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400 bg-white'
          }
        `}
      >
        <input {...getInputProps()} />

        {preview ? (
          <div className="space-y-4">
            <img
              src={preview}
              alt="Preview"
              className="max-h-64 mx-auto rounded-lg shadow-md"
            />
            <p className="text-sm text-gray-600">
              다른 이미지를 선택하려면 클릭하거나 드래그하세요
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            <div className="text-6xl">📷</div>
            <p className="text-lg font-medium text-gray-700">
              사진을 드래그하거나 클릭하여 업로드
            </p>
            <p className="text-sm text-gray-500">
              JPG, PNG, WEBP 지원 (최대 10MB)
            </p>
          </div>
        )}
      </div>

      {/* Genre Selection */}
      <div className="bg-white rounded-lg p-6 shadow-sm">
        <h3 className="text-lg font-semibold mb-4">장르 선택</h3>
        <div className="grid grid-cols-3 gap-3">
          {GENRES.map((genre) => (
            <button
              key={genre.value}
              onClick={() => setSelectedGenre(genre.value)}
              className={`
                p-4 rounded-lg border-2 transition-all duration-200
                ${
                  selectedGenre === genre.value
                    ? 'border-primary-500 bg-primary-50 text-primary-700'
                    : 'border-gray-200 hover:border-gray-300 text-gray-700'
                }
              `}
            >
              <div className="text-3xl mb-2">{genre.icon}</div>
              <div className="font-medium">{genre.label}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Analyze Button */}
      <button
        onClick={handleAnalyze}
        disabled={!file}
        className={`
          w-full py-4 px-6 rounded-lg font-semibold text-lg
          transition-all duration-200
          ${
            file
              ? 'bg-primary-600 text-white hover:bg-primary-700 shadow-lg hover:shadow-xl'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }
        `}
      >
        {file ? '구도 분석 시작' : '사진을 업로드하세요'}
      </button>
    </div>
  );
}
