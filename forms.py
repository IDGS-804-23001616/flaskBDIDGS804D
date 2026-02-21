
from wtforms import Form, StringField, IntegerField, EmailField
from wtforms.validators import DataRequired, Length, Email


class UserForm(Form):

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
        "Apellido",
        [
            DataRequired(message="El apellido es obligatorio"),
            Length(min=2, max=50, message="El apellido debe tener entre 2 y 50 caracteres")
        ]
    )

    correo = EmailField(
        "Correo",
        [
            DataRequired(message="El correo es obligatorio"),
            Email(message="Ingrese un correo válido")
        ]
    )
    
    telefono = StringField(
        "Teléfono",
        [
          DataRequired(message="El celular es obligatoria"),
        ]
    )
    
    apellido_materno = StringField(
        "Apellido",
        [
            DataRequired(message="El apellido es obligatorio"),
            Length(min=2, max=50, message="El apellido debe tener entre 2 y 50 caracteres")
        ]
    )
