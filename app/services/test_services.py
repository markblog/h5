from app.ext import raw_db
from flask import request, g

def test_db_text():

	result = raw_db.paginate('SELECT * FROM public.user')