from app.entities.dataset import Dataset


class DatasetRepository:

    def save(
        self,
        db,
        dataset
    ):
        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        return dataset

    def find_by_id(
        self,
        db,
        dataset_id
    ):

        return (
            db.query(Dataset)
            .filter(
                Dataset.id == dataset_id
            )
            .first()
        )

    def find_latest_version(
        self,
        db,
        filename
    ):

        return (
            db.query(Dataset)
            .filter(
                Dataset.filename == filename
            )
            .order_by(
                Dataset.version.desc()
            )
            .first()
        )

    def find_all(
    self,
    db
):

        return (
        db.query(Dataset)
        .order_by(
            Dataset.id.desc()
        )
        .all()
    )