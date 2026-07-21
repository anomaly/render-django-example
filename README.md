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

Before you start you must have0

- Direnv
Direnv automatically loads and unloads environment variables depending on your curent directory. This is used when we have an envrc file in your project. Created per project isolated dev env. 

```bash
brew install direnv
```

- uv
Uv library supports managing Python projects which installs and resolves dependencies faster than pip and replaces multiple tools(like pip, venv etc)

```bash
brew install uv
```

- Taskfile
Open source task runner and builder tool.Use for better cross platform build and ideal code generation. Utilizes YAML syntax to define tasks. 

```bash
brew install go-task/tap/go-task
brew install go-task
```

- Postgres (GRANT PRIVILEGES)
GRANT is used to define access privileges on the database object lie the table, foreign table, column , view. schema etc. 

```bash
grant ALL on database MY_DB to group MY_GROUP;
```

```
export DJANGO_SETTINGS_MODULE=rango.settings.dev
export POSTGRES_DB=django
export POSTGRES_HOST=localhost
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=password123
export POSTGRES_PORT=5432
```                        

- .envrc
A configuration file used by direnv to perform automatic loading and unlaoding of env variables like API Keys. 
```bash
vim .envrc
```

- Render

```bash
brew update
brew install render
```




## On Render.com


## Resources
- [Deploy a Django App on Render](https://render.com/docs/deploy-django)
- [Pydantic Agents](https://github.com/Ho1yShif/pydantic-agents-workflows) by [@Ho1yShif](https://github.com/Ho1yShif)
