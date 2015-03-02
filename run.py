#!flask/bin/python
from app import app, manager
from flask.ext.migrate import MigrateCommand
 
manager.add_command('db', MigrateCommand)
app.host = '0.0.0.0'
app.debug = 'True'
#manager.run()
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
    app.secret_key = 123456
    #manager.run()
