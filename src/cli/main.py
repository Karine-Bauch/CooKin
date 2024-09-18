import typer

import services.recipe

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def recipe(location: str):
    recipe_ = services.recipe.get_recipe(location)
    print(recipe_)

if __name__ == "__main__":
    app()