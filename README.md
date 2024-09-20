# CooKin

## Description

CooKin is a project to obtain a weather-appropriate recipe depending on the location you send. 

## How to install the project

1. Clone the repo
```bash
git clone git@github.com:Karine-Bauch/CooKin.git
```

2. Open it in IDE and install dependencies
```bash
pip install -e .[test,quality]
```

3. Add a .env file with your OpenAI API key, seeing .env.example for sample

## How to use the project in OpenApi Doc

Run the API (at the root of the project)
```bash
fastapi dev src/api/router.py
```

Got to [OpenApi Documentation](http://127.0.0.1:8000/docs)

Click on **"try it out"**
Enter a location and click on **"Execute"**

In the response body, find the weather-appropriate recipe.

## How to use the project in CLI (Typer)

In a new Terminal window, run the command (at the root of the project)
```bash
weather_recipe <location>
```

Need help ? Run
```bash
weather_recipe --help
```
