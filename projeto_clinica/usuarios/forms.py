from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError
from flask_login import current_user
from projeto_clinica.models import Paciente
import re

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="E-mail inválido")])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')
    
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="E-mail inválido")])
    cpf = StringField('CPF', validators=[
        DataRequired(),
        Length(min=14, max=14),
        Regexp(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message="CPF deve estar no formato 000.000.000-00")
    ])
    nome = StringField('Nome', validators=[DataRequired()])
    idade = StringField('Idade: ', validators=[
        DataRequired(),
        Regexp(r'^(1[01]{2}|[1-9]?[0-9])$', message="Idade inválida!")  # Regex to validate age
    ])
    pagamento = SelectField('Pagamento: ', choices=[('crt', 'Cartão'), ('avst', 'À vista')])
    password = PasswordField('Senha: ', validators=[
        DataRequired(),
        EqualTo('pass_confirm', message="Senhas devem ser iguais!")
    ])
    pass_confirm = PasswordField('Confirmar senha: ', validators=[DataRequired()])
    convenio = SelectField('Convênio: ', choices=[("y", "Sim"), ("n", "Não")])
    submit = SubmitField('Cadastrar')

    # Custom validator for 'nome'
    def validate_nome(self, field):
        nome = field.data.strip()

        # Validate that the name contains only letters and spaces
        if not all(char.isalpha() or char.isspace() for char in nome):
            raise ValidationError("O nome deve conter apenas letras e espaços.")
        
        # Check if name already exists in the database
        if Paciente.query.filter_by(nome=nome).first():
            raise ValidationError("Este nome já foi registrado!")

    # Custom validator for 'email'
    def validate_email(self, field):
        # Check if email already exists in the database
        if Paciente.query.filter_by(email=field.data).first():
            raise ValidationError('Seu e-mail já foi registrado!')

    # Custom validator for 'cpf'
    def validate_cpf(self, field):
        # Check if CPF already exists in the database
        if Paciente.query.filter_by(cpf=field.data).first():
            raise ValidationError('Este CPF já foi registrado!')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="E-mail inválido")])
    nome = StringField('Nome', validators=[DataRequired()])
    nova_senha = PasswordField('Nova Senha', validators=[
        Length(min=6, message="A senha deve ter pelo menos 6 caracteres"),
        DataRequired()
    ])
    confirmar_senha = PasswordField('Confirmar Nova Senha', validators=[
        DataRequired(),
        EqualTo('nova_senha', message="As senhas devem coincidir")
    ])
    pagamento = SelectField('Método de pagamento', choices=[('crt', 'Cartão'), ('avst', 'À vista')])
    convenio = SelectField('Convênio', choices=[('y', 'Sim'), ('n', 'Não')])
    submit = SubmitField('Atualizar')

    def validate_nome(self, field):
        # Verificar se o nome contém apenas letras e espaços
        if not all(char.isalpha() or char.isspace() for char in field.data):
            raise ValidationError("O nome deve conter apenas letras e espaços.")

        # Verificar se o nome já foi registrado no banco de dados (exceto para o usuário atual)
        if field.data != current_user.nome:
            existing_nome = Paciente.query.filter_by(nome=field.data).first()
            if existing_nome:
                raise ValidationError('Este nome já foi registrado por outro usuário.')

    def validate_email(self, field):
        # Verificar se o email já foi registrado no banco de dados (exceto para o usuário atual)
        if field.data != current_user.email:
            existing_email = Paciente.query.filter_by(email=field.data).first()
            if existing_email:
                raise ValidationError('Este e-mail já foi registrado por outro usuário.')
