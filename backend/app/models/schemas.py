from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum


class GenreType(str, Enum):
    """Photo genre types"""
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"
    PRODUCT = "product"


class RuleScore(BaseModel):
    """Individual composition rule score"""
    name: str
    score: float = Field(..., ge=0, le=100)
    message: str
    suggestion: str


class CompositionAnalysis(BaseModel):
    """Complete composition analysis result"""
    total_score: float = Field(..., ge=0, le=100)
    genre: GenreType
    rules: List[RuleScore]
    coach_guide: str
    expert_prompt: str
    metadata: Dict[str, any] = {}


class AnalyzeRequest(BaseModel):
    """Request for composition analysis"""
    genre: GenreType = GenreType.PORTRAIT


class GenerateRequest(BaseModel):
    """Request for nano-banana image generation"""
    prompt: str
    style: Optional[str] = "natural"
    strength: Optional[float] = Field(0.7, ge=0, le=1)


class GenerateResponse(BaseModel):
    """Response from image generation"""
    success: bool
    image_url: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, any] = {}
