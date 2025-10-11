from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="views/templates")


@router.get("/scans/{scan_id}", response_class=HTMLResponse)
async def get_images(request: Request, scan_id: str):
    return templates.TemplateResponse(
        "scan.html", {"request": request, "scan_id": scan_id}
    )
