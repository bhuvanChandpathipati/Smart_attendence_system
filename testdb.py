from mongodb import db

print("✅ Connected Successfully")
print("Collections:", db.list_collection_names())