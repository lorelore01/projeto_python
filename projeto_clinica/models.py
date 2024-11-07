# models.py

from projeto_clinica import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return Paciente.query.get(user_id)

class Paciente(db.Model, UserMixin):
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), index=True)
    idade = db.Column(db.String(3))
    cpf = db.Column(db.String(11), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    pagamento = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    convenio = db.Column(db.String(64))
    
    # Define relationships
    medico = db.relationship("Medico", back_populates="paciente", uselist=False)
    consultas = db.relationship("Consulta", back_populates="paciente")
    
    def __init__(self, nome, idade, cpf, email, convenio, pagamento, senha):
        self.nome = nome
        self.idade = idade
        self.cpf = cpf
        self.email = email
        self.pagamento = pagamento
        self.convenio = convenio
        self.password_hash = generate_password_hash(senha)  # Handle password hash here
    
    def check_password(self, senha):
        return check_password_hash(self.password_hash, senha)
    
    def __repr__(self):
        return f"Paciente {self.nome}"
    
    
class Medico(db.Model):
    
    __tablename__ = 'medicos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), nullable=False)
    especialidade = db.Column(db.String(64))
    horarios = db.Column(db.String(128))
    email = db.Column(db.String(120), nullable = True)
 

    # Chave estrangeira para um relacionamento um-para-um com Paciente
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), unique=True)
    paciente = db.relationship("Paciente", back_populates="medico", lazy=True)

    # Relacionamento um-para-muitos com Consulta
    consultas = db.relationship("Consulta", back_populates="medico", lazy=True)
    
    def __init__(self, nome, especialidade, horarios):
        self.nome = nome
        self.especialidade = especialidade
        self.horarios = horarios
    
    def __repr__(self):
        return f"Médico: {self.nome}"


class Consulta(db.Model):
    __tablename__ = 'consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime)
    data = db.Column(db.DateTime, nullable=False,  default=datetime.utcnow)
    descricao = db.Column(db.Text)
    dia_da_semana = db.Column(db.String(10))  # New column to store the day of the week

    # Foreign keys
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'))
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'))

    # Relationships
    paciente = db.relationship("Paciente", back_populates="consultas", lazy=True)
    medico = db.relationship("Medico", back_populates="consultas", lazy=True)
    
    def __init__(self, data, descricao, paciente_id, medico_id, dia_da_semana):
        self.data = data
        self.descricao = descricao
        self.paciente_id = paciente_id  # Set paciente_id
        self.medico_id = medico_id  # Set medico_id
        self.dia_da_semana = dia_da_semana  
    
    def __repr__(self):
        return f"Consulta: {self.descricao}"

    # Helper method to extract day of the week (0 = Monday, 6 = Sunday)
    def get_dia_da_semana(self):
        return self.data.weekday()  # 0 = Monday, 6 = Sunday
    
    # Method to format the date for graph usage
    def get_formatted_data(self):
        return self.data.strftime('%a %H:%M')  # Example: 'Mon 14:30'

    # Optional: Method to get the doctor's name
    def get_medico_name(self):
        return self.medico.nome if self.medico else 'No doctor assigned'

    # Optional: Method to get the patient's name
    def get_paciente_name(self):
        return self.paciente.nome if self.paciente else 'No patient assigned'