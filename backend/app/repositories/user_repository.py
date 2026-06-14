from app.entities.user import User


class UserRepository:

    def save(self, db, user):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def find_by_email(
        self,
        db,
        email
    ):
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )