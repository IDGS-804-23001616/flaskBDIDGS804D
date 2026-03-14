from . import maestros
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from .forms import MaestroForm
from models import db, Maestros


@maestros.route("/perfil/<nombre>")
def perfil(nombre):
    return f"Perfil de {nombre}"

@maestros.route('/', methods=['GET','POST'])
@maestros.route('/index')
def index():
    create_form = MaestroForm(request.form)
    maestros = Maestros.query.all()
      
    return render_template('maestros/index.html', form=create_form, maestros=maestros)

@maestros.route("/agregar", methods=["GET", "POST"])
def agregar():
    create_form = MaestroForm(request.form)

    if request.method == "POST" and create_form.validate():
        mae = Maestros(
            matricula=int(create_form.matricula.data),
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            especialidad=create_form.especialidad.data,
            correo=create_form.correo.data
        )
        db.session.add(mae)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("La matricula del maestro ya existe.", "error")
            return render_template("maestros/agregar.html", form=create_form)
        return redirect(url_for("maestros.index"))

    return render_template("maestros/agregar.html", form=create_form)

@maestros.route("/detalles", methods=["GET", "POST"])
def detalles():
    create_form = MaestroForm(request.form)
    if request.method == "GET":
        matricula = request.args.get("id")
        
        maes = Maestros.query.filter_by(matricula=matricula).first() 
        
        matricula = maes.matricula
        nombre = maes.nombre
        apellidos = maes.apellidos
        correo = maes.correo
        especialidad = maes.especialidad

    return render_template("maestros/detalles.html", nombre=nombre, apellidos=apellidos, correo=correo, especialidad=especialidad)

@maestros.route("/modificar", methods=["GET", "POST"])
def modificar():
    
    create_form = MaestroForm(request.form)
    matricula = request.args.get("id")
    maes = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()

    if request.method == "GET":
        create_form.matricula.data = maes.matricula
        create_form.nombre.data = maes.nombre
        create_form.apellidos.data = maes.apellidos
        create_form.correo.data = maes.correo
        create_form.especialidad.data = maes.especialidad


    if request.method == "POST" and create_form.validate():
        maes.matricula = create_form.matricula.data
        maes.nombre = create_form.nombre.data
        maes.apellidos = create_form.apellidos.data
        maes.correo = create_form.correo.data
        maes.especialidad = create_form.especialidad.data

        db.session.add(maes)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("La matricula del maestro ya existe.", "error")
            return render_template("maestros/modificar.html", form=create_form)
        return redirect(url_for("maestros.index"))

    return render_template("maestros/modificar.html", form=create_form)


@maestros.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = MaestroForm(request.form)
    matricula = request.args.get("id")
    maes = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()

    if request.method == "GET":
        create_form.matricula.data = maes.matricula
        create_form.nombre.data = maes.nombre
        create_form.apellidos.data = maes.apellidos
        create_form.correo.data = maes.correo
        create_form.especialidad.data = maes.especialidad


    if request.method == "POST":
        db.session.delete(maes)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("No se puede eliminar el maestro porque tiene cursos relacionados.", "error")
            return render_template("maestros/eliminar.html", form=create_form)
        return redirect(url_for("maestros.index"))

    return render_template("maestros/eliminar.html", form=create_form)
