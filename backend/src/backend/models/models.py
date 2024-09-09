"""
File: models.py
Author: Logan Lee

This file defines the models to be used in the web application.
"""
import datetime
from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from flask_login import UserMixin

from ..extensions import login_manager


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    info: Mapped[str] = mapped_column(String(250), nullable=True)

    users: Mapped[List["User"]] = relationship(back_populates="role")
    
    def __repr__(self) -> str:
        return self.name


class User(Base, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))    
    username: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    secret_key: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    
    role: Mapped["Role"] = relationship(back_populates="users")                                        
    
    def __repr__(self) -> str:
        return self.public_username


@login_manager.user_loader
def load_user(user_id):
    return db.session.scalar(db.select(User).where(User.id == user_id))


class Unit(Base):
    """ A unit is designed to be extensible. Weight, length, currency, etc. The unit itself
        is just a name. UnitConversion obj will handle the actual converting between units. 
        The 'category' field is a string that you can use to group units together. 
    """
    __tablename__ = "units"
    id: Mapped[int] = mapped_column(primary_key=True)
    unit: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String(120), nullable=True)

    def __repr__(self) -> str:
        return self.unit


class UnitConversion(Base):
    """ The UnitConversion is how we will convert Units. 
            -Unit_1 is the given
            -Unit_2 is the desired.
            -Multi is the float amount to multiply the Unit_1 to convert into Unit_2
    """
    __tablename__ = "unit_conversions"
    id: Mapped[int] = mapped_column(primary_key=True)
    unit_1_id: Mapped[int] = mapped_column(ForeignKey('units.id'))
    unit_2_id: Mapped[int] = mapped_column(ForeignKey('units.id'))
    multi: Mapped[float] = mapped_column(Float)

    def __repr__(self) -> str:
        return "Multi for converting '{}' -> '{}' is {}".format(self.unit_1_id, self.unit_2_id, self.multi)


class Phylum(Base):
    __tablename__ = "phylums"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    info: Mapped[str] = mapped_column(String(1000), nullable=True)

    fungi_classes: Mapped[List['FungiClass']] = relationship(back_populates='phylum')
    mushroom_orders: Mapped[List['MushroomOrder']] = relationship(back_populates='phylum')
    families: Mapped[List['Family']] = relationship(back_populates='phylum')
    genuses: Mapped[List['Mushroom']] = relationship(back_populates='phylum')
    mushrooms: Mapped[List['Mushroom']] = relationship(back_populates='phylum')

    def __repr__(self) -> str:
        return self.division


class FungiClass(Base):
    __tablename__ = "fungi_classes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    phylum_id: Mapped[int] = mapped_column(ForeignKey('phylums.id'))
    info: Mapped[str] = mapped_column(String(1000), nullable=True)
    
    phylum: Mapped['Phylum'] = relationship(back_populates='fungi_classes')
    mushroom_orders: Mapped[List['MushroomOrder']] = relationship(back_populates='phylum')
    mushrooms: Mapped[List['Mushroom']] = relationship(back_populates='fungi_class')

    def __repr__(self) -> str:
        return self.division


class MushroomOrder(Base):
    __tablename__ = "mushroom_orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    info: Mapped[str] = mapped_column(String(1000), nullable=True)
    
    mushrooms: Mapped[List['Mushroom']] = relationship(back_populates='mushroom_order')

    def __repr__(self) -> str:
        return self.division


class Family(Base):
    __tablename__ = "families"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    info: Mapped[str] = mapped_column(String(1000), nullable=True)
    
    mushrooms: Mapped[List['Mushroom']] = relationship(back_populates='family')

    def __repr__(self) -> str:
        return self.division


class Genus(Base):
    __tablename__ = "genus"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    info: Mapped[str] = mapped_column(String(1000), nullable=True)
    
    mushrooms: Mapped[List['Mushroom']] = relationship(back_populates='genus')

    def __repr__(self) -> str:
        return self.division


class Mushroom(Base):
    __tablename__ = "mushrooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    phylum_id: Mapped[str] = mapped_column(ForeignKey('phylums.id'), nullable=False)
    fungi_class_id: Mapped[str] = mapped_column(ForeignKey('fungi_classes.id'), nullable=False)
    mushroom_order_id: Mapped[str] = mapped_column(ForeignKey('mushroom_orders.id'))
    family_id: Mapped[int] = mapped_column(ForeignKey('families.id'))
    genus_id: Mapped[str] = mapped_column(ForeignKey('genus.id'), nullable=False)
    species: Mapped[str] = mapped_column(String(120), unique=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    info: Mapped[str] = mapped_column(String(1000), nullable=True)
    

class GrowRoom(Base):
    """ A GrowRoom object is intended to be used as a way to track harvests, contamination,
        and operational efficiency. Hopefully it can help to find areas needing improvement 
    """
    __tablename__ = "growrooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    shelves: Mapped[List['Shelf']] = relationship(back_populates="growroom")

    def __repr__(self) -> str:
        return self.name


class Shelf(Base):
    """ Shelves will part of the grow operation, each are given an x, y, and z coordinate.
        Used to track batches on a finer level.

        **The coordinates are strings so that they can be named, numbered, or uuid barcode.
    """
    __tablename__ = "shelves"
    id: Mapped[int] = mapped_column(primary_key=True)
    growroom_id: Mapped[int] = mapped_column(ForeignKey("growrooms.id"))
    x: Mapped[str] = mapped_column(String(100))
    y: Mapped[str] = mapped_column(String(100))
    z: Mapped[str] = mapped_column(String(100))

    growroom: Mapped['GrowRoom'] = relationship(back_populates="shelves")

    def __repr__(self) -> str:
        return f"(X: {self.x}, Y: {self.y}, Z: {self.z})"


class GrainSubstrate(Base):
    """
    """
    __tablename__ = "grain_substrates"
    id: Mapped[int] = mapped_column(primary_key=True)
    grain: Mapped[str] = mapped_column(String(120), unique=True)
    cost: Mapped[float] = mapped_column(Float, default=0.0)

    # grainspawns: Mapped[List[]] = 

    def __repr__(self) -> str:
        return ""


class Substrate(Base):
    """ Substrate is a material that will be combined with other Substrate in the
        BulkSubstrate for the GrainSpawn to colonize.  
    """
    __tablename__ = "grain_substrates"
    id: Mapped[int] = mapped_column(primary_key=True)
    grain: Mapped[str] = mapped_column(String(120), unique=True)



class BulkSubstrate(Base):
    """
    """
    __tablename__ = "bulk_substrates"
    id: Mapped[int] = mapped_column(primary_key=True)
