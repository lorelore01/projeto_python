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

def create_3d_bar_chart(counts_per_doctor):
    # Create a new figure and axis for a 3D plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Define positions for the bars
    x_pos = []
    y_pos = []
    z_pos = [0] * len(counts_per_doctor)

    # Width and depth of each bar
    dx = np.ones(len(counts_per_doctor))  # Width of bars
    dy = np.ones(len(counts_per_doctor))  # Depth of bars

    # Define the height of each bar (number of consultations per day)
    dz = []

    # Loop through each doctor and their consultation counts
    for i, (doctor, counts) in enumerate(counts_per_doctor.items()):
        for j, count in enumerate(counts):
            x_pos.append(i)  # X position for the doctor
            y_pos.append(j)  # Y position for the day of the week
            dz.append(count)  # Height of the bar (number of consultations)

    # Set labels for the x and y axes
    ax.set_xlabel('Médicos')
    ax.set_ylabel('Dia da Semana')
    ax.set_zlabel('Número de Consultas')

    # Set ticks on the x and y axes
    ax.set_xticks(np.arange(len(counts_per_doctor)))
    ax.set_yticks(np.arange(5))  # 5 days of the week (assuming data for Monday-Friday)

    # Set the labels for the x and y axes
    ax.set_xticklabels(list(counts_per_doctor.keys()))
    ax.set_yticklabels(["Mon", "Tue", "Wed", "Thu", "Fri"])

    # Create the 3D bar chart
    ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color='skyblue', shade=True)

    # Return the figure object
    return fig

def prepare_data_for_plot():
    results = get_consultation_counts()

    # Initialize a dictionary to hold counts for each doctor
    doctor_counts = {
        "Dra. Marina": [0] * 7,  # There are 7 days in a week
        "Dr. Ricardo": [0] * 7,
        "Dra. Ana": [0] * 7,
        "Dr. Jonatas": [0] * 7,
        "Dra. Leandra": [0] * 7,
    }

    # Map the weekday numbers to indices (0=Sunday, 1=Monday, ..., 6=Saturday)
    weekday_index = {0: 6, 1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}

    # Populate the counts based on query results
    for nome, dia_da_semana, total in results:
        index = weekday_index[int(dia_da_semana)]
        doctor_counts[nome][index] += total

    # Flatten the counts into a list for plotting
    counts_for_plot = []
    for doctor in doctor_counts.values():
        counts_for_plot.extend(doctor)

    return counts_for_plot

@graficos_bp.route('/graphics')
@login_required
def graphics_page():
    # Step 1: Get the consultation counts (replace with actual DB retrieval)
    dados = get_consultation_counts()  # Get data from the database

    # Step 2: Prepare the data for the graph
    datas = []
    contagem = prepare_data_for_plot()
    
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

