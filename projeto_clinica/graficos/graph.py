from flask import Blueprint, render_template
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask_login import login_required
from projeto_clinica import db
from projeto_clinica.models import Consulta, Medico

graficos_bp = Blueprint('graficos', __name__)

def encode_plot_to_base64(fig):
    """Helper function to encode a matplotlib figure as a base64 string."""
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return base64.b64encode(img.getvalue()).decode('utf-8')

@graficos_bp.route('/grafico_consultas')
@login_required
def grafico_consultas():
    consultas = Consulta.query.all()
    day_counts = {day: 0 for day in range(7)}
    for consulta in consultas:
        day_counts[consulta.data.weekday()] += 1

    days = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "dom"]
    counts = [day_counts[day] for day in range(7)]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(days, counts, color='skyblue')
    ax.set_title("Consultas por Dia da Semana", fontsize=16)
    ax.set_xlabel("Dia da Semana", fontsize=12)
    ax.set_ylabel("Número de Consultas", fontsize=12)

    image_data = encode_plot_to_base64(fig)
    return render_template('grafico_consultas.html', image_data=image_data)

def get_consultation_counts():
    return db.session.query(
        Medico.nome,
        db.func.strftime('%Y-%m-%d', Consulta.data),
        db.func.count(Consulta.id)
    ).join(Medico).group_by(Medico.nome, Consulta.data).all()

def create_3d_bar_chart(counts_per_doctor):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    x_pos, y_pos, dz = [], [], []
    for i, (doctor, counts) in enumerate(counts_per_doctor.items()):
        for j, count in enumerate(counts):
            x_pos.append(i)
            y_pos.append(j)
            dz.append(count)

    dx, dy = np.full(len(dz), 0.5), np.full(len(dz), 0.5)
    ax.bar3d(x_pos, y_pos, np.zeros(len(dz)), dx, dy, dz, color='skyblue', shade=True)
    ax.set_xticks(range(len(counts_per_doctor)))
    ax.set_xticklabels(list(counts_per_doctor.keys()), rotation=45)
    ax.set_yticks(range(5))
    ax.set_yticklabels(["Seg", "Ter", "Qua", "Qui", "Sex"])
    ax.set_zticks([0, 1, 2, 3, 4])  # Ajuste os valores conforme necessário
    ax.set_zticklabels(['0', '1', '2', '3', '4'])
    ax.set_xlabel('Médicos')
    ax.set_ylabel('Dia da Semana')
    ax.set_zlabel('Número de Consultas')

    return fig

@graficos_bp.route('/graphics')
@login_required
def graphics_page():
    counts_per_doctor = {doctor: [0] * 5 for doctor in ["Dra. Marina Menezes", "Dr. Ricardo Alexandre Mendes", "Dra. Ana Silva", "Dr. Jonatas Figueiredo", "Dra. Leandra Ferreira"]}
    for nome, dia_da_semana, total in get_consultation_counts():
        weekday = datetime.strptime(dia_da_semana, '%Y-%m-%d').weekday()
        if nome in counts_per_doctor and 0 <= weekday < 5:
            counts_per_doctor[nome][weekday] += total

    fig = create_3d_bar_chart(counts_per_doctor)
    image_data = encode_plot_to_base64(fig)
    return render_template('grafico_consultas.html', image_data=image_data)
