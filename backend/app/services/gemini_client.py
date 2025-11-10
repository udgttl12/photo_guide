import google.generativeai as genai
from PIL import Image
import base64
import io
from typing import Optional, Dict
import asyncio
from ..core.config import settings


class GeminiClient:
    """Client for Google Gemini API (Nano-Banana image generation)"""

    def __init__(self):
        """Initialize Gemini client"""
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY not configured")

        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)

    async def generate_image(
        self,
        image_path: str,
        prompt: str,
        style: str = "natural",
        strength: float = 0.7
    ) -> Dict:
        """
        Generate improved image using Gemini

        Args:
            image_path: Path to original image
            prompt: Improvement instructions
            style: Style preset (natural, vivid, dramatic)
            strength: How much to modify (0-1)

        Returns:
            Dict with success status and result
        """
        try:
            # Load original image
            original_image = Image.open(image_path)

            # Build enhanced prompt
            full_prompt = self._build_prompt(prompt, style, strength)

            # Call Gemini API
            # Note: Gemini 2.0 Flash Exp doesn't directly support image-to-image
            # We'll use it for image understanding and text generation
            # For actual image manipulation, you might need to use different models
            # or services. For MVP, we'll generate descriptive guidance.

            response = await asyncio.to_thread(
                self.model.generate_content,
                [full_prompt, original_image]
            )

            # Since Gemini primarily does text, we'll return the improvement suggestions
            # In production, you'd integrate with imagen or other image generation models
            return {
                "success": True,
                "suggestions": response.text,
                "note": "Image generation coming soon - currently showing AI analysis and suggestions"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _build_prompt(self, base_prompt: str, style: str, strength: float) -> str:
        """Build enhanced prompt with style and strength"""

        style_modifiers = {
            "natural": "Maintain natural, photographic look with subtle enhancements.",
            "vivid": "Enhance colors and contrast for more vibrant, eye-catching result.",
            "dramatic": "Apply dramatic lighting and tones for artistic, moody effect."
        }

        strength_text = {
            0.3: "Make very subtle adjustments, barely noticeable changes.",
            0.5: "Make moderate adjustments, balanced improvements.",
            0.7: "Make clear improvements while keeping natural feel.",
            0.9: "Make strong, obvious improvements and corrections."
        }

        # Find closest strength level
        strength_key = min(strength_text.keys(), key=lambda x: abs(x - strength))

        prompt = f"""You are a professional photo editor. Analyze this image and provide specific, actionable recommendations for improvement.

{base_prompt}

Style preference: {style_modifiers.get(style, style_modifiers['natural'])}
Adjustment strength: {strength_text[strength_key]}

Provide a detailed list of specific edits that should be made, including:
- Exact adjustments needed (e.g., "increase exposure by +0.5 EV", "rotate 2° clockwise")
- Color and tone corrections
- Composition improvements
- Any cropping or straightening needed

Be specific and technical in your recommendations."""

        return prompt


async def generate_nano_banana(
    image_path: str,
    prompt: str,
    style: str = "natural",
    strength: float = 0.7
) -> Dict:
    """
    Convenience function for generating nano-banana image

    Args:
        image_path: Path to original image
        prompt: Improvement instructions
        style: Style preset
        strength: Modification strength (0-1)

    Returns:
        Generation result
    """
    client = GeminiClient()
    return await client.generate_image(image_path, prompt, style, strength)
