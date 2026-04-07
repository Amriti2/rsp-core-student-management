# RSP Core Student Management System

RSP Core is a Flask and Firebase student management app with student dashboards, principal oversight, calendar management, chat, and community service tracking.

## Installation

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Put the Firebase service account file in the project root as `rsp-system-firebase-adminsdk-fbsvc-ab197f8feb.json`.

## Run Locally

For local use on this laptop:

```bash
python run_app.py
```

## Share On Your Wi-Fi

For access from other laptops on the same network:

```bash
python web_run.py
```

Or on Windows, just double-click:

```text
start_lan.bat
```

The app will print both the local link and the LAN link, for example `http://192.168.x.x:5000`.

## Downloadable Windows App

The packaged Windows build is in the `dist` folder:

- `dist/RSP-Core.exe`
- `dist/RSP-Core-portable.zip`

You can copy the ZIP file to another Windows laptop and run the EXE there.

## Public Deployment

This project is prepared for Render deployment with `render.yaml`.

### Render setup

1. Push this project to GitHub.
2. Create a new Render Web Service from the repo.
3. Render will use `render.yaml` automatically.
4. In Render, add the environment variable `FIREBASE_SERVICE_ACCOUNT_JSON`.

`FIREBASE_SERVICE_ACCOUNT_JSON` should contain the full contents of your Firebase service account JSON as one string.

You can also set:

- `FLASK_SECRET_KEY`

Once deployed, Render will give you a public HTTPS link that works from any laptop.

## Principal Access

Principal usernames are controlled in `PRINCIPALS` inside `app.py`. Those usernames must also exist in Firestore as user documents so they can log in through the normal login page.