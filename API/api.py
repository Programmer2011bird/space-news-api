from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

import database.cursor as cursor
import fastapi


API: fastapi.FastAPI = fastapi.FastAPI()
DB_CONTROLLER: cursor.DB_CONTROLLER = cursor.DB_CONTROLLER()


@API.get("/search/{query}")
async def search_keyword(query: str):
    result: list = DB_CONTROLLER.search_title(query)

    return {"results": result}

@API.get("/category/{query}")
async def search_category(query: str):
    result: list = DB_CONTROLLER.search_category(query)

    return {"results": result}