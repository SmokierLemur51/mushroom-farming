""" File: models/mushrooms.py ** Author: Logan Lee (Lemur) ** Date: 8-September-2024  

Define mushrooms for populating the database.

"""
from flask_sqlalchemy import SQLAlchemy

from .models import Phylum, FungiClass, MushroomOrder, Genus, Mushroom

# Common mushrooms: oyster, shiitake, lions mane, beech, enoki, morel, penny bun, honey

def new_mushroom():
	pass

def populate_phylums(db: SQLAlchemy):
	p = [
		Phylum(name='basidiomycota'), 
		Phylum(name='ascomycota'),
	]
	try:
		db.session.add_all(p)
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(e)


def populate_fungi_classes(db: SQLAlchemy):
	c = [
		FungiClass()
	]
	try:
		db.session.add_all(c)
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(e)