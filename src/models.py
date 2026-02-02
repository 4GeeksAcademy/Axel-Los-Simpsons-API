from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorites_table = Table(
    "favorites_table",
    db.metadata,
    Column("Location_id", ForeignKey("location.id"), nullable=True),
    Column("Character_id", ForeignKey("character.id"), nullable=True),
    Column("User_id", ForeignKey("user.id"), nullable=False),
    Column("id", db.Integer, primary_key=True)
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    character_liked: Mapped[list["Character"]] = relationship(
        "Character",
        secondary=favorites_table,
        back_populates="character_liked"
    )
    location_liked: Mapped[list["Location"]] = relationship(
        "Location",
        secondary=favorites_table,
        back_populates="location_liked"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.user,
            "email": self.email
        }

    def favorites_serialize(self):
        return {
            "favorites": {
                "characters": [character for character in self.character_liked],
                "locations": [location for location in self.location_liked]
            }
        }


class Location(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)
    use: Mapped[str] = mapped_column(String(180), nullable=False)
    image: Mapped[str] = mapped_column(String(250), nullable=False)
    town: Mapped[str] = mapped_column(String(180), nullable=False)
    location_liked: Mapped[list[User]] = relationship(
        "User", secondary=favorites_table, back_populates="location_liked")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "use": self.use,
            "image": self.image,
            "town": self.town
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    quote: Mapped[str] = mapped_column(String(180), nullable=False)
    image: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    character_liked: Mapped[list[User]] = relationship(
        "User", secondary=favorites_table, back_populates="character_liked")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "quote": self.quote,
            "image": self.image
        }
