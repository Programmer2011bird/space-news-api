import database.cursor as cursor
import fastapi


API: fastapi.FastAPI = fastapi.FastAPI()


@API.get("/search/{query}")
async def search_keyword(query: str):
    DB_CONTROLLER: cursor.DB_CONTROLLER = cursor.DB_CONTROLLER()
    result: list = DB_CONTROLLER.search_title(query)

    return {"results": result}

