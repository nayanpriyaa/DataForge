from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import JSON

from app.db.database import Base


class AnalyticsReport(Base):

    __tablename__ = "analytics_reports"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    dataset_id = Column(
        Integer,
        nullable=False
    )

    analytics_json = Column(
        JSON,
        nullable=False
    )