import axios from 'axios';

const API_BASE_URL = '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

/**
 * Analyze photo composition
 * @param {File} file - Image file
 * @param {string} genre - Photo genre (portrait, landscape, product)
 * @returns {Promise} Analysis result
 */
export const analyzeComposition = async (file, genre = 'portrait') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('genre', genre);

  const response = await api.post('/analyze-composition', formData);
  return response.data;
};

/**
 * Generate nano-banana enhanced image
 * @param {File} file - Original image file
 * @param {string} prompt - Improvement instructions
 * @param {string} style - Style preset
 * @param {number} strength - Modification strength (0-1)
 * @returns {Promise} Generation result
 */
export const generateNanoBanana = async (
  file,
  prompt,
  style = 'natural',
  strength = 0.7
) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('prompt', prompt);
  formData.append('style', style);
  formData.append('strength', strength);

  const response = await api.post('/generate-nanobanana', formData);
  return response.data;
};

/**
 * Check API health
 */
export const healthCheck = async () => {
  const response = await axios.get('/health');
  return response.data;
};

export default api;
