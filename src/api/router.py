import fastapi

import services.recipe

app = fastapi.FastAPI()


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to the new CooKin app !"}


@app.post(
    "/{location}",
    description="Get an original recipe adapted to weather condition of the location",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=str,
    # TODO: add error responses=
)
def get_recipe(location: str) -> str:
    response = services.recipe.get_recipe(location)
    print(response)
    return response
