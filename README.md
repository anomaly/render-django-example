# Django sample for Render Workflows
> A Django template to demonstrate the use of Render Workflows inside of Django

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

This is a sample Django project that demonstrates the use of Render Workflows inside of the Django context. In particular it seeks to demonstrate:

- Workflow Tasks accessing the Django ORM
- A Django management command that can trigger the worker
- A way of sharing the workflow context across packages (so you can define tasks in separate apps or files)

We also include:

- A minimal `blueprint` to deploy this project to Render
- Instructions for running the project locally
