import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime, timedelta
from sqlalchemy import func
from projeto_clinica.models import Consulta
from projeto_clinica import db
from projeto_clinica.models import Medico
import os 
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def get_consultation_counts():
    # Current week start and end dates
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Query to count consultations per doctor per day
    results = db.session.query(
        Medico.nome,
        func.strftime('%w', Consulta.data_hora).label('dia_da_semana'),
        func.count(Consulta.id).label('total_consultas')
    ).join(Consulta).filter(
        Consulta.data_hora >= start_of_week,
        Consulta.data_hora < end_of_week
    ).group_by(
        Medico.nome, 'dia_da_semana'
    ).all()

    return results

def prepare_data_for_plot():
    results = get_consultation_counts()

    # Initialize a dictionary to hold counts for each doctor
    doctor_counts = {
        "Dra. Marina": [0] * 5,
        "Dr. Ricardo": [0] * 5,
        "Dra. Ana": [0] * 5,
        "Dr. Jonatas": [0] * 5,
        "Dra. Leandra": [0] * 5,
    }

    # Map the weekday numbers to indices (0=Sunday, 1=Monday, etc.)
    weekday_index = {0: 6, 1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}  # Adjust according to your needs

    # Populate the counts
    for nome, dia_da_semana, total in results:
        index = weekday_index[int(dia_da_semana)]
        doctor_counts[nome][index] += total

    # Flatten the counts into a list for plotting
    counts_for_plot = []
    for doctor in doctor_counts.values():
        counts_for_plot.extend(doctor)

    return counts_for_plot

def plot_consultas(dados, colors=None, legend_labels=None, file_path='static/grafico_consultas.png'):
    # Prepare data for the bars
    dz = []  # Heights based on your consultation counts
    
    # Assuming dados is a list of counts for each doctor on each day, e.g., [1, 2, 3, ...]
    for count in dados:
        dz.append(count)  # Append each count for each doctor's day
    
    # Ensure we have the correct number of bars (5 doctors * 5 days = 25 bars)
    assert len(dz) == 25, f"Expected 25 bars, but got {len(dz)}."

    # Define the positions for the bars
    xpos = np.repeat([0, 1, 2, 3, 4], 5)  # Days of the week repeated for each specialty
    ypos = np.tile([0, 1, 2, 3, 4], 5)    # Doctors/Specialties repeated for each day of the week
    zpos = [0] * 25                       # Base of the bars

    dx = np.ones_like(xpos) * 0.3        # Width of the bars on the X-axis
    dy = np.ones_like(ypos) * 0.3        # Depth of the bars on the Y-axis
    
    # Default colors if none are provided
    if colors is None:
        colors = ["#8BC34A", "#4FC3F7", "#9E9E9E", "#FFCCBC", "#E53935"]
    
    # Repeat colors for the number of days
    colors_rptd = np.tile(colors, 5)

    # Create the figure and 3D axes
    fig = plt.figure(figsize=(12, 8))
    ax = plt.axes(projection="3d")
    
    # Set title and labels
    ax.set_title("Consultas marcadas essa semana", fontsize=18)
    ax.set_zlabel("Total de consultas", fontsize=15)
    
    # Create the 3D bar chart
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors_rptd, edgecolor='k', linewidth=0.5)

    # Customize the legend
    if legend_labels is None:
        legend_labels = [
            "Dra. Marina / Pediatra", 
            "Dr. Ricardo / Oftalmologista", 
            "Dra. Ana / Ortopedista", 
            "Dr. Jonatas / Dermatologista", 
            "Dra. Leandra / Cardiologista"
        ]
    
    legend_handles = [mlines.Line2D([0], [0], color=color, marker="s", linestyle="", markersize=10) for color in colors]
    ax.legend(legend_handles, legend_labels, title="Médicos/Especialidades", loc="upper left", bbox_to_anchor=(1.05, 1))

    # Set X and Y ticks
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_xticklabels(["Segunda", "Terça", "Quarta", "Quinta", "Sexta"])
    
    ax.set_yticks([0, 1, 2, 3, 4])
    ax.set_yticklabels(["Dra. Marina", "Dr. Ricardo", "Dra. Ana", "Dr. Jonatas", "Dra. Leandra"])

    # Save the figure to a file
    plt.savefig(file_path, bbox_inches='tight')
    plt.close(fig)  # Close the figure to free memory

def contar_consultas_por_semana():
    # Obtém a data atual
    hoje = datetime.now()
    # Obtém a data do início da semana
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    # Obtém a data do final da semana
    final_semana = inicio_semana + timedelta(days=6)

    # Consulta para contar as consultas por semana
    dados = db.session.query(
        func.strftime('%Y-%m-%d', Consulta.data_hora), 
        func.count(Consulta.id)
    ).filter(
        Consulta.data_hora >= inicio_semana,
        Consulta.data_hora <= final_semana
    ).group_by(
        func.strftime('%Y-%m-%d', Consulta.data_hora)
    ).all()

    # Prepare data for plotting (dz will be the counts)
    dz = [d[1] for d in dados]  # Get counts for each day
    return dz

