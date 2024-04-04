from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, ForeignKey, DateTime

from src.database.db import Base
from src.api.schemas.user import User


class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True, nullable=False, autoincrement=True, index=True)
    title: Mapped[String] = mapped_column(String, nullable=False)
    description: Mapped[String] = mapped_column(String, nullable=True)
    status: Mapped[String] = mapped_column(String, nullable=False, default="pending")

    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    user_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)


class Users(Base):
    __tablename__ = "users"

    username: Mapped[String] = mapped_column(String, primary_key=True, index=True, nullable=False)
    password: Mapped[String] = mapped_column(String, nullable=False)

    def to_read_model(self) -> User:
        return User(
            username=self.username,
            password=self.password
        )
