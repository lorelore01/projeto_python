import sqlite3

connector = sqlite3.connect("consultorio.db", check_same_thread=False)
cursor = connector.cursor()

cursor.execute("""PRAGMA foreign_keys = ON;""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pacientes (
              id INTEGER PRIMARY KEY,
              nome TEXT NOT NULL,
              cpf TEXT NOT NULL,
              convenio TEXT,
              idade INTEGER,
              email TEXT,
              telefone TEXT,
              pagamento TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                especialidade TEXT,
                horario TEXT                
)
""")

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY,
                paciente_id INTEGER,
                data_horario DATETIME NOT NULL,
                medico_id INTEGER,
                observacoes TEXT,
                FOREIGN KEY(paciente_id) REFERENCES pacientes(id),
                FOREIGN KEY(medico_id) REFERENCES medicos(id)

                )
               """)

connector.commit()
connector.close()