# Deploy RSP Core To Render

This project is already prepared for Render with `render.yaml`.

## Before you start

Do not upload the Firebase service account JSON file to GitHub.
The project is already configured to use the environment variable `FIREBASE_SERVICE_ACCOUNT_JSON` instead.

## 1. Put the project on GitHub

If `git` is not installed on this laptop, use GitHub Desktop.

Create a new GitHub repository and upload this project folder.

## 2. Create the Render service

1. Open Render.
2. Click `New +`.
3. Choose `Web Service`.
4. Connect your GitHub repository.
5. Render should detect `render.yaml` automatically.

## 3. Add environment variables in Render

Add these variables:

`FLASK_SECRET_KEY`

Render can generate this automatically.

`FIREBASE_SERVICE_ACCOUNT_JSON`

Paste the full contents of your Firebase service account JSON file into this variable.

It must include the whole JSON object, including the private key lines.

## 4. Deploy

Click deploy.

Render will install dependencies from `requirements.txt` and run:

`gunicorn app:app`

## 5. Your public link

After deployment, Render will give you a public HTTPS URL like:

`https://rsp-core.onrender.com`

That link will work from any laptop or network.

## Notes

- Free Render services may sleep after inactivity.
- The first request after sleep can take a little longer.
- If the app fails on deploy, check that `FIREBASE_SERVICE_ACCOUNT_JSON` was pasted correctly.