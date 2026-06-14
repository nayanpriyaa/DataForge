from app.entities.analytics_report import AnalyticsReport
from app.repositories.analytics_repository import AnalyticsRepository


class AnalyticsReportService:

    def __init__(self):

        self.repository = (
            AnalyticsRepository()
        )

    def save_report(
        self,
        db,
        dataset_id,
        analytics_json
    ):

        report = AnalyticsReport(
            dataset_id=dataset_id,
            analytics_json=analytics_json
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

        return (
            self.repository
            .find_by_dataset_id(
                db,
                dataset_id
            )
        )