from app.entities.quality_report import QualityReport


class QualityRepository:

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
            db.query(QualityReport)
            .filter(
                QualityReport.dataset_id == dataset_id
            )
            .first()
        )