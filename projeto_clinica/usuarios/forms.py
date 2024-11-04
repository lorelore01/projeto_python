from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from projeto_clinica.models import Paciente

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')
    
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    cpf = StringField('CPF', validators=[
    DataRequired(),
    Length(min=14, max=14, message="CPF inválido!"),
    Regexp(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message="CPF deve estar no formato 000.000.000-00")
    ])
    nome = StringField('Nome', validators=[DataRequired()])
    idade = StringField('Idade: ', validators=[DataRequired(), Regexp(r'^(1[01]{2}|[1-9]?[0-9])$', message="Idade inválida!")])  # Regex para idade
    pagamento = StringField('Pagamento: ', validators=[DataRequired()])
    password = PasswordField('Senha: ', validators=[DataRequired(), EqualTo('pass_confirm', message="Senhas devem ser iguais!")])
    pass_confirm = PasswordField('Confirmar senha: ', validators=[DataRequired()])
    convenio = StringField('Convenio: ', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')
        
    def validate_email(self, field):
        if Paciente.query.filter_by(email=field.data).first():
            raise ValidationError('Seu e-mail já foi registrado!')
    
    def validate_cpf(self, field):
        if Paciente.query.filter_by(cpf=field.data).first():
            raise ValidationError('Este CPF já foi registrado!')

    def validate_idade(self, field):
        try:
            idade = int(field.data)
            if idade < 0 or idade > 123:
                raise ValidationError('Idade deve ser entre 0 e 123 anos.')
        except ValueError:
            raise ValidationError('Idade deve ser um número válido.')
        

class UpdateUserForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Atualizar')
    
    def check_email(self,field):
        if Paciente.query.filter_by(email=field.data).first():
            raise ValidationError('Seu e-mail já foi registrado!')
