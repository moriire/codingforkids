"""
This file defines the database models
"""

from .common import db, Field
from pydal.validators import *
from . import settings
loc = settings.required_folder(settings.APP_FOLDER, "static/images") 
### Define your table below
#
db.define_table('exam',
    Field("question", type="text"),
    Field("option_a", type="string"),
    Field("option_b", type="string"),
    Field("option_c", type="string"),
    Field("answer", type="string")
)

db.commit()
#
