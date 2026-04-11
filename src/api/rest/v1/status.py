import asyncio
from fastapi import APIRouter, Request, Response, status
from src.api.dependencies import check_db, check_cache

router = APIRouter()

@router.get("/")
async def all_check(request: Request, response: Response):
    db_status, cache_status = asyncio.gather(
        check_db(request),
        check_cache(request),
    )

    overall_ok = all(
        status == "ok" for status in (db_status, cache_status)
    )

    if not overall_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": "ok" if overall_ok else "degraded",
        "services": {
            "db": db_status,
            "cache": cache_status,
        }
    }

@router.get("/app")
def app_check():
    return {"status": "ok"}

@router.get("/db")
async def db_check(request: Request):
    status = await check_db(request)
    return {"status": status}

@router.get("/cache")
async def cache_check(request: Request):
    status = await check_cache(request)
    return {"status": status}

