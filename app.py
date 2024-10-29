from flask import Flask, render_template, request
from flask_cors import CORS
from db import funcoes

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pacientes')
def pacientes():
    return render_template('html/pacientes.html')

@app.route('/medicos')
def medicos():
    return render_template('html/medicos.html')

@app.route('/horario_medico1')
def horario_medico1():
    return render_template('html/horario_medico1.html')

@app.route('/horario_medico2')
def horario_medico2():
    return render_template('html/horario_medico2.html')

@app.route('/horario_medico3')
def horario_medico3():
    return render_template('html/horario_medico3.html')

@app.route('/horario_medico4')
def horario_medico4():
    return render_template('html/horario_medico4.html')

@app.route('/horario_medico5')
def horario_medico5():
    return render_template('html/horario_medico5.html')

@app.route("/api/cadastro", methods=["POST"])
def cadastrar_paciente():
    data = request.json
    funcoes.criar_paciente(data)
    return render_template("html/pacientes.html")

if __name__ == '__main__':
    app.run(debug=True)