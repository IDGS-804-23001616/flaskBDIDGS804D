from . import maestros
from flask import render_template, request
import forms
from models import Maestros

@maestros.route("/perfil/<nombre>")
def perfil(nombre):
    return f"Perfil de {nombre}"

@maestros.route('/maestros', methods=['GET','POST'])
@maestros.route('/index')
def index():
    create_form = forms.UserForm(request.form)
    maestros = Maestros.query.all()
      
    return render_template('maestros/listadoMaes.html', form=create_form, maestros=maestros)