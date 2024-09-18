import typer

import services.recipe

app = typer.Typer()


@app.command()
def recipe(location: str):
    """
    Send a recipe weather-appropriate for a LOCATION
    """
    print("We're searching a fantastic recipe for you, please wait...")
    recipe_ = services.recipe.get_recipe(location)
    print(recipe_)


if __name__ == "__main__":
    app()
