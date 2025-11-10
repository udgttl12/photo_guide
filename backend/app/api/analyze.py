from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from pathlib import Path
from ..core.composition import CompositionAnalyzer
from ..models.schemas import CompositionAnalysis, GenreType, RuleScore
from ..core.config import settings

router = APIRouter()


@router.post("/analyze-composition", response_model=CompositionAnalysis)
async def analyze_composition(
    file: UploadFile = File(..., description="Image file to analyze"),
    genre: GenreType = Form(GenreType.PORTRAIT, description="Photo genre")
):
    """
    Analyze photo composition and provide feedback

    Analyzes:
    - Rule of thirds compliance
    - Horizon straightness
    - Exposure quality
    - Image sharpness

    Returns composition score, detailed feedback, and improvement suggestions.
    """

    # Validate file
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not allowed. Allowed: {settings.allowed_extensions}"
        )

    # Create upload directory if not exists
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(exist_ok=True)

    # Save uploaded file
    file_id = str(uuid.uuid4())
    file_path = upload_dir / f"{file_id}{file_ext}"

    try:
        # Write file
        contents = await file.read()

        # Check file size
        if len(contents) > settings.max_upload_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {settings.max_upload_size / 1024 / 1024}MB"
            )

        with open(file_path, "wb") as f:
            f.write(contents)

        # Analyze composition
        analyzer = CompositionAnalyzer(genre=genre.value)
        result = analyzer.analyze(str(file_path))

        # Convert to response model
        response = CompositionAnalysis(
            total_score=result["total_score"],
            genre=genre,
            rules=[RuleScore(**rule) for rule in result["rules"]],
            coach_guide=result["coach_guide"],
            expert_prompt=result["expert_prompt"],
            metadata={
                **result["metadata"],
                "file_id": file_id,
                "filename": file.filename
            }
        )

        return response

    except Exception as e:
        # Clean up file on error
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
