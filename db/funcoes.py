import sqlite3
connector = sqlite3.connect("db/consultorio.db", check_same_thread=False)
cursor = connector.cursor()

def criar_paciente(data):
    cursor.execute("INSERT INTO pacientes (nome, cpf, idade, email, telefone, pagamento, convenio) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (data["nome"], data["cpf"], data["idade"], data["email"], data["telefone"], data["forma-pagamento"], data["convenio"]))
    connector.commit()
#def recuperar_pacientes():
    #cursor.execute("SELECT * FROM pacientes")
    #return cursor.fetchall()