from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.db.database import Base


class Dataset(Base):

    __tablename__ = "datasets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(
        String,
        nullable=False
    )
    parent_dataset_id = Column(
    Integer,
    nullable=True
)
    file_path = Column(
        String,
        nullable=False
    )

    version = Column(
        Integer,
        default=1
    )

    status = Column(
        String,
        default="uploaded"
    )

    owner_id = Column(
        Integer,
        nullable=False
    )