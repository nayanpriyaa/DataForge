from app.entities.data_profile import DataProfile
from app.repositories.profile_repository import ProfileRepository


class ProfileService:

    def __init__(self):
        self.repository = ProfileRepository()

    def save_profile(
        self,
        db,
        dataset_id,
        profile_json
    ):

        profile = DataProfile(
            dataset_id=dataset_id,
            profile_json=profile_json
        )

        return self.repository.save(
            db,
            profile
        )

    def get_profile(
        self,
        db,
        dataset_id
    ):

        return self.repository.find_by_dataset_id(
            db,
            dataset_id
        )