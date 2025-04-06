from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

import database.cursor as cursor
import datetime
import fastapi


API: fastapi.FastAPI = fastapi.FastAPI()
DB_CONTROLLER: cursor.DB_CONTROLLER = cursor.DB_CONTROLLER()


@API.get("/search/keyword/{query}")
async def search_keyword(query: str):
    result: list = DB_CONTROLLER.search_title(query)

    return {"results": result}

@API.get("/search/category/{query}")
async def search_category(query: str):
    result: list = DB_CONTROLLER.search_category(query)

    return {"results": result}

@API.get("/search/date/{year}-{month}-{day}")
async def search_date(year: str, month: str, day: str):
    result: list = DB_CONTROLLER.search_date(datetime.datetime(int(year), int(month), int(day)))

    return {"results": result}

@API.get("/search/date/start_date={start_year}-{start_month}-{start_day}&end_date={end_year}-{end_month}-{end_day}")
async def search_between_dates(start_year: str, start_month: str, start_day: str, end_year: str, end_month: str, end_day: str):
    print(start_year)
    start_date: datetime.datetime = datetime.datetime(int(start_year), int(start_month), int(start_day))
    end_date: datetime.datetime = datetime.datetime(int(end_year), int(end_month), int(end_day))

    result: list = DB_CONTROLLER.search_between_dates(start_date, end_date)

    return {"results": result}