from app.entities.quality_report import QualityReport
from app.repositories.quality_repository import QualityRepository


class QualityService:

    def __init__(self):
        self.repository = QualityRepository()

    def save_report(
        self,
        db,
        dataset_id,
        quality_json
    ):

        report = QualityReport(
            dataset_id=dataset_id,
            quality_json=quality_json
        )

        return self.repository.save(
            db,
            report
        )

    def get_report(
        self,
        db,
        dataset_id
    ):

        return self.repository.find_by_dataset_id(
            db,
            dataset_id
        )