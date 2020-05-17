from app import create_app
app = create_app('DEBUGGING')


if __name__ == '__main__':
	from flask_script import Manager, Server
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

	manager.add_command('runserver', Server(port=5006))
	manager.run(default_command='runserver')
