# Django sample for Render
> A Django template for Render

> [!CAUTION]
> This project is currently under development, don't deploy if you this notice

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/anomaly/django-render-sample)

> [!WARNING]
> Render Workflows does not support Blueprint, you will have to follow the documented steps to register your Workflow worker.

This is a sample Django project that demonstrates the use of Render technologies inside of the Django context. In particular it seeks to demonstrate:

- Settings for development and deployment into Render
- Workflow Tasks accessing the Django ORM
- A Django management command that can trigger the worker

We also include:

- A minimal `blueprint` to deploy this project to Render
- Instructions for running the project locally


## Setup for development

`direnv` automatically loads and unloads environment variables from your `.envrc` file on your current directory. Install this via `brew`:

```bash
brew install direnv
```

Use this template for a `.envrc` file and adjust the values as needed.

```envrc
export DJANGO_SETTINGS_MODULE=rango.settings.dev
export POSTGRES_DB=django
export POSTGRES_HOST=localhost
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_PORT=5432
```

Each time you modify `.envrc`, run `direnv allow` to reload the environment variables.

We use `uv` to manage Python dependencies. Install it and sync the dependencies:

```bash
brew install uv
uv sync
```

`Taskfile` is a cross-platform task runner and builder tool. Install it via `brew` and use it to run tasks defined in `Taskfile.yaml`.

```bash
brew install go-task/tap/go-task
brew install go-task
task # will show you the available tasks
```

Make sure you create a databae for your project and `GRANT` the necessary privileges to the `postgres` user.

```psql
CREATE DATABASE django;
GRANT ALL PRIVILEGES ON DATABASE django TO postgres;
```

### Render Workflows

You will require the Render CLI to assist with your developing Render Workflows, install it with the handy `brew` command below.

```bash
brew install render
```

## Django project structure

For giggles I called the Django app `rango` (Render and Django, also [a western comedy film](https://en.wikipedia.org/wiki/Rango_(2011_film)))

- `rango/` - the Django app
- `busybee` - the app where I have the workflow implemented

## On Render.com


## Resources
- [Deploy a Django App on Render](https://render.com/docs/deploy-django)
- [Pydantic Agents](https://github.com/Ho1yShif/pydantic-agents-workflows) by [@Ho1yShif](https://github.com/Ho1yShif)
