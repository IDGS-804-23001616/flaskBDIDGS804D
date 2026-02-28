from . import maestros
from flask import render_template, request, redirect, url_for
import forms
from models import db, Maestros


@maestros.route("/perfil/<nombre>")
def perfil(nombre):
    return f"Perfil de {nombre}"

@maestros.route('/', methods=['GET','POST'])
@maestros.route('/index')
def index():
    create_form = forms.UserForm(request.form)
    maestros = Maestros.query.all()
      
    return render_template('maestros/listadoMaes.html', form=create_form, maestros=maestros)

@maestros.route("/agregar", methods = ["GET", "POST"])
def maestro():
    create_form = forms.UserForm(request.form)
    if request.method == "POST":
        mae = Maestros(
        nombre = create_form.nombre.data,
        apellidos = create_form.apellidos.data,
        especialiad = create_form.especialiad.data,
        correo = create_form.correo.data,
        matricula = create_form.matricula.data)
        db.session.add(mae)
        db.session.commit()
        return redirect(url_for("maestros.index"))
    return render_template("maestros/agregarMa.html", form = create_form)

@maestros.route("/detalles", methods=["GET", "POST"])
def detallesMae():
    create_form = forms.UserForm(request.form)
    if request.method == "GET":
        matricula = request.args.get("id")
        
        maes = Maestros.query.filter_by(matricula=matricula).first() 
        
        matricula = maes.matricula
        nombre = maes.nombre
        apellidos = maes.apellidos
        correo = maes.correo
        especialiad = maes.especialiad

    return render_template("maestros/detallesmae.html", nombre=nombre, apellidos=apellidos, correo=correo, especialiad=especialiad)

@maestros.route("/modificar", methods=["GET", "POST"])
def modificarMae():
    
    create_form = forms.UserForm(request.form)
    matricula = request.args.get("id")
    maes = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()

    if request.method == "GET":
        create_form.matricula.data = maes.matricula
        create_form.nombre.data = maes.nombre
        create_form.apellidos.data = maes.apellidos
        create_form.correo.data = maes.correo
        create_form.especialiad.data = maes.especialiad


    if request.method == "POST":
        maes.matricula = create_form.matricula.data
        maes.nombre = create_form.nombre.data
        maes.apellidos = create_form.apellidos.data
        maes.correo = create_form.correo.data
        maes.especialiad = create_form.especialiad.data

        db.session.add(maes)
        db.session.commit()
        return redirect(url_for("maestros.index"))

    return render_template("maestros/modificarmae.html", form=create_form)


@maestros.route("/eliminar", methods=["GET", "POST"])
def eliminarMae():
    create_form = forms.UserForm(request.form)
    matricula = request.args.get("id")
    maes = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()

    if request.method == "GET":
        create_form.matricula.data = maes.matricula
        create_form.nombre.data = maes.nombre
        create_form.apellidos.data = maes.apellidos
        create_form.correo.data = maes.correo
        create_form.especialiad.data = maes.especialiad


    if request.method == "POST":
        db.session.delete(maes)
        db.session.commit()
        return redirect(url_for("maestros.index"))

    return render_template("maestros/eliminarmae.html", form=create_form)
