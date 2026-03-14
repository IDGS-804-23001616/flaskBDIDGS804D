
from . import cursos
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from .forms import CursoForm
from models import db, Cursos, Maestros, Alumnos, Inscripciones


@cursos.route('/', methods=['GET','POST'])
@cursos.route('/index')
def index():
    create_form = CursoForm(request.form)
    cursos_list = Cursos.query.all()
      
    return render_template('cursos/index.html', form=create_form, cursos=cursos_list)

@cursos.route("/agregar", methods = ["GET", "POST"])
def agregar():
    create_form = CursoForm(request.form)
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") 
                                      for m in Maestros.query.all()]
    
    if request.method == "POST" and create_form.validate():
        curso = Cursos(
            nombre = create_form.nombre.data,
            descripcion = create_form.descripcion.data,
            maestro_id = create_form.maestro_id.data
        )
        db.session.add(curso)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("No se pudo guardar el curso. Verifica los datos.", "error")
            return render_template("cursos/agregar.html", form=create_form)
        return redirect(url_for("cursos.index"))
    return render_template("cursos/agregar.html", form = create_form)

@cursos.route("/detalles", methods=["GET", "POST"])
def detalles():
    create_form = CursoForm(request.form)
    if request.method == "GET":
        id = request.args.get("id")

        curso = db.session.query(Cursos).filter(Cursos.id == id).first()

        id = curso.id
        nombre = curso.nombre
        descripcion = curso.descripcion
        maestro = curso.maestro

    return render_template("cursos/detalles.html", curso=curso)

@cursos.route("/modificar", methods=["GET", "POST"])
def modificar():
    create_form = CursoForm(request.form)
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") 
                                      for m in Maestros.query.all()]
    id = request.args.get("id")
    curso = db.session.query(Cursos).filter(Cursos.id == id).first()

    if request.method == "GET":
        create_form.nombre.data = curso.nombre
        create_form.descripcion.data = curso.descripcion
        create_form.maestro_id.data = curso.maestro_id

    if request.method == "POST" and create_form.validate():
        curso.nombre = create_form.nombre.data
        curso.descripcion = create_form.descripcion.data
        curso.maestro_id = create_form.maestro_id.data

        db.session.add(curso)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("No se pudo actualizar el curso. Verifica los datos.", "error")
            return render_template("cursos/modificar.html", form=create_form)
        return redirect(url_for("cursos.index"))

    return render_template("cursos/modificar.html", form=create_form)

@cursos.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = CursoForm(request.form)
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") 
                                      for m in Maestros.query.all()]
    id = request.args.get("id")
    curso = db.session.query(Cursos).filter(Cursos.id == id).first()

    if request.method == "GET":
        create_form.nombre.data = curso.nombre
        create_form.descripcion.data = curso.descripcion
        create_form.maestro_id.data = curso.maestro_id

    if request.method == "POST":
        Inscripciones.query.filter_by(curso_id=id).delete()
        db.session.delete(curso)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("No se pudo eliminar el curso.", "error")
            return render_template("cursos/eliminar.html", form=create_form)
        return redirect(url_for("cursos.index"))

    return render_template("cursos/eliminar.html", form=create_form)

@cursos.route("/inscribir", methods=["GET", "POST"])
def inscribir():
    curso_id = request.args.get("curso_id")
    curso = db.session.query(Cursos).filter(Cursos.id == curso_id).first()
    
    if request.method == "POST":
        alumno_id = request.form.get('alumno_id')
        inscripcion_existente = Inscripciones.query.filter_by(
            alumno_id=alumno_id,
            curso_id=curso_id
        ).first()
        if not inscripcion_existente:
            nueva_inscripcion = Inscripciones(
                alumno_id=alumno_id,
                curso_id=curso_id
            )
            db.session.add(nueva_inscripcion)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash("El alumno ya estaba inscrito en este curso.", "error")
        return redirect(url_for('cursos.index'))
    alumnos_inscritos_ids = [i.alumno_id for i in Inscripciones.query.filter_by(curso_id=curso_id).all()]
    alumnos = Alumnos.query.filter(~Alumnos.id.in_(alumnos_inscritos_ids)).all()
    
    return render_template('cursos/inscribir.html', curso=curso, alumnos=alumnos)

@cursos.route('/desinscribir', methods=['POST'])
def desinscribir():
    curso_id = request.args.get("curso_id")
    alumno_id = request.args.get("alumno_id")
    
    inscripcion = Inscripciones.query.filter_by(
        alumno_id=alumno_id,
        curso_id=curso_id
    ).first()
    
    if inscripcion:
        db.session.delete(inscripcion)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("No se pudo desinscribir al alumno.", "error")
    return redirect(url_for('cursos.detalles', id=curso_id))
    

@cursos.route('/inscripciones', methods=['GET'])
def consulta_inscripciones():
    curso_id = request.args.get('curso_id', '').strip()
    maestro_id = request.args.get('maestro_id', '').strip()
    alumno_id = request.args.get('alumno_id', '').strip()

    cursos_options = Cursos.query.all()
    maestros_options = Maestros.query.all()
    alumnos_options = Alumnos.query.all()

    cursos_list = Cursos.query.all()
    inscripciones_data = []
    for curso in cursos_list:
        maestro = curso.maestro
        alumnos_inscritos = curso.alumnos

        if curso_id and str(curso.id) != curso_id:
            continue
        if maestro_id and (not maestro or str(maestro.matricula) != maestro_id):
            continue
        if alumno_id and not any(str(alumno.id) == alumno_id for alumno in alumnos_inscritos):
            continue

        inscripciones_data.append({
            'curso': curso,
            'maestro': maestro,
            'alumnos': alumnos_inscritos
        })

    return render_template(
        'cursos/consulta_inscripciones.html',
        inscripciones=inscripciones_data,
        cursos_options=cursos_options,
        maestros_options=maestros_options,
        alumnos_options=alumnos_options,
        selected_curso_id=curso_id,
        selected_maestro_id=maestro_id,
        selected_alumno_id=alumno_id
    )