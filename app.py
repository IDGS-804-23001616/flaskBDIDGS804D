from flask import Flask, render_template,request,redirect,url_for,flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate #agregar referencia de migracion
from flask import g
from maestros import maestros
from alumnos import alumnos
from cursos import cursos
from models import db, Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(maestros, url_prefix="/maestros")
app.register_blueprint(alumnos, url_prefix="/alumnos")
app.register_blueprint(cursos, url_prefix="/cursos")
db.init_app(app)
migrate = Migrate(app, db)#migracion a db 
csrf = CSRFProtect()


@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

@app.route("/", methods=['GET', 'POST'])
@app.route("/index")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
