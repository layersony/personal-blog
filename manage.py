from app import create_app, db
from flask_script import Manager, Server
from app.models import Blog, User, Comment
from flask_migrate import Migrate, MigrateCommand

app = create_app('production')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('server', Server)
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
  return dict(app = app, db=db, blog=Blog, comment=Comment, user=User)

if __name__ == '__main__':
  manager.run()
