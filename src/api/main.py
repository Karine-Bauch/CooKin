import fastapi

import services.meteo

app = fastapi.FastAPI()


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to the new CooKin app !"}


@app.post("/{location}")
def get_recipe(location: str) -> dict:
    response = services.meteo.get_weather(location)
    return response