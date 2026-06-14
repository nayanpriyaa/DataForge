import os

from app.entities.dataset import Dataset
from app.repositories.dataset_repository import DatasetRepository


class UploadService:

    def __init__(self):
        self.repository = DatasetRepository()

    def upload(
        self,
        db,
        filename,
        file_path,
        owner_id
    ):

        dataset = Dataset(
            filename=filename,
            file_path=file_path,
            owner_id=owner_id
        )

        return self.repository.save(
            db,
            dataset
        )