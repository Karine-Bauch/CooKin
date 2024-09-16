import fastapi

import services.meteo

app = fastapi.FastAPI()


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to the new CooKin app !"}
