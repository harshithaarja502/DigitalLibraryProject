# Digital Library

## Deploy on Render

This repository includes a Render Blueprint in `render.yaml`. Push the repository
to GitHub, then in Render choose **New + → Blueprint** and connect this repository.
Render will install dependencies, collect static files, apply migrations, and start
the Django app with Gunicorn. The Blueprint generates a `SECRET_KEY` and configures
production `DEBUG`, allowed hosts, and CSRF origins.

To create an admin account after the first deployment, open the Render shell and run:

```sh
python manage.py createsuperuser
```

This project intentionally uses SQLite to match the assignment requirements. Render
free web-service filesystems are ephemeral, so SQLite data can be lost when the
service restarts, redeploys, or is replaced.
