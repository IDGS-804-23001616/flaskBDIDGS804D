
from wtforms import Form, StringField, IntegerField, EmailField
from wtforms.validators import DataRequired, Length, Email


class AlumnoForm(Form):

    matricula = StringField(
        "Matrícula",
        [
            DataRequired(message="La matrícula es obligatoria"),
            Length(min=6, max=12, message="La matrícula debe tener entre 6 y 12 dígitos")
        ]
    )

    nombre = StringField(
        "Nombre",
        [
            DataRequired(message="El nombre es obligatorio"),
            Length(min=2, max=50, message="El nombre debe tener entre 2 y 50 caracteres")
        ]
    )

    apellido = StringField(
        "Apellido Paterno",
        [
            DataRequired(message="El apellido paterno es obligatorio"),
            Length(min=2, max=50, message="El apellido debe tener entre 2 y 50 caracteres")
        ]
    )

    apellido_materno = StringField(
        "Apellido Materno",
        [
            DataRequired(message="El apellido materno es obligatorio"),
            Length(min=2, max=50, message="El apellido debe tener entre 2 y 50 caracteres")
        ]
    )

    correo = EmailField(
        "Correo Electrónico",
        [
            DataRequired(message="El correo es obligatorio"),
            Email(message="Ingrese un correo válido")
        ]
    )
    
    telefono = StringField(
        "Teléfono",
        [
          DataRequired(message="El teléfono es obligatorio"),
          Length(min=10, max=10, message="El teléfono debe tener 10 dígitos")
        ]
    )
