import cv2
import numpy as np
from typing import Dict


def analyze_exposure(image: np.ndarray) -> Dict:
    """
    Analyze image exposure using histogram analysis

    Checks for clipping (over/under exposure) and dynamic range
    """
    # Convert to grayscale for histogram analysis
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate histogram
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist = hist.flatten() / hist.sum()  # Normalize

    # Check for clipping in shadows (0-10) and highlights (245-255)
    shadow_clip = np.sum(hist[0:10])
    highlight_clip = np.sum(hist[245:256])

    # Calculate dynamic range (std deviation of histogram)
    pixel_values = np.arange(256)
    mean_brightness = np.sum(hist * pixel_values)
    std_brightness = np.sqrt(np.sum(hist * (pixel_values - mean_brightness) ** 2))

    # Normalize dynamic range (0-100)
    dynamic_range = min(100, (std_brightness / 128) * 100)

    # Calculate penalties
    shadow_penalty = min(30, shadow_clip * 300)  # Max 30 points
    highlight_penalty = min(30, highlight_clip * 300)  # Max 30 points
    range_bonus = dynamic_range * 0.2  # Max 20 points

    # Base score
    score = 100 - shadow_penalty - highlight_penalty + range_bonus
    score = max(0, min(100, score))

    # Generate feedback
    issues = []
    if shadow_clip > 0.15:
        issues.append("significant shadow clipping")
    elif shadow_clip > 0.08:
        issues.append("minor shadow clipping")

    if highlight_clip > 0.15:
        issues.append("significant highlight clipping")
    elif highlight_clip > 0.08:
        issues.append("minor highlight clipping")

    if dynamic_range < 30:
        issues.append("low contrast")

    if not issues:
        if score >= 90:
            message = "Excellent exposure with good dynamic range"
            suggestion = "Exposure is well-balanced"
        else:
            message = "Good exposure overall"
            suggestion = "Minor adjustments could improve contrast"
    else:
        message = f"Exposure issues detected: {', '.join(issues)}"

        if shadow_clip > 0.15 and highlight_clip > 0.15:
            suggestion = "Reduce contrast or use HDR techniques"
        elif shadow_clip > 0.15:
            suggestion = "Increase exposure or lift shadows"
        elif highlight_clip > 0.15:
            suggestion = "Decrease exposure or recover highlights"
        else:
            suggestion = "Increase contrast to improve visual impact"

    return {
        "score": round(score, 1),
        "message": message,
        "suggestion": suggestion,
        "metadata": {
            "mean_brightness": round(mean_brightness, 1),
            "dynamic_range": round(dynamic_range, 1),
            "shadow_clipping": round(shadow_clip * 100, 2),
            "highlight_clipping": round(highlight_clip * 100, 2)
        }
    }
