from app.repositories.dataset_repository import DatasetRepository
from app.entities.dataset import Dataset


class DatasetService:

    def __init__(self):
        self.repository = DatasetRepository()

    def get_dataset(
        self,
        db,
        dataset_id
    ):

        return self.repository.find_by_id(
            db,
            dataset_id
        )

    def get_latest_version(
        self,
        db,
        filename
    ):

        return self.repository.find_latest_version(
            db,
            filename
        )

    def create_dataset(
        self,
        db,
        filename,
        file_path,
        version,
        owner_id,
        status,
        parent_dataset_id=None
    ):

        dataset = Dataset(
            filename=filename,
            file_path=file_path,
            version=version,
            owner_id=owner_id,
            status=status,
            parent_dataset_id=parent_dataset_id
        )

        return self.repository.save(
            db,
            dataset
        )

    def get_all_datasets(
    self,
    db
):

       return self.repository.find_all(
        db
    )