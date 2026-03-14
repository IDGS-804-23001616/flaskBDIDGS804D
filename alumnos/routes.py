from . import alumnos
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from .forms import AlumnoForm
from models import db, Alumnos


@alumnos.route('/', methods=['GET','POST'])
@alumnos.route('/index')
def index():
    create_form = AlumnoForm(request.form)
    alumno = Alumnos.query.all()
      
    return render_template('alumnos/index.html', form=create_form, alumno=alumno)

@alumnos.route("/agregar", methods = ["GET", "POST"])
def agregar():
    create_form = AlumnoForm(request.form)
    if request.method == "POST" and create_form.validate():
        alum = Alumnos(
        nombre = create_form.nombre.data,
        apellido = create_form.apellido.data,
        correo = create_form.correo.data,
        matricula = create_form.matricula.data,
        apellido_materno = create_form.apellido_materno.data,
        telefono = create_form.telefono.data)
        db.session.add(alum)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("La matricula ya existe. Usa una diferente.", "error")
            return render_template("alumnos/agregar.html", form=create_form)
        return redirect(url_for("alumnos.index"))
    return render_template("alumnos/agregar.html", form = create_form)

@alumnos.route("/detalles", methods=["GET", "POST"])
def detalles():
    create_form = AlumnoForm(request.form)
    if request.method == "GET":
        id = request.args.get("id")

        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        id = request.args.get("id")
        nombre = alum1.nombre
        apellido = alum1.apellido
        apellido_materno = alum1.apellido_materno
        correo = alum1.correo
        telefono = alum1.telefono


    return render_template("alumnos/detalles.html", nombre=nombre, apellido=apellido, correo=correo)

@alumnos.route("/modificar", methods=["GET", "POST"])
def modificar():
    create_form = AlumnoForm(request.form)
    id = request.args.get("id")
    alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

    if request.method == "GET":
        create_form.matricula.data = alum1.matricula
        create_form.nombre.data = alum1.nombre
        create_form.apellido.data = alum1.apellido
        create_form.apellido_materno.data = alum1.apellido_materno
        create_form.correo.data = alum1.correo
        create_form.telefono.data = alum1.telefono

    if request.method == "POST" and create_form.validate():
        alum1.matricula = create_form.matricula.data
        alum1.nombre = create_form.nombre.data
        alum1.apellido = create_form.apellido.data
        alum1.apellido_materno = create_form.apellido_materno.data
        alum1.correo = create_form.correo.data
        alum1.telefono = create_form.telefono.data

        db.session.add(alum1)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("La matricula ya existe. Usa una diferente.", "error")
            return render_template("alumnos/modificar.html", form=create_form)
        return redirect(url_for("alumnos.index"))

    return render_template("alumnos/modificar.html", form=create_form)

@alumnos.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = AlumnoForm(request.form)
    id = request.args.get("id")
    alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

    if request.method == "GET":
        create_form.matricula.data = alum1.matricula
        create_form.nombre.data = alum1.nombre
        create_form.apellido.data = alum1.apellido
        create_form.apellido_materno.data = alum1.apellido_materno
        create_form.correo.data = alum1.correo
        create_form.telefono.data = alum1.telefono

    if request.method == "POST":
        alum = Alumnos.query.get(id)

        db.session.delete(alum1)
        db.session.commit()
        return redirect(url_for("alumnos.index"))

    return render_template("alumnos/eliminar.html", form=create_form)
