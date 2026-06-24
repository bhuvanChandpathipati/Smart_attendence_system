from mongodb import students_collection, attendance_collection

students_collection.insert_one({
    "name": "Bhuvan"
})

attendance_collection.insert_one({
    "name": "Bhuvan",
    "date": "2026-06-24",
    "time": "14:00:00"
})

print("Data inserted successfully")