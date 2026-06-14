from app.entities.data_profile import DataProfile


class ProfileRepository:

    def save(
        self,
        db,
        profile
    ):
        db.add(profile)

        db.commit()

        db.refresh(profile)

        return profile

    def find_by_dataset_id(
        self,
        db,
        dataset_id
    ):

        return (
            db.query(DataProfile)
            .filter(
                DataProfile.dataset_id == dataset_id
            )
            .first()
        )