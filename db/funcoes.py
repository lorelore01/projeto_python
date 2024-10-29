import sqlite3
connector = sqlite3.connect("consultorio.db", check_same_thread=False)
cursor = connector.cursor()

def criar_paciente(data):
    print(data)
    connector.execute("INSERT INTO pacientes (nome, cpf, idade, email, telefone, pagamento, tipo_consulta, convenio) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                      (data["nome"], data["cpf"], data["idade"], data["email"], data["telefone"], data["convenio"], data["forma-pagamento"], "Sei lá"))
    connector.commit()