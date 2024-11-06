from flask import Blueprint, render_template
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask_login import login_required
from projeto_clinica import db
from projeto_clinica.models import Consulta, Medico

# Define the blueprint
graficos_bp = Blueprint('graficos', __name__)

# Route to display the consultations chart
@graficos_bp.route('/grafico_consultas')
@login_required
def grafico_consultas():
    # Step 1: Query all consultations
    consultas = Consulta.query.all()

    # Step 2: Count the consultations by day of the week (0 = Monday, 6 = Sunday)
    days_of_week = [0, 1, 2, 3, 4, 5, 6]  # Days of the week: Monday to Sunday
    day_counts = {day: 0 for day in days_of_week}

    for consulta in consultas:
        dia = consulta.data.weekday()  # Get the weekday (0=Monday, 6=Sunday)
        day_counts[dia] += 1

    # Step 3: Prepare data for the graph
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    counts = [day_counts[day] for day in days_of_week]

    # Step 4: Create a bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(days, counts, color='skyblue')
    ax.set_title("Consultas por Dia da Semana", fontsize=16)
    ax.set_xlabel("Dia da Semana", fontsize=12)
    ax.set_ylabel("Número de Consultas", fontsize=12)

    # Step 5: Save the plot to a BytesIO object
    img = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(img)
    img.seek(0)
    plt.close(fig)

    # Step 6: Encode the image as base64 for embedding in the template
    image_data = base64.b64encode(img.getvalue()).decode('utf-8')

    # Step 7: Render the template with the graph
    return render_template('grafico_consultas.html', image_data=image_data)

@graficos_bp.route('/graphics')
@login_required
def graphics_page():
    # Step 1: Get the consultation counts (replace with actual DB retrieval)
    dados = get_consultation_counts()  # Get data from the database

    # Step 2: Prepare the data for the graph
    datas = []
    contagem = []
    
    doctor_names = ["Dra. Marina", "Dr. Ricardo", "Dra. Ana", "Dr. Jonatas", "Dra. Leandra"]
    
    counts_per_doctor = {name: [0] * 5 for name in doctor_names}  # 5 days of the week

    # Step 3: Process results to count consultations
    for nome, dia_da_semana, total in dados:
        if nome in counts_per_doctor:
            counts_per_doctor[nome][int(dia_da_semana)] += total

    # Flatten the counts into the right format
    for doctor in doctor_names:
        datas.append(doctor)
        contagem.extend(counts_per_doctor[doctor])

    # Step 4: Generate the plot using the consultation counts
    dz = [total for counts in counts_per_doctor.values() for total in counts]  # Flatten counts for plotting
    fig = create_3d_bar_chart(counts_per_doctor)  # Generate the 3D bar chart with real data
    canvas = FigureCanvas(fig)
    
    # Save the image to a BytesIO buffer
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    
    # Encode the image as base64
    image_data = base64.b64encode(img.getvalue()).decode('utf-8')

    return render_template('grafico_consultas.html', datas=datas, contagem=contagem, image_data=image_data)

# Get consultation counts from DB (with Medico)
def get_consultation_counts():
    # Join Consulta with Medico to get the doctor's name
    consultas = db.session.query(
        Medico.nome,  # Get the doctor's name
        Consulta.data.weekday(),  # Extract the weekday
        db.func.count(Consulta.id)  # Count the number of consultations
    ).join(Medico).group_by(Medico.nome, Consulta.data.weekday()).all()

    result = []
    for medico, dia_da_semana, count in consultas:
        result.append((medico, dia_da_semana, count))

    return result
