from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import JSON

from app.db.database import Base


class DatasetComparison(Base):

    __tablename__ = "dataset_comparisons"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    dataset_id = Column(
        Integer,
        nullable=False
    )

    comparison_json = Column(
        JSON,
        nullable=False
    )