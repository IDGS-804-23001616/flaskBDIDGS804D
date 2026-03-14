
from wtforms import Form, StringField, IntegerField, EmailField
from wtforms.validators import DataRequired, Length, Email


class MaestroForm(Form):

    matricula = StringField(
        "Matrícula",
        [
            DataRequired(message="La matrícula es obligatoria"),
            Length(min=5, max=7, message="La matrícula debe tener entre 6 y 12 dígitos")
        ]
    )

    nombre = StringField(
        "Nombre",
        [
            DataRequired(message="El nombre es obligatorio"),
            Length(min=2, max=50, message="El nombre debe tener entre 2 y 50 caracteres")
        ]
    )

    apellidos = StringField(
        "Apellidos",
        [
            DataRequired(message="Los apellidos son obligatorios"),
            Length(min=2, max=100, message="Los apellidos deben tener entre 2 y 100 caracteres")
        ]
    )

    especialidad = StringField(
        "Especialidad",
        [
            DataRequired(message="La especialidad es obligatoria"),
            Length(min=2, max=50, message="La especialidad debe tener entre 2 y 50 caracteres")
        ]
    )

    correo = EmailField(
        "Correo Electrónico",
        [
            DataRequired(message="El correo es obligatorio"),
            Email(message="Ingrese un correo válido")
        ]
    )
