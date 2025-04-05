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