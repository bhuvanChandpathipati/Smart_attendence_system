from flask import Flask, render_template, request, redirect, url_for, session
from mongodb import students_collection, attendance_collection
from openpyxl import Workbook
from flask import send_file
import subprocess
import os
from datetime import datetime

app = Flask(__name__)

app.secret_key = "smart_attendance_secret_key"


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["user"] = username
            return redirect(url_for("dashboard"))

        return "Invalid Credentials"

    return render_template("login.html")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():

    session.pop("user", None)
    return redirect(url_for("login"))


# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    total_students = students_collection.count_documents({})

    total_attendance = attendance_collection.count_documents({})

    today = datetime.now().strftime("%Y-%m-%d")

    today_attendance = attendance_collection.count_documents({
        "date": today
    })

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_attendance=total_attendance,
        today_attendance=today_attendance
    )


# =========================
# ATTENDANCE
# =========================
@app.route("/attendance")
def attendance():

    if "user" not in session:
        return redirect(url_for("login"))

    data = list(
        attendance_collection.find().sort("_id", -1)
    )

    return render_template(
        "attendance.html",
        data=data
    )


# =========================
# SEARCH STUDENT
# =========================
@app.route("/search_student")
def search_student():

    if "user" not in session:
        return redirect(url_for("login"))

    name = request.args.get("name", "")

    if name:

        data = list(
            attendance_collection.find(
                {
                    "name": {
                        "$regex": name,
                        "$options": "i"
                    }
                }
            ).sort("_id", -1)
        )

    else:
        data = []

    return render_template(
        "search.html",
        data=data
    )


# =========================
# REGISTER STUDENT
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        student_name = request.form["name"].strip()

        if student_name == "":
            return "Invalid Name"

        folder = os.path.join(
            "dataset",
            student_name
        )

        if not os.path.exists(folder):
            os.makedirs(folder)

        existing = students_collection.find_one({
            "name": student_name
        })

        if not existing:

            students_collection.insert_one({
                "name": student_name
            })

        return render_template(
            "register_success.html",
            student_name=student_name
        )

    return render_template("register.html")


# =========================
# STUDENTS
# =========================
@app.route("/students")
def students():

    if "user" not in session:
        return redirect(url_for("login"))

    data = list(
        students_collection.find()
    )

    return render_template(
        "students.html",
        students=data
    )
@app.route("/export_excel")
def export_excel():

    if "user" not in session:
        return redirect(url_for("login"))

    data = list(
        attendance_collection.find().sort("_id", -1)
    )

    wb = Workbook()
    ws = wb.active

    ws.title = "Attendance"

    ws.append(["Name", "Date", "Time"])

    for row in data:

        ws.append([
            row["name"],
            row["date"],
            row["time"]
        ])

    file_name = "attendance_report.xlsx"

    wb.save(file_name)

    return send_file(
        file_name,
        as_attachment=True
    )

# =========================
# CAPTURE FACES
# =========================
@app.route("/capture/<name>")
def capture(name):

    if "user" not in session:
        return redirect(url_for("login"))

    subprocess.Popen([
        "python",
        "src/capture_faces.py",
        name
    ])

    return f"""
    <h2>Capturing Faces for {name}</h2>
    <a href='/dashboard'><button>Back</button></a>
    """


# =========================
# TRAIN MODEL
# =========================
@app.route("/train")
def train():

    if "user" not in session:
        return redirect(url_for("login"))

    subprocess.run([
        "python",
        "src/train_model.py"
    ])

    return """
    <h2>Model Trained Successfully</h2>
    <a href='/dashboard'><button>Back</button></a>
    """


# =========================
# START ATTENDANCE
# =========================
@app.route("/start_attendance")
def start_attendance():

    if "user" not in session:
        return redirect(url_for("login"))

    subprocess.Popen([
        "python",
        "src/recognize.py"
    ])

    return redirect(
        url_for("attendance")
    )
@app.route("/analytics")
def analytics():

    if "user" not in session:
        return redirect(url_for("login"))

    pipeline = [
        {
            "$group": {
                "_id": "$name",
                "count": {"$sum": 1}
            }
        }
    ]

    data = list(attendance_collection.aggregate(pipeline))

    return render_template(
        "analytics.html",
        data=data
    )

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return redirect(url_for("login"))


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)