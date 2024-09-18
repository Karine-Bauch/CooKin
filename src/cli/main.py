import typer
import rich
import rich.progress

import services.recipe

app = typer.Typer()


@app.command()
def recipe(location: str):
    """
    Send a recipe weather-appropriate for a LOCATION
    """
    rich.print(f"We're searching a [bold green]fantastic[/bold green] recipe :fork_and_knife_with_plate: for you at {location}, please wait...\n")

    with rich.progress.Progress(rich.progress.SpinnerColumn(spinner_name='aesthetic', speed=0.5), transient=True) as progress:
        progress.add_task("Waiting for your recipe...", start=True)
        recipe_ = services.recipe.get_recipe(location)
    rich.print(recipe_)


if __name__ == "__main__":
    app()
