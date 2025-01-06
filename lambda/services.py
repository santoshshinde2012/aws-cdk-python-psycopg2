from sqlalchemy.orm import Session
from models import Record

class RecordService:
    def __init__(self, db_session: Session):
        self.session = db_session

    def create_record(self, name: str, description: str = "") -> Record:
        """Creates a new record."""
        new_record = Record(name=name, description=description)
        self.session.add(new_record)
        self.session.commit()
        self.session.refresh(new_record)
        return new_record

    def get_all_records(self) -> list:
        """Fetches all records."""
        return self.session.query(Record).all()
