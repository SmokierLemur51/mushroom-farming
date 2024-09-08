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


class GrowRoom(Base):
    pass


class Shelf(Base):
    pass

class Phylum(Base):
    __tablename__ = "phylums"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)

    mushrooms: Mapped[List['Mushroom']] = relationship(back_populates='phylum')

    def __repr__(self) -> str:
        return self.division

class FungiClass(Base):
    __tablename__ = "fungi_classes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)

    mushrooms: Mapped[List['Mushroom']] = relationship(back_populates='fungi_class')

    def __repr__(self) -> str:
        return self.division


class MushroomOrder(Base):
    __tablename__ = "mushroom_orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)

    mushrooms: Mapped[List['Mushroom']] = relationship(back_populates='mushroom_order')

    def __repr__(self) -> str:
        return self.division


class Family(Base):
    __tablename__ = "families"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)

    mushrooms: Mapped[List['Mushroom']] = relationship(back_populates='family')

    def __repr__(self) -> str:
        return self.division


class Genus(Base):
    __tablename__ = "genus"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)

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
