from flask_sqlalchemy import SQLAlchemy

from ..models import (
    GrainSubstrate,
    Substrate,
)


def pop_grainsubstrate(db:SQLAlchemy):
    gs = [
        GrainSubstrate(grain="", cost=)
    ]
    try:
        db.session.add_all(gs)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)


