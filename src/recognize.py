import cv2
import os
from datetime import datetime
from mongodb import attendance_collection


def mark_attendance(name):

    if name == "Unknown":
        return

    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    record = attendance_collection.find_one({
        "name": name,
        "date": today
    })

    if record is None:

        attendance_collection.insert_one({
            "name": name,
            "date": today,
            "time": current_time
        })

        print(f"✅ Attendance Marked: {name}")


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

print("Current Directory:", os.getcwd())
print("✅ Model loaded successfully")


names = {}

if os.path.exists("labels.txt"):
    with open("labels.txt", "r") as f:
        for line in f:
            label, name = line.strip().split(",")
            names[int(label)] = name

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

attendance_marked = set()

print("🎥 Camera Started... Press Q to Exit")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(50, 50)
    )

    for (x, y, w, h) in faces:

        face_roi = gray[
            y:y+h,
            x:x+w
        ]

        face_roi = cv2.resize(
            face_roi,
            (200, 200)
        )

        label, confidence = recognizer.predict(
            face_roi
        )

        if confidence < 80:

            name = names.get(
                label,
                "Unknown"
            )

            if (
                name != "Unknown"
                and name not in attendance_marked
            ):

                mark_attendance(name)
                attendance_marked.add(name)

        else:
            name = "Unknown"

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            name,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "Smart Attendance System",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("✅ Program Closed")