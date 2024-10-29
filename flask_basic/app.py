from flask import Flask, render_template

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)