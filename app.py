import os
import sys
import json

import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "rsp_core_secure_system_key")

PRINCIPALS = ["admin", "principal_mark", "school_head", "amran2", "principal2"]


def initialize_firestore():
    if getattr(sys, "frozen", False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "rsp-system-firebase-adminsdk-fbsvc-ab197f8feb.json")
    env_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON", "").strip()
    env_json_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_PATH", "").strip()

    try:
        if not firebase_admin._apps:
            if env_json:
                cred = credentials.Certificate(json.loads(env_json))
            elif env_json_path:
                cred = credentials.Certificate(env_json_path)
            else:
                cred = credentials.Certificate(json_path)
            firebase_admin.initialize_app(cred)
        client = firestore.client()
        print("Firebase Connected Successfully!")
        return client
    except Exception as error:
        print(f"Firebase Error: {error}")
        return None


db = initialize_firestore()


def db_ready():
    return db is not None


def is_principal_username(username):
    return username in PRINCIPALS


def is_principal_user(user_data):
    username = (user_data or {}).get("username", "")
    return is_principal_username(username)


def parse_subjects(raw_subjects):
    if not raw_subjects:
        return []
    return [subject.strip() for subject in raw_subjects.split(",") if subject.strip()]


def get_user_document(user_id):
    if not db_ready():
        return None
    document = db.collection("users").document(user_id).get()
    if not document.exists:
        return None
    return document


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/test_firestore")
def test_firestore():
    if not db_ready():
        return jsonify({"success": False, "error": "Firestore is not connected."}), 500

    try:
        test_doc = db.collection("test").document("connection_test")
        test_doc.set({"status": "connected", "timestamp": firestore.SERVER_TIMESTAMP}, merge=True)
        data = test_doc.get().to_dict() or {}
        return jsonify({"success": True, "data": data}), 200
    except Exception as error:
        print(f"Firestore Test Error: {error}")
        return jsonify({"success": False, "error": str(error)}), 500


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm", "").strip()

        if not db_ready():
            flash("Database connection failed. Check your Firebase file and Firestore setup.", "danger")
            return render_template("signup.html")

        if not username or not password:
            flash("Please fill in all fields.", "danger")
            return render_template("signup.html")

        if confirm and password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("signup.html")

        try:
            existing = db.collection("users").where("username", "==", username).limit(1).get()
            if existing:
                flash("Username already exists.", "danger")
                return render_template("signup.html")

            created_ref = db.collection("users").document()
            created_ref.set(
                {
                    "username": username,
                    "password": generate_password_hash(password),
                    "name": "",
                    "subjects": [],
                    "level": "",
                    "notes": [],
                    "community_service": [],
                    "community_hours": 0,
                }
            )
            flash("Account created successfully. Please log in.", "success")
            return redirect(url_for("login"))
        except Exception as error:
            print(f"Signup Error: {error}")
            flash("Could not create account right now.", "danger")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not db_ready():
            flash("Database connection failed. Check your Firebase file and Firestore setup.", "danger")
            return render_template("login.html")

        if not username or not password:
            flash("Please fill in all fields.", "danger")
            return render_template("login.html")

        try:
            result = db.collection("users").where("username", "==", username).limit(1).get()
            if not result:
                flash("Invalid username or password.", "danger")
                return render_template("login.html")

            user_doc = result[0]
            user_data = user_doc.to_dict() or {}
            stored_password = user_data.get("password", "")

            if stored_password and check_password_hash(stored_password, password):
                flash("Login successful.", "success")
                if is_principal_user(user_data):
                    return redirect(url_for("principal_dashboard", user_id=user_doc.id))
                return redirect(url_for("dashboard", user_id=user_doc.id))

            flash("Invalid username or password.", "danger")
        except Exception as error:
            print(f"Login Error: {error}")
            flash("Could not log in right now.", "danger")

    return render_template("login.html")


@app.route("/dashboard/<user_id>")
def dashboard(user_id):
    if not db_ready():
        flash("Database connection failed. Check your Firebase file and Firestore setup.", "danger")
        return redirect(url_for("login"))

    try:
        user_doc = get_user_document(user_id)
        if user_doc is None:
            flash("User not found.", "danger")
            return redirect(url_for("login"))

        user_data = user_doc.to_dict() or {}
        if is_principal_user(user_data):
            return redirect(url_for("principal_dashboard", user_id=user_id))
        user_data.setdefault("username", "")
        user_data.setdefault("name", "")
        user_data.setdefault("subjects", [])
        user_data.setdefault("level", "")
        user_data.setdefault("notes", [])
        return render_template("dashboard.html", user=user_data, user_id=user_id)
    except Exception as error:
        print(f"Dashboard Error: {error}")
        flash("Could not load the dashboard.", "danger")
        return redirect(url_for("login"))


@app.route("/principal-dashboard/<user_id>")
def principal_dashboard(user_id):
    if not db_ready():
        flash("Database connection failed. Check your Firebase file and Firestore setup.", "danger")
        return redirect(url_for("login"))

    try:
        principal_doc = get_user_document(user_id)
        if principal_doc is None:
            flash("Principal account not found.", "danger")
            return redirect(url_for("login"))

        principal_data = principal_doc.to_dict() or {}
        if not is_principal_user(principal_data):
            flash("Access denied.", "danger")
            return redirect(url_for("login"))

        student_documents = db.collection("users").stream()
        students = []
        for document in student_documents:
            student = document.to_dict() or {}
            if is_principal_user(student):
                continue
            student["id"] = document.id
            students.append(student)

        students.sort(key=lambda student: (student.get("name") or student.get("username") or "").lower())
        return render_template(
            "principal_dashboard.html",
            students=students,
            principal_id=user_id,
        )
    except Exception as error:
        print(f"Principal Dashboard Error: {error}")
        flash("Could not load the principal dashboard.", "danger")
        return redirect(url_for("login"))


@app.route("/update/<user_id>", methods=["POST"])
def update(user_id):
    if not db_ready():
        return ("Database unavailable", 500)

    try:
        user_doc = get_user_document(user_id)
        if user_doc is None:
            return ("User not found", 404)

        updates = {}
        if "name" in request.form:
            updates["name"] = request.form.get("name", "").strip()
        if "level" in request.form:
            updates["level"] = request.form.get("level", "").strip()
        if "subjects" in request.form:
            updates["subjects"] = parse_subjects(request.form.get("subjects", ""))

        if updates:
            db.collection("users").document(user_id).update(updates)

        return redirect(url_for("dashboard", user_id=user_id))
    except Exception as error:
        print(f"Update Error: {error}")
        return ("Update failed", 500)


@app.route("/api/notes/<user_id>", methods=["GET", "POST"])
def api_notes(user_id):
    if not db_ready():
        return jsonify({"error": "Database unavailable"}), 500

    try:
        user_doc = get_user_document(user_id)
        if user_doc is None:
            return jsonify({"error": "User not found"}), 404

        user_data = user_doc.to_dict() or {}
        notes = list(user_data.get("notes", []))

        if request.method == "POST":
            payload = request.get_json(silent=True) or {}
            note = (payload.get("note") or "").strip()
            if not note:
                return jsonify({"error": "Note content is required."}), 400

            notes.append(note)
            db.collection("users").document(user_id).update({"notes": notes})
            return jsonify({"status": "ok", "notes": notes})

        return jsonify({"notes": notes})
    except Exception as error:
        print(f"Notes API Error: {error}")
        return jsonify({"error": "Could not load notes"}), 500


@app.route("/api/chat/<user_id>", methods=["GET", "POST", "DELETE"])
def api_chat(user_id):
    if not db_ready():
        return jsonify({"error": "Database unavailable"}), 500

    try:
        user_doc = get_user_document(user_id)
        if user_doc is None:
            return jsonify({"error": "User not found"}), 404

        chat_ref = db.collection("users").document(user_id).collection("chat")

        if request.method == "POST":
            payload = request.get_json(silent=True) or {}
            message = (payload.get("message") or "").strip()
            if not message:
                return jsonify({"error": "Message content is required."}), 400

            chat_ref.add(
                {
                    "message": message,
                    "sender": "student",
                    "timestamp": firestore.SERVER_TIMESTAMP,
                }
            )
            return jsonify({"status": "ok"})

        if request.method == "DELETE":
            payload = request.get_json(silent=True) or {}
            message_id = (payload.get("id") or "").strip()
            if not message_id:
                return jsonify({"error": "Message ID is required."}), 400
            chat_ref.document(message_id).delete()
            return jsonify({"status": "ok"})

        chat_messages = []
        for document in chat_ref.order_by("timestamp").stream():
            message = document.to_dict() or {}
            message["id"] = document.id
            chat_messages.append(message)
        return jsonify({"chat": chat_messages})
    except Exception as error:
        print(f"Chat API Error: {error}")
        return jsonify({"error": "Could not load chat"}), 500


@app.route("/calendar/<user_id>")
def calendar(user_id):
    user_doc = get_user_document(user_id)
    user_data = user_doc.to_dict() if user_doc else {}
    is_principal = is_principal_username(user_id) or is_principal_user(user_data)
    return render_template("calendar.html", user_id=user_id, is_principal=is_principal)


@app.route("/community/<user_id>")
def community(user_id):
    user_doc = get_user_document(user_id)
    user_data = user_doc.to_dict() if user_doc else {}
    return render_template("community.html", user_id=user_id, is_principal=is_principal_user(user_data))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
