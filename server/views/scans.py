from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from handlers.scans_handler import ScansHandler, get_scans_handler

router = APIRouter()
templates = Jinja2Templates(directory="static/templates")


@router.get("/scans", response_class=HTMLResponse)
async def get_scans(
    request: Request, scans_handler: Annotated[ScansHandler, Depends(get_scans_handler)]
) -> HTMLResponse:
    scans = await scans_handler.list_scans()

    return templates.TemplateResponse(
        "all_scans.html", {"request": request, "scans": scans}
    )


@router.get("/scans/{scan_id}", response_class=HTMLResponse)
async def get_images(request: Request, scan_id: str) -> HTMLResponse:
    return templates.TemplateResponse(
        "scan.html", {"request": request, "scan_id": scan_id}
    )
