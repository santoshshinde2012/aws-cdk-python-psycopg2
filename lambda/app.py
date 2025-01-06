import json
from database import Database
from services import RecordService

def lambda_handler(event, context):
    db = Database()
    db.init_db()  # Ensure tables exist
    session = db.SessionLocal()

    try:
        service = RecordService(session)

        if event.get("action") == "write":
            data = event.get("data", {})
            new_record = service.create_record(
                name=data["name"],
                description=data.get("description", "")
            )
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Record created",
                    "record_id": new_record.id
                }),
            }

        elif event.get("action") == "read":
            records = service.get_all_records()
            result = [
                {"id": r.id, "name": r.name, "description": r.description}
                for r in records
            ]
            return {
                "statusCode": 200,
                "body": json.dumps({"records": result}),
            }

        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid action. Use 'write' or 'read'."}),
            }

    except Exception as e:
        session.rollback()
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    finally:
        session.close()
