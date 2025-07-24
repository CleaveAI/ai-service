from fastapi import APIRouter

from src.utils.response import Response, Status

router = APIRouter()


@router.post("/run")
async def run_eval():
    """Run evaluation with standard 200 response."""
    return Response.success(
        message="Evaluation completed successfully",
        data={"result": "evaluation_complete", "score": 0.95},
    )


@router.post("/create")
async def create_eval():
    """Create new evaluation with 201 Created response."""
    return Response.success(
        message="Evaluation created successfully",
        data={"eval_id": "eval_123", "status": "created"},
        status_code=Status.CREATED,
    )


@router.get("/{eval_id}")
async def get_eval(eval_id: str):
    """Get evaluation by ID with conditional responses."""
    # Simulate checking if eval exists
    if eval_id == "not_found":
        return Response.error(
            message=f"Evaluation with ID '{eval_id}' not found",
            status_code=Status.NOT_FOUND,
        )

    return Response.success(
        message="Evaluation retrieved successfully",
        data={"eval_id": eval_id, "status": "completed", "score": 0.87},
    )
