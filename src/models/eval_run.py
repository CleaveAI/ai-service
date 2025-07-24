from datetime import datetime
from typing import List, Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


# ----- Run Sub Documents -----
class Step(BaseModel):
    name: str
    status: str
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    message: Optional[str] = None


class VariantProgress(BaseModel):
    variant_id: str
    variant_prompt: str
    status: str
    total_tests: int
    completed_tests: int
    updated_at: datetime = Field(default_factory=datetime.now)


class BestVariant(BaseModel):
    variant_id: str
    variant_prompt: str
    score: float
    updated_at: datetime = Field(default_factory=datetime.now)


class RunConfig(BaseModel):
    max_variants: int
    stop_threshold: float


# ----- Run Document -----
class EvalRun(Document):
    dataset_id: PydanticObjectId
    original_prompt: str
    config: RunConfig
    status: str
    steps: List[Step] = Field(
        default_factory=lambda: [
            Step(name="Initializing"),
            Step(name="generate_variants"),
            Step(name="evaluate_variants"),
        ]
    )
    variants: List[VariantProgress] = Field(default_factory=list)
    best_variant: Optional[BestVariant] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "eval_runs"
