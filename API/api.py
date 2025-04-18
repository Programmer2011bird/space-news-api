from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi import FastAPI, Request
import database.cursor as cursor
import datetime


LIMITER: Limiter = Limiter(key_func=get_remote_address)
API: FastAPI = FastAPI()
API.state.limiter = LIMITER
API.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
DB_CONTROLLER: cursor.DB_CONTROLLER = cursor.DB_CONTROLLER()


def assign_key(inputs: list[tuple]) -> list[dict[str, str |  datetime.date]]:
    out: list[dict[str, str |  datetime.date]] = []

    for result in inputs:
        out.append({
            "name": result[0],
            "category": result[1],
            "date": result[2], 
            "link": result[3],
            "summary": result[4],
            "article_content": result[5], 
            "author": result[6]
        })

    return out

@API.get("/search/keyword/{query}")
@LIMITER.limit("100/hour")
async def search_keyword(request: Request, query: str) -> dict[str, list[dict[str, str | datetime.date]]]:
    results: list[tuple] = DB_CONTROLLER.search_title(query)
    out: list[dict[str, str |  datetime.date]] = assign_key(results)

    return {"results": out}

@API.get("/search/category/{query}")
@LIMITER.limit("100/hour")
async def search_category(request: Request, query: str) -> dict[str, list[dict[str, str |  datetime.date]]]:
    query: str = query.replace("%20", " ")
    results: list[tuple] = DB_CONTROLLER.search_category(query)
    out: list[dict[str, str |  datetime.date]] = assign_key(results)

    return {"results": out}

@API.get("/search/author/{query}")
@LIMITER.limit("100/hour")
async def search_author(request: Request, query: str) -> dict[str, list[dict[str, str |  datetime.date]]]:
    query: str = query.replace("%20", " ")
    results: list[tuple] = DB_CONTROLLER.search_author(query)
    out: list[dict[str, str | datetime.date]] = assign_key(results)

    return {"results": out}

@API.get("/search/date/{year}-{month}-{day}")
@LIMITER.limit("100/hour")
async def search_date(request: Request, year: str, month: str, day: str) -> dict[str, list[dict[str, str | datetime.date]]]:
    results: list[tuple] = DB_CONTROLLER.search_date(datetime.datetime(int(year), int(month), int(day)))
    out: list[dict[str, str |  datetime.date]] = assign_key(results)

    return {"results": out}

@API.get("/search/dates/start_date={start_year}-{start_month}-{start_day}&end_date={end_year}-{end_month}-{end_day}")
@LIMITER.limit("100/hour")
async def search_between_dates(request: Request, start_year: str, start_month: str, start_day: str, end_year: str, end_month: str, end_day: str) -> dict[str, list[dict[str, str | datetime.date]]]:
    start_date: datetime.datetime = datetime.datetime(int(start_year), int(start_month), int(start_day))
    end_date: datetime.datetime = datetime.datetime(int(end_year), int(end_month), int(end_day))

    results: list[tuple] = DB_CONTROLLER.search_between_dates(start_date, end_date)
    out: list[dict[str, str |  datetime.date]] = assign_key(results)

    return {"results": out}

@API.get("/")
@API.get("/daily")
@LIMITER.limit("100/hour")
async def get_daily_news(request: Request):
    today_date: datetime.date = datetime.date.today()
    
    results: list[tuple] = DB_CONTROLLER.search_date(today_date)
    out: list[dict[str, str |  datetime.date]] = assign_key(results)

    return {"results": out}
