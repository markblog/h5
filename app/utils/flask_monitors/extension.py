from functools import partial
from .core import save_user_behavior


class Monitor(object):

	def __init__(self, app=None, **kwargs):
		self._options = kwargs
		if app is not None:
			with app.app_context():
				db = kwargs.get('db')
				func = partial(save_user_behavior, db, app.config)
				app.before_request(func)

