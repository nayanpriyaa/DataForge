from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import JSON

from app.db.database import Base


class DataProfile(Base):

    __tablename__ = "data_profiles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    dataset_id = Column(
        Integer,
        nullable=False
    )

    profile_json = Column(
        JSON,
        nullable=False
    )