from projeto_clinica.models import Paciente, Consulta
from projeto_clinica import db, app

# Creating an application context
with app.app_context():
    # Delete all consultas
    db.session.query(Consulta).delete()

    # Delete all pacientes
    db.session.query(Paciente).delete()

    # Commit the changes to the database
    db.session.commit()