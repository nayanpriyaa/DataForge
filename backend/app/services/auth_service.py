from app.entities.user import User

from app.repositories.user_repository import (
    UserRepository
)

from app.core.security import (
    hash_password
)

from app.core.security import (
    verify_password
)

from app.core.security import (
    create_access_token
)


class AuthService:

    def __init__(self):

        self.repository = (
            UserRepository()
        )

    def register(
        self,
        db,
        name,
        email,
        password
    ):

        password_hash = (
            hash_password(
                password
            )
        )

        user = User(
            name=name,
            email=email,
            password_hash=password_hash
        )

        return self.repository.save(
            db,
            user
        )

    def login(
        self,
        db,
        email,
        password
    ):

        user = (
            self.repository
            .find_by_email(
                db,
                email
            )
        )

        if user is None:

            raise ValueError(
                "Invalid email or password"
            )

        if not verify_password(
            password,
            user.password_hash
        ):

            raise ValueError(
                "Invalid email or password"
            )

        token = (
            create_access_token(
                {
                    "sub":
                        str(
                            user.id
                        )
                }
            )
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user
        }