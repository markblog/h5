from flask_script import Command

class MonitorCommand(Command):
	"""A basic class for monitor command"""
	def __init__(self):
		super().__init__()

	def run(self):
		raise Exception('Please implement run function in your monitor command class')


class BehaviorMonitorCommand(MonitorCommand):
	"""create the table for record the user behavior"""

	def __init__(self, db = None):
		self.db = db

	def run(self):

		if self.db:

			class UserLogModel(self.db.Model):
				__tablename__ = 'user_log'
			
				id = self.db.Column(self.db.Integer, primary_key=True, autoincrement=True)
				user_id = self.db.Column(self.db.Integer, nullable=True)
				method = self.db.Column(self.db.String(10), nullable=True)
				path = self.db.Column(self.db.String(64), nullable=True)
				args = self.db.Column(self.db.String(1024), nullable=True)
				request_json = self.db.Column(self.db.JSON, nullable=True)
				form = self.db.Column(self.db.String(1024), nullable=True)
				cookies = self.db.Column(self.db.String(512), nullable=True)
				date = self.db.Column(self.db.DateTime, nullable = True)
			 
			self.db.create_all()
			print('user_log table has been created successfully.')

		else:
			raise Exception('Please pass the db engine you want to create log table in it.')