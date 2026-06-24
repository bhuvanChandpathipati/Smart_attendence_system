from mongodb import attendance_collection
import pandas as pd
import matplotlib.pyplot as plt

data = list(attendance_collection.find())

df = pd.DataFrame(data)

counts = df["name"].value_counts()

plt.figure(figsize=(8,5))
counts.plot(kind="bar")

plt.title("Attendance Count")
plt.xlabel("Student")
plt.ylabel("Days Present")

plt.tight_layout()
plt.savefig("static/attendance_chart.png")

print("Chart Generated")