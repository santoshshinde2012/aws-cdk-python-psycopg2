import json
import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import the shared get_secret function
from shared.get_dburl import get_dburl

# SQLAlchemy Base and Session setup
Base = declarative_base()

secret_name = os.getenv("SECRET_NAME")

if not secret_name:
    raise ValueError("Environment variable SECRET_NAME is not set!")

# Get the database URL from Secrets Manager
try:
    DATABASE_URL = get_dburl(secret_name)
except Exception as e:
    raise ValueError(f"Error fetching secret: {str(e)}")

# SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Define the database model (example: 'records' table)
class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)


# Ensure the table exists (useful for local testing)
Base.metadata.create_all(bind=engine)


# Lambda handler
def lambda_handler(event, context):
    session = SessionLocal()
    try:
        # Parse the event to handle writing and reading records
        if event.get("action") == "write":
            # Write a record to the database
            new_record = Record(
                name=event["data"]["name"],
                description=event["data"].get("description", ""),
            )
            session.add(new_record)
            session.commit()
            session.refresh(new_record)

            return {
                "statusCode": 200,
                "body": json.dumps(
                    {"message": "Record created", "record_id": new_record.id}
                ),
            }

        elif event.get("action") == "read":
            # Read records from the database
            records = session.query(Record).all()
            result = [
                {"id": r.id, "name": r.name, "description": r.description}
                for r in records
            ]

            return {"statusCode": 200, "body": json.dumps({"records": result})}

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
