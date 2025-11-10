from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from pathlib import Path
from typing import Optional
from ..services.gemini_client import GeminiClient
from ..models.schemas import GenerateRequest, GenerateResponse
from ..core.config import settings

router = APIRouter()


@router.post("/generate-nanobanana", response_model=GenerateResponse)
async def generate_nanobanana(
    file: UploadFile = File(..., description="Original image file"),
    prompt: str = Form(..., description="Improvement instructions"),
    style: Optional[str] = Form("natural", description="Style preset (natural/vivid/dramatic)"),
    strength: Optional[float] = Form(0.7, description="Modification strength (0-1)")
):
    """
    Generate improved image using Google Gemini (Nano-Banana)

    Takes an original image and improvement instructions,
    returns AI-enhanced version with suggested modifications.
    """

    # Validate file
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Validate strength
    if not 0 <= strength <= 1:
        raise HTTPException(status_code=400, detail="Strength must be between 0 and 1")

    # Validate style
    valid_styles = ["natural", "vivid", "dramatic"]
    if style not in valid_styles:
        raise HTTPException(status_code=400, detail=f"Style must be one of {valid_styles}")

    # Create upload directory
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(exist_ok=True)

    output_dir = Path(settings.output_dir)
    output_dir.mkdir(exist_ok=True)

    # Save uploaded file
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.allowed_extensions:
        raise HTTPException(status_code=400, detail=f"File type not allowed: {file_ext}")

    file_id = str(uuid.uuid4())
    input_path = upload_dir / f"{file_id}_input{file_ext}"
    output_path = output_dir / f"{file_id}_output{file_ext}"

    try:
        # Save input file
        contents = await file.read()

        if len(contents) > settings.max_upload_size:
            raise HTTPException(status_code=400, detail="File too large")

        with open(input_path, "wb") as f:
            f.write(contents)

        # Generate improved image
        client = GeminiClient()
        result = await client.generate_image(
            str(input_path),
            prompt,
            style,
            strength
        )

        if result["success"]:
            return GenerateResponse(
                success=True,
                image_url=f"/outputs/{file_id}_output{file_ext}",
                metadata={
                    "file_id": file_id,
                    "original_filename": file.filename,
                    "style": style,
                    "strength": strength,
                    **result
                }
            )
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Generation failed"))

    except HTTPException:
        raise
    except Exception as e:
        # Clean up files on error
        if input_path.exists():
            input_path.unlink()
        if output_path.exists():
            output_path.unlink()
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Photo Guide API"}
