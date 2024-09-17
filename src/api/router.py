import fastapi

import services.recipe
import services.exc

app = fastapi.FastAPI()


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to the new CooKin app !"}


@app.post(
    "/{location}",
    description="Get an original recipe adapted to weather condition of the location",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=str,
    responses={
        fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
        fastapi.status.HTTP_404_NOT_FOUND: {"description": "Recipe Not Found"},
    }
)
def get_recipe(location: str) -> str:
    response = services.recipe.get_recipe(location)
    print(response)
    return response

