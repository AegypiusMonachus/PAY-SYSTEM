from app import create_app
app = create_app('DEBUGGING')


if __name__ == '__main__':
	from flask_script import Manager
	manager = Manager(app)

	@manager.shell
	def _make_context():
		return dict(app=app)

	@manager.command
	def test():
		import unittest
		loader = unittest.TestLoader()
		runner = unittest.TextTestRunner()
		runner.run(loader.discover('tests', pattern='test*'))

	manager.run()
