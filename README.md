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
creates the `admin` superuser if it does not exist. Set
`DJANGO_SUPERUSER_PASSWORD` in the Render web service's Environment settings; the
password is intentionally not stored in this repository. To use the requested demo
credentials, set it to `admin123` and sign in at `/admin/` with username `admin`.
Startup does not reset an existing account's password, so you can change it after
signing in. `admin123` is weak; use only for a temporary demo and change it promptly.

To create an additional admin account manually, open the Render shell and run:

```sh
python manage.py createsuperuser
```

This project intentionally uses SQLite to match the assignment requirements. Render
free web-service filesystems are ephemeral, so SQLite data can be lost when the
service restarts, redeploys, or is replaced.
