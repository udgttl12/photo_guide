import cv2
import numpy as np
from typing import Dict


def analyze_horizon(image: np.ndarray) -> Dict:
    """
    Analyze horizon line straightness

    Uses Hough Line Transform to detect horizontal lines
    and measure their angle deviation
    """
    height, width = image.shape[:2]

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

    # Detect lines using Hough Transform
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi/180,
        threshold=80,
        minLineLength=width // 4,
        maxLineGap=10
    )

    if lines is None or len(lines) == 0:
        return {
            "score": 100,
            "message": "No clear horizon line detected",
            "suggestion": "This analysis is most useful for landscape photos",
            "metadata": {"angle": 0, "has_horizon": False}
        }

    # Find the most horizontal line (likely the horizon)
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]

        # Calculate angle from horizontal
        if x2 - x1 != 0:
            angle = np.degrees(np.arctan((y2 - y1) / (x2 - x1)))

            # Only consider nearly horizontal lines (within ±30 degrees)
            if abs(angle) < 30:
                angles.append(angle)

    if not angles:
        return {
            "score": 100,
            "message": "No clear horizon line detected",
            "suggestion": "This analysis is most useful for landscape photos",
            "metadata": {"angle": 0, "has_horizon": False}
        }

    # Use median angle to reduce outlier effect
    median_angle = np.median(angles)
    abs_angle = abs(median_angle)

    # Score: 100 for perfect horizontal, decreasing with tilt
    # Penalize more severely after 2 degrees
    if abs_angle <= 1:
        score = 100
    elif abs_angle <= 2:
        score = 100 - (abs_angle - 1) * 10
    else:
        score = max(0, 90 - (abs_angle - 2) * 15)

    # Generate feedback
    if abs_angle < 1:
        message = "Horizon is perfectly level"
        suggestion = "Great job keeping the horizon straight"
    elif abs_angle < 2:
        message = f"Horizon is slightly tilted ({median_angle:.1f}°)"
        suggestion = "Minor adjustment needed - barely noticeable"
    elif abs_angle < 5:
        message = f"Horizon is tilted {abs_angle:.1f}° to the {'right' if median_angle > 0 else 'left'}"
        suggestion = "Consider rotating the image to level the horizon"
    else:
        message = f"Horizon is significantly tilted ({median_angle:.1f}°)"
        suggestion = "Straighten the horizon - this can be distracting to viewers"

    return {
        "score": round(score, 1),
        "message": message,
        "suggestion": suggestion,
        "metadata": {
            "angle": round(median_angle, 2),
            "has_horizon": True,
            "line_count": len(angles)
        }
    }
