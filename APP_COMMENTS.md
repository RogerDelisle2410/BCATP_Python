Overview

This document contains non-intrusive comments and a high-level explanation of the Flask app implemented in `app.py`. No code files were changed.

Purpose

- A Flask web application that exposes multiple "tabs" (sections) representing different tables (e.g., `army`, `airforce`, `navy`, `bcatp`, etc.).
- Uses SQLAlchemy models (imported from `models.py`) and a SQLite database configured via `SQLALCHEMY_DATABASE_URI`.

Key points

- Database: SQLAlchemy is initialized with `db.init_app(app)` and the app uses `app.config['SQLALCHEMY_DATABASE_URI']` (two commented options: Azure path and local path).

- Models: The app imports many models at the top: `Bcatp, Army, Airforce, Navy, Dewline, Pinetree, Defunct, Midcanada, Planes, Ships, Tanks`.

Routes and behavior

- Root `/` : Redirects to `/home`.

- Universal edit: `/<tab>/edit/<int:id>` supports GET (render `edit.html` with the row) and POST (update `name`, optional `longitude`/`latitude` only if provided, `comment`, and `wiki`). A `models` mapping selects the proper model class based on `tab`.

- Home: `/home` renders `home.html`.

- Per-tab listing routes: For each tab (e.g., `/army`, `/bcatp`, `/airforce`, `/navy`, `/dewline`, `/pinetree`, `/defunct`, `/midcanada`, `/planes`, `/ships`, `/tanks`) there's a route that:
  - Reads query args `page` (int), `per_page` (int), and `starts` (string filter).
  - Builds a query optionally filtering `name` with `ilike` on `starts`.
  - If `per_page == 0` it returns all rows (unpaginated) sorted by `name`.
  - Otherwise it uses `db.paginate(..., page=page, per_page=per_page)` to create a pagination object and passes it to the template.
  - Templates used correspond to the tab name (e.g., `army.html`, `bcatp.html`, etc.) and receive `rows`, `active_tab`, `starts`, `per_page`, `total_pages`, and `pagination`.

- Add endpoints: Each tab has an `/add` POST endpoint that constructs a new model instance from `request.form` values and commits it. Some tabs set `longitude`/`latitude` to `0` by default (e.g., `planes`, `ships`, `tanks`), while others convert form values to float.

- Universal delete: `/delete/<tab>/<int:id>` maps `tab` to a model, looks up the row, deletes it, and commits. Returns HTTP 400 for invalid tab and 404 for missing record.

- Global search: `/global_search` accepts `query` (string). If empty, returns an empty JSON array. Otherwise it:
  - Iterates through all configured tables (same mapping as other parts).
  - Loads all rows ordered by `name` (unpaginated) and checks whether the lowercase `query` substring appears in each `r.name.lower()`.
  - Computes the pagination `page` for the found row using `per_page = 10` and `page = (index // per_page) + 1` and returns a JSON array of matches with `tab`, `id`, `name`, and `page`.

Notes, caveats and suggestions (non-code)

- The `global_search` function assumes a default `per_page = 10` when computing the `page` for results. This must match the per-page default in each tab's UI (currently `per_page` defaults to `10` in many routes). If you change the UI default, update `global_search` accordingly.

- For numeric form values (longitude/latitude), the code converts directly via `float(request.form.get(...))`. If form fields may be empty or invalid, consider additional validation to avoid ValueError exceptions.

- `db.paginate` is used (Flask-SQLAlchemy 3.x style). Ensure the installed Flask-SQLAlchemy version supports `db.paginate`.

- This file contains only comments and high-level explanation; no code was edited.

End of comments
