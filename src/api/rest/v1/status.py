import asyncio

from fastapi import APIRouter, Depends, Response, status

from src.api.dependencies import (
    check_cache,
    check_db,
    get_cache_client,
    get_cache_type,
    get_db_engine,
    get_db_type,
)

router = APIRouter()


@router.get("/")
async def all_check(
    response: Response,
    db_type=Depends(get_db_type),
    db_engine=Depends(get_db_engine),
    cache_type=Depends(get_cache_type),
    cache_client=Depends(get_cache_client),
):
    db_status, cache_status = await asyncio.gather(
        check_db(db_type=db_type, db_engine=db_engine),
        check_cache(cache_type=cache_type, cache_client=cache_client),
    )

    overall_ok = all(status == "ok" for status in (db_status, cache_status))

    if not overall_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": "ok" if overall_ok else "degraded",
        "services": {
            "db": db_status,
            "cache": cache_status,
        },
    }


@router.get("/app")
def app_check():
    return {"status": "ok"}


@router.get("/db")
async def db_check(db_engine=Depends(get_db_engine), db_type=Depends(get_db_type)):
    status = await check_db(db_type=db_type, db_engine=db_engine)
    return {"status": status}


@router.get("/cache")
async def cache_check(
    cache_client=Depends(get_cache_client), cache_type=Depends(get_cache_type)
):
    status = await check_cache(cache_type=cache_type, cache_client=cache_client)
    return {"status": status}
