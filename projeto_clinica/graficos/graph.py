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

def get_consultation_counts():
    return db.session.query(
        Medico.nome,
        db.func.strftime('%Y-%m-%d', Consulta.data),
        db.func.count(Consulta.id)
    ).join(Medico).group_by(Medico.nome, Consulta.data).all()

def create_3d_bar_chart(counts_per_doctor):
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Prepare data for the 3D bar chart
    x_pos, y_pos, dz = [], [], []
    for i, (doctor, counts) in enumerate(counts_per_doctor.items()):
        for j, count in enumerate(counts):
            x_pos.append(i)
            y_pos.append(j)
            dz.append(count)

    dx, dy = np.full(len(dz), 0.5), np.full(len(dz), 0.5)
    
    # Add 3D bars with custom styling
    ax.bar3d(x_pos, y_pos, np.zeros(len(dz)), dx, dy, dz, color='skyblue', shade=True)

    # Customize tick marks and labels for clarity
    ax.set_xticks(range(len(counts_per_doctor)))
    ax.set_xticklabels(list(counts_per_doctor.keys()), rotation=45, fontsize=12)
    ax.set_yticks(range(5))
    ax.set_yticklabels(["Seg", "Ter", "Qua", "Qui", "Sex"], fontsize=12)
    ax.set_zticks([0, 1, 2, 3, 4])  # Adjust these values as needed
    ax.set_zticklabels(['0', '1', '2', '3', '4'], fontsize=12)

    # Set labels and title with more space for readability
    ax.set_xlabel('Médicos', fontsize=14)
    ax.set_ylabel('Dia da Semana', fontsize=14)
    ax.set_zlabel('Número de Consultas', fontsize=14)
    ax.set_title("Consultas por Médico e Dia da Semana", fontsize=18)

    # Adding a grid for better visualization
    ax.grid(True, color='gray', linestyle='--', linewidth=0.5)

    return fig

@graficos_bp.route('/graphics')
@login_required
def graphics_page():
    # Prepare the data with counts per doctor
    counts_per_doctor = {doctor: [0] * 5 for doctor in ["Dra. Marina Menezes", "Dr. Ricardo Alexandre Mendes", "Dra. Ana Silva", "Dr. Jonatas Figueiredo", "Dra. Leandra Ferreira"]}
    for nome, dia_da_semana, total in get_consultation_counts():
        weekday = datetime.strptime(dia_da_semana, '%Y-%m-%d').weekday()
        if nome in counts_per_doctor and 0 <= weekday < 5:
            counts_per_doctor[nome][weekday] += total

    # Create the 3D bar chart
    fig = create_3d_bar_chart(counts_per_doctor)
    
    # Convert the figure to base64 format
    image_data = encode_plot_to_base64(fig)
    
    # Render the template and pass the image data
    return render_template('grafico_consultas.html', image_data=image_data)
