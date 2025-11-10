import cv2
import numpy as np
from typing import Dict, List
from .rule_of_thirds import analyze_rule_of_thirds
from .horizon import analyze_horizon
from .exposure import analyze_exposure
from .sharpness import analyze_sharpness


class CompositionAnalyzer:
    """Main composition analyzer with genre-specific weighting"""

    # Genre-specific weights for each rule
    GENRE_WEIGHTS = {
        "portrait": {
            "rule_of_thirds": 0.35,
            "horizon": 0.10,
            "exposure": 0.35,
            "sharpness": 0.20
        },
        "landscape": {
            "rule_of_thirds": 0.30,
            "horizon": 0.35,
            "exposure": 0.25,
            "sharpness": 0.10
        },
        "product": {
            "rule_of_thirds": 0.20,
            "horizon": 0.05,
            "exposure": 0.35,
            "sharpness": 0.40
        }
    }

    def __init__(self, genre: str = "portrait"):
        self.genre = genre
        self.weights = self.GENRE_WEIGHTS.get(genre, self.GENRE_WEIGHTS["portrait"])

    def analyze(self, image_path: str) -> Dict:
        """
        Perform complete composition analysis

        Args:
            image_path: Path to the image file

        Returns:
            Dict containing analysis results
        """
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")

        # Run all analyses
        results = {
            "rule_of_thirds": analyze_rule_of_thirds(image),
            "horizon": analyze_horizon(image),
            "exposure": analyze_exposure(image),
            "sharpness": analyze_sharpness(image)
        }

        # Calculate weighted total score
        total_score = sum(
            results[rule]["score"] * self.weights[rule]
            for rule in self.weights
        )

        # Build rule scores list
        rule_scores = [
            {
                "name": "Rule of Thirds",
                "score": results["rule_of_thirds"]["score"],
                "message": results["rule_of_thirds"]["message"],
                "suggestion": results["rule_of_thirds"]["suggestion"]
            },
            {
                "name": "Horizon Level",
                "score": results["horizon"]["score"],
                "message": results["horizon"]["message"],
                "suggestion": results["horizon"]["suggestion"]
            },
            {
                "name": "Exposure",
                "score": results["exposure"]["score"],
                "message": results["exposure"]["message"],
                "suggestion": results["exposure"]["suggestion"]
            },
            {
                "name": "Sharpness",
                "score": results["sharpness"]["score"],
                "message": results["sharpness"]["message"],
                "suggestion": results["sharpness"]["suggestion"]
            }
        ]

        # Generate coach guide (beginner-friendly explanation)
        coach_guide = self._generate_coach_guide(total_score, results)

        # Generate expert prompt for nano-banana
        expert_prompt = self._generate_expert_prompt(results, image.shape)

        return {
            "total_score": round(total_score, 1),
            "genre": self.genre,
            "rules": rule_scores,
            "coach_guide": coach_guide,
            "expert_prompt": expert_prompt,
            "metadata": {
                "image_size": {"width": image.shape[1], "height": image.shape[0]},
                "weights": self.weights,
                "raw_results": {
                    k: v["metadata"] for k, v in results.items() if "metadata" in v
                }
            }
        }

    def _generate_coach_guide(self, total_score: float, results: Dict) -> str:
        """Generate beginner-friendly coaching guide"""

        if total_score >= 85:
            intro = "🎉 Excellent photo! Your composition is very strong."
        elif total_score >= 70:
            intro = "👍 Good job! Your photo has solid composition with room for minor improvements."
        elif total_score >= 50:
            intro = "📷 Your photo is on the right track, but there are some areas to improve."
        else:
            intro = "📚 Let's work on improving your composition. Here are the key areas to focus on:"

        tips = [intro, ""]

        # Add specific tips based on low-scoring rules
        if results["rule_of_thirds"]["score"] < 60:
            tips.append("💡 **Rule of Thirds**: Imagine a 3×3 grid on your viewfinder. Try placing your main subject at one of the four intersection points instead of dead center. This creates more dynamic, interesting compositions.")

        if results["horizon"]["score"] < 80 and results["horizon"]["metadata"].get("has_horizon"):
            angle = results["horizon"]["metadata"]["angle"]
            tips.append(f"🌅 **Horizon Level**: Your horizon is tilted {abs(angle):.1f}° to the {'right' if angle > 0 else 'left'}. Use your camera's grid overlay or level feature to keep horizons straight. Tilted horizons can make viewers feel uneasy.")

        if results["exposure"]["score"] < 60:
            meta = results["exposure"]["metadata"]
            if meta["shadow_clipping"] > 8:
                tips.append("💡 **Exposure - Shadows**: Your shadows are too dark (clipping). Try increasing exposure or using fill light to reveal more detail in dark areas.")
            if meta["highlight_clipping"] > 8:
                tips.append("☀️ **Exposure - Highlights**: Your bright areas are overexposed (blown out). Reduce exposure or use exposure compensation to preserve highlight details.")

        if results["sharpness"]["score"] < 60:
            tips.append("🔍 **Sharpness**: Your image appears soft or blurry. Make sure to:\n  - Focus carefully on your subject\n  - Use a faster shutter speed (1/focal_length minimum)\n  - Hold the camera steady or use a tripod\n  - Check if your lens is clean")

        if len(tips) == 2:  # Only intro, no specific tips
            tips.append("Keep up the great work! All the fundamentals are looking good.")

        return "\n\n".join(tips)

    def _generate_expert_prompt(self, results: Dict, shape: tuple) -> str:
        """Generate detailed prompt for nano-banana image generation"""

        height, width = shape[:2]
        improvements = []

        # Rule of thirds adjustment
        rot_score = results["rule_of_thirds"]["score"]
        if rot_score < 70:
            improvements.append(
                "reframe composition to better align with rule of thirds, "
                "positioning key subject elements at power points (intersection of grid lines)"
            )

        # Horizon correction
        horizon_data = results["horizon"]["metadata"]
        if horizon_data.get("has_horizon") and abs(horizon_data["angle"]) > 1:
            angle = horizon_data["angle"]
            improvements.append(f"rotate image {-angle:.1f} degrees to level the horizon line")

        # Exposure adjustments
        exp_meta = results["exposure"]["metadata"]
        if exp_meta["shadow_clipping"] > 8:
            improvements.append("lift shadows and recover detail in dark areas")
        if exp_meta["highlight_clipping"] > 8:
            improvements.append("reduce highlights and recover detail in bright areas")
        if exp_meta["dynamic_range"] < 40:
            improvements.append("increase contrast and dynamic range for more visual impact")

        # Sharpness enhancement
        sharp_meta = results["sharpness"]["metadata"]
        if results["sharpness"]["score"] < 70:
            if sharp_meta["quality"] in ["poor", "moderate"]:
                improvements.append("enhance sharpness and clarity, add micro-contrast to bring out details")

        # Genre-specific enhancements
        if self.genre == "portrait":
            improvements.append("ensure flattering skin tones and natural colors")
            improvements.append("optimize lighting on face with proper catchlights in eyes")
        elif self.genre == "landscape":
            improvements.append("enhance color saturation and vibrancy while maintaining natural look")
            improvements.append("improve depth and dimensionality through selective sharpening")
        elif self.genre == "product":
            improvements.append("ensure perfect focus and maximum sharpness on product")
            improvements.append("create clean, professional lighting with no harsh shadows")

        if not improvements:
            prompt = f"Enhance this {self.genre} photograph while maintaining its natural character. Subtle improvements to color, tone, and overall polish."
        else:
            prompt = f"Improve this {self.genre} photograph with the following adjustments:\n\n"
            prompt += "\n".join(f"- {imp}" for imp in improvements)
            prompt += f"\n\nMaintain natural, photographic quality. Avoid over-processing. Target style: professional {self.genre} photography."

        return prompt


def analyze_composition(image_path: str, genre: str = "portrait") -> Dict:
    """
    Convenience function for analyzing composition

    Args:
        image_path: Path to image file
        genre: Photo genre (portrait, landscape, product)

    Returns:
        Complete analysis results
    """
    analyzer = CompositionAnalyzer(genre=genre)
    return analyzer.analyze(image_path)
