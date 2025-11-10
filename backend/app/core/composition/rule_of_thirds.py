import cv2
import numpy as np
from typing import Tuple, Dict


def analyze_rule_of_thirds(image: np.ndarray) -> Dict:
    """
    Analyze Rule of Thirds composition

    Checks if important visual elements are near the intersection points
    of the 3x3 grid (power points)
    """
    height, width = image.shape[:2]

    # Define rule of thirds grid points (4 intersection points)
    third_x = width // 3
    third_y = height // 3
    power_points = [
        (third_x, third_y),
        (2 * third_x, third_y),
        (third_x, 2 * third_y),
        (2 * third_x, 2 * third_y)
    ]

    # Convert to grayscale for edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect edges using Canny
    edges = cv2.Canny(gray, 50, 150)

    # Calculate interest points near power points
    interest_scores = []
    radius = min(width, height) // 10  # 10% of image size

    for px, py in power_points:
        # Extract region around power point
        y1, y2 = max(0, py - radius), min(height, py + radius)
        x1, x2 = max(0, px - radius), min(width, px + radius)
        region = edges[y1:y2, x1:x2]

        # Calculate edge density (interest level)
        if region.size > 0:
            density = np.sum(region > 0) / region.size
            interest_scores.append(density)

    # Calculate average interest at power points
    avg_interest = np.mean(interest_scores) if interest_scores else 0

    # Score: 0-100 based on interest concentration
    score = min(100, avg_interest * 500)  # Scale factor

    # Generate feedback
    if score >= 80:
        message = "Excellent composition following the Rule of Thirds"
        suggestion = "Your subject placement is well-balanced"
    elif score >= 60:
        message = "Good use of Rule of Thirds"
        suggestion = "Consider positioning key elements closer to power points"
    elif score >= 40:
        message = "Moderate alignment with Rule of Thirds"
        suggestion = "Try moving your subject toward the intersection points"
    else:
        message = "Subject is not aligned with Rule of Thirds"
        suggestion = "Reframe to place your subject at one of the four intersection points"

    return {
        "score": round(score, 1),
        "message": message,
        "suggestion": suggestion,
        "metadata": {
            "power_points": power_points,
            "interest_scores": [round(s, 3) for s in interest_scores]
        }
    }
