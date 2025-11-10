import cv2
import numpy as np
from typing import Dict


def analyze_sharpness(image: np.ndarray) -> Dict:
    """
    Analyze image sharpness using Laplacian variance

    Higher variance indicates sharper image (more edges/details)
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate Laplacian variance
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    variance = laplacian.var()

    # Empirical thresholds (may need tuning based on image size)
    # Typical ranges: <100 (blurry), 100-500 (acceptable), >500 (sharp)

    # Normalize based on image size
    height, width = gray.shape
    pixels = height * width
    normalized_variance = variance * (1000000 / pixels)  # Normalize to 1MP

    # Calculate score
    if normalized_variance >= 500:
        score = 100
    elif normalized_variance >= 300:
        score = 80 + (normalized_variance - 300) / 200 * 20
    elif normalized_variance >= 100:
        score = 50 + (normalized_variance - 100) / 200 * 30
    else:
        score = max(0, normalized_variance / 100 * 50)

    # Generate feedback
    if normalized_variance >= 500:
        message = "Image is very sharp with excellent detail"
        suggestion = "Sharpness is excellent"
        quality = "excellent"
    elif normalized_variance >= 300:
        message = "Image has good sharpness"
        suggestion = "Detail level is acceptable"
        quality = "good"
    elif normalized_variance >= 100:
        message = "Image sharpness is moderate"
        suggestion = "Consider using faster shutter speed or better focus"
        quality = "moderate"
    else:
        message = "Image appears blurry or out of focus"
        suggestion = "Improve focus or reduce camera shake (use tripod/faster shutter)"
        quality = "poor"

    return {
        "score": round(score, 1),
        "message": message,
        "suggestion": suggestion,
        "metadata": {
            "laplacian_variance": round(variance, 2),
            "normalized_variance": round(normalized_variance, 2),
            "quality": quality
        }
    }
