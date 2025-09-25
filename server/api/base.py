from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def base_url() -> dict[str, bool]:
    return {"ok": True}
