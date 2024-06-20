from typing import Any, Dict, Type, TypeVar
from flask import Flask

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_sqlalchemy import SQLAlchemy
from date_utils import timestamp_to_date
import os


db = SQLAlchemy()

T = TypeVar('T', bound="EntityMixin")

class EntityMixin:

    __abstract__ = True

    @classmethod
    def findById(cls: Type[T], id) -> T:
        """Find an entity by its ID."""
        try:
            entity = db.session.query(cls).filter(cls.id == id).first()
            print(f"Entity found by ID {id}: {entity}")
            return entity
        except SQLAlchemyError as e:
            print(f"Error finding entity by ID {id}: {e}")
            return None

    @classmethod
    def findAll(cls: Type[T], offset: int = 0, limit: int = 100) -> list[T]:
        """Find all entities with an optional pagination."""
        try:
            entities = db.session.query(cls).offset(offset).limit(limit).all()
            print(f"Entities found with offset {offset} and limit {limit}: {entities}")
            return entities
        except SQLAlchemyError as e:
            print(f"Error finding all entities: {e}")
            return []

    @classmethod
    def findBy(cls: Type[T], **filters: Any) -> T | list[T]:
        """Find entities by the given filters."""
        try:
            entities = db.session.query(cls).filter_by(**filters).all()
            print(f"Entities found with filters {filters}: {entities}")
            if len(entities) > 1:
                return entities
            return entities[0] if entities else None

        except Exception as e:
            print(f"Error finding entities with filters {filters}: {e}")
            return []

    @classmethod
    def deleteById(cls: Type[T], id: int) -> None:
        exists: T | None = db.session.query(cls).filter(cls.id == id).first()
        if exists:
            db.session.delete(exists)
            db.session.commit()

    def save(self) -> None:
        """Save the current entity instance."""
        try:
            if not db.session.object_session(self):
                db.session.add(self)

            db.session.commit()
            db.session.refresh(self)
            print(f"Entity saved and refreshed: {self}")
            return True

        except IntegrityError as e:
            print(f"Integrity error saving entity {self}: {e}")
            db.session.rollback()
            return False

        except SQLAlchemyError as e:
            print(f"Error saving entity {self}: {e}")
            db.session.rollback()
            return False

    def delete(self) -> None:
        """Delete the current entity instance."""
        try:
            with db.session.begin():
                db.session.delete(self)
            print(f"Entity deleted: {self}")
            return True
        except SQLAlchemyError as e:
            print(f"Error deleting entity {self}: {e}")
            db.session.rollback()
            return False

    def __str__(self) -> str:
        class_name = type(self).__name__
        attributes = ', '.join(f"{attr}={getattr(self, attr)}" for attr in self.__dict__)
        return f"{class_name}({attributes})"

    def to_dict(self) -> dict[str, Any]:
        """Convert the entity instance to a dictionary."""
        entity_dict = {}
        for column in self.__table__.columns:
            entity_dict[column.name] = getattr(self, column.name)
        return entity_dict


days_images = db.Table(
    'day_image',
    db.Column('day_id', db.Integer, db.ForeignKey('day.id')),
    db.Column('image_id', db.Integer, db.ForeignKey('image.id'))
)

days_tags = db.Table(
    'day_tag',
    db.Column('day_id', db.Integer, db.ForeignKey('day.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

album_image_association = db.Table(
    'album_image',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id')),
    db.Column('image_id', db.Integer, db.ForeignKey('image.id'))
)


class Image(db.Model, EntityMixin):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    source = db.Column(db.String, nullable=False)
    main_image = db.Column(db.Integer, nullable=False)
    albums = db.relationship("Album", secondary=album_image_association, back_populates="images")
    days = db.relationship("Day", secondary=days_images, back_populates="images")

    def __init__(
            self,
            source: str = "../../NoPhoto.png",
            main_image: int = 0
        ) -> None:
        self.source = source
        self.main_image = main_image

    @classmethod
    def findByName(cls, name: str) -> "list[Image]":
        found_image = db.session.query(Image).filter(Image.source == name).all()
        return found_image

    def delete(self, isAllowedToDeleteFile: bool = False) -> dict[str, str]:

        if self in self.days:
            return {"success": False, "message": "This image presents in a day"}

        if "http" not in self.source:
            try:
                if isAllowedToDeleteFile:
                    os.remove("app/static/images/calendar/vlad/" + self.source)

            except Exception as e:
                print("Error deleting image:", e)
                return {"success": False, "message": f"Image doesn't exist in the image storage. Try NOT to allow to delete the file so that it'll delete in DB, but not in the file itself. Error: {e}"}

        super().delete()
        if isAllowedToDeleteFile:
            return {"success": True, "message": "Image and file deleted successfully"}
        else:
            return {"success": True, "message": "Image deleted successfully"}

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source,
            "main_image": self.main_image,
        }

class City(db.Model, EntityMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)

class Tag(db.Model, EntityMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    days = db.relationship("Day", secondary=days_tags, back_populates="tags")

class Album(db.Model, EntityMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)
    images = db.relationship("Image", secondary=album_image_association, back_populates="albums")

    def __init__(
            self,
            name: str = "Unnamed album",
            images: list = []
        ) -> None:
        self.name = name
        self.images = images

    def findFirstImage(self) -> Image:
        if self.images:
            return self.images[0]

        return Image()

    def deleteImagesByNames(
            self,
            image_names: list[str],
            isAllowedToDeleteFiles: bool = False
        ) -> dict[str, str]:
        print("deleteImagesByNames image_names:", image_names)
        for image_name in image_names:

            images_by_name = Image.findBy(name=image_name)

            if isinstance(images_by_name, Image):
                images_by_name = [images_by_name]

            for image in images_by_name:
                if image not in self.images:
                    continue

                self.images.remove(image)
                result = image.delete(isAllowedToDeleteFiles)
                print("result in deleteImagesByNames:", result)

                if result["success"]:
                    continue
                else:
                    return {"success": False, "message": result["message"]}

        db.session.commit()
        return {"success": True, "message": "Images deleted successfully"}


    def findThreeImages(self) -> list[Image]:
        if len(self.images) >= 3:
            return self.images[:3]
        return self.images


    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
        }


class Day(db.Model, EntityMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    city_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    steps = db.Column(db.Integer, nullable=False)
    images = db.relationship("Image", secondary=days_images, back_populates="days")
    tags = db.relationship("Tag", secondary=days_tags, back_populates="days")

    def __init__(
            self,
            timestamp: int,
            city_id: int = 2,
            desc: str = "No description",
            content: str = "No content",
            steps: int = 0,
            images: list[Image] = []
        ) -> None:
        self.id = timestamp
        self.city_id = city_id
        self.description = desc
        self.content = content
        self.steps = steps
        self.images = images

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "city_id": self.city_id,
            "description": self.description,
            "content": self.content,
            "steps": self.steps,
        }

    def getDate(self) -> str:
        return f"{self.getYear()}-{self.getMonth()}-{self.getDayNumber()}"

    def getYear(self) -> int:
        return timestamp_to_date(self.id)[0]

    def getMonth(self) -> int:
        return timestamp_to_date(self.id)[1]

    def getDayNumber(self) -> int:
        return timestamp_to_date(self.id)[2]

    def getCity(self) -> str:
        return City.findById(self.city_id).name

    def getTagNames(self) -> list[str]:
        return [tag.name for tag in self.tags]

    def findMainImage(self) -> Image:
        for image in self.images:
            if image.main_image:
                return image
        return Image()

    def setMainImage(self, mainImage: Image) -> bool:
        for i, image in enumerate(self.images):
            if image.main_image:
                self.images[i] = mainImage
                return True

        self.images.append(mainImage)
        db.session.commit()
        return False

    def findOtherImages(self) -> list[Image]:
        other_images = []
        for image in self.images:
            if not image.main_image:
                other_images.append(image)

        db.session.commit()
        return other_images


    @classmethod
    def findAllByDateRange(cls, start_date: int, end_date: int) -> "list[Day]":
        days = db.session.query(cls).filter(cls.id >= start_date, cls.id <= end_date).all()
        return days

    @property
    def city_name(self) -> str:
        return self.getCity()



def insert_default_cities() -> None:
    cities = [
        'Kyiv',
        'Irpin',
        'Krakow',
        'Warsaw',
        'Wroclaw'
    ]
    for city_name in cities:
        city = City(name=city_name)
        db.session.add(city)


def insert_default_tags() -> None:
    tags = [
        'home',
        'school',
        'coding',
        'gaming',
        'travel',
        'biking'
    ]
    for tag_name in tags:
        tag = Tag(name=tag_name)
        db.session.add(tag)



def create_db(app: Flask) -> None:
    db.init_app(app)

    with app.app_context():
        db.create_all()

        if not City.findAll():
            insert_default_cities()
            db.session.commit()

        if not Tag.findAll():
            insert_default_tags()
            db.session.commit()