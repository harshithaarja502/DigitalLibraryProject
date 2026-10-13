# Digital Library

## Deploy on Render

This repository includes a Render Blueprint in `render.yaml`. Push the repository
to GitHub, then in Render choose **New + → Blueprint** and connect this repository.
Render will install dependencies, collect static files, apply migrations, and start
the Django app with Gunicorn. The Blueprint generates a `SECRET_KEY` and configures
production `DEBUG`, allowed hosts, and CSRF origins.

During each deployment, the build also runs `python manage.py seed_demo_data` to
create a small set of fictional authors, books, and members if they are not already
present. This does not copy records from your local database.

On each service start, the Blueprint applies migrations, seeds demo records, and
creates or updates the `libraryadmin` superuser. Render generates its password;
view `DJANGO_SUPERUSER_PASSWORD` in the web service's Environment settings and use it
to sign in at `/admin/`. The generated password is applied on each service start.

To create an additional admin account manually, open the Render shell and run:

```sh
python manage.py createsuperuser
```

This project intentionally uses SQLite to match the assignment requirements. Render
free web-service filesystems are ephemeral, so SQLite data can be lost when the
service restarts, redeploys, or is replaced.
