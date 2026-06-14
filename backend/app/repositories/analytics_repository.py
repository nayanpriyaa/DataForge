from app.entities.analytics_report import AnalyticsReport


class AnalyticsRepository:

    def save(
        self,
        db,
        report
    ):

        db.add(report)

        db.commit()

        db.refresh(report)

        return report

    def find_by_dataset_id(
        self,
        db,
        dataset_id
    ):

        return (
            db.query(AnalyticsReport)
            .filter(
                AnalyticsReport.dataset_id
                == dataset_id
            )
            .first()
        )