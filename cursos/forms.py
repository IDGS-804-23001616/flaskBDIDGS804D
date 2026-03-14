from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class CursoForm(FlaskForm):
    nombre = StringField('Nombre del Curso', 
                        validators=[DataRequired(), Length(max=150)])
    descripcion = TextAreaField('Descripción',
                               validators=[Length(max=500)])
    maestro_id = SelectField('Maestro', 
                           coerce=int,
                           validators=[DataRequired()])
    submit = SubmitField('Guardar')
