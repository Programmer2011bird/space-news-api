from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

import database.cursor as cursor
import datetime
import fastapi


API: fastapi.FastAPI = fastapi.FastAPI()
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
            "article_content": result[5]
        })

    return out

@API.get("/search/keyword/{query}")
async def search_keyword(query: str) -> dict[str, list[dict[str, str | datetime.date]]]:
    results: list[tuple] = DB_CONTROLLER.search_title(query)
    out: list[dict[str, str |  datetime.date]] = assign_key(results)

    return {"results": out}

@API.get("/search/category/{query}")
async def search_category(query: str) -> dict[str, list[dict[str, str |  datetime.date]]]:
    results: list[tuple] = DB_CONTROLLER.search_category(query)
    out: list[dict[str, str |  datetime.date]] = assign_key(results)

    return {"results": out}

@API.get("/search/date/{year}-{month}-{day}")
async def search_date(year: str, month: str, day: str) -> dict[str, list[dict[str, str | datetime.date]]]:
    results: list[tuple] = DB_CONTROLLER.search_date(datetime.datetime(int(year), int(month), int(day)))
    out: list[dict[str, str |  datetime.date]] = assign_key(results)

    return {"results": out}

@API.get("/search/dates/start_date={start_year}-{start_month}-{start_day}&end_date={end_year}-{end_month}-{end_day}")
async def search_between_dates(start_year: str, start_month: str, start_day: str, end_year: str, end_month: str, end_day: str) -> dict[str, list[dict[str, str | datetime.date]]]:
    start_date: datetime.datetime = datetime.datetime(int(start_year), int(start_month), int(start_day))
    end_date: datetime.datetime = datetime.datetime(int(end_year), int(end_month), int(end_day))

    results: list[tuple] = DB_CONTROLLER.search_between_dates(start_date, end_date)
    out: list[dict[str, str |  datetime.date]] = assign_key(results)

    return {"results": out}

@API.get("/")
@API.get("/daily")
async def get_daily_news():
    today_date: datetime.date = datetime.date.today()
    
    results: list[tuple] = DB_CONTROLLER.search_date(today_date)
    out: list[dict[str, str |  datetime.date]] = assign_key(results)

    return {"results": out}