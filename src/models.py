from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorite_characters_table = Table(
    "favorite_characters",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True),
)

favorite_locations_table = Table(
    "favorite_locations",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("location_id", ForeignKey("location.id"), primary_key=True),
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    favorite_characters = relationship(
        "Character",
        secondary=favorite_characters_table,
        back_populates="liked_by_users"
    )

    favorite_locations = relationship(
        "Location",
        secondary=favorite_locations_table,
        back_populates="liked_by_users"
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
                "characters": [c.serialize() for c in self.favorite_characters],
                "locations": [l.serialize() for l in self.favorite_locations]
            }
        }


class Location(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)
    use: Mapped[str] = mapped_column(String(180), nullable=False)
    image: Mapped[str] = mapped_column(String(250), nullable=False)
    town: Mapped[str] = mapped_column(String(180), nullable=False)

    liked_by_users = relationship(
        "User",
        secondary=favorite_locations_table,
        back_populates="favorite_locations"
    )

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

    liked_by_users = relationship(
        "User",
        secondary=favorite_characters_table,
        back_populates="favorite_characters"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "quote": self.quote,
            "image": self.image
        }