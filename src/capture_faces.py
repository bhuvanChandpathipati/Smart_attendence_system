import cv2
import os

def capture_faces(student_name):
    folder_path = f"dataset/{student_name}"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    cap = cv2.VideoCapture(0)

    count = 0
    max_images = 50

    print("Starting face capture...")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]

            image_path = os.path.join(
                folder_path,
                f"{count}.jpg"
            )

            cv2.imwrite(image_path, face)

            count += 1

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Images: {count}/{max_images}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        cv2.imshow("Capturing Faces", frame)

        if count >= max_images:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print("Face capture completed!")

if __name__ == "__main__":
    capture_faces("Bhuvan")