from mpl_toolkits.mplot3d import Axes3D
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np

#Onde as barras irão ficar no primeiro plano
xpos = np.repeat([0, 1, 2, 3, 4], 5)  # Dias da Semana repetidos para cada especialidade
ypos = np.tile([0, 1, 2, 3, 4], 5)  # Médicos/Especialidades repetidos para cada dia da semana
zpos = [0] * 25 #Chão

dx = np.ones_like(xpos)*0.3 #Grossura das barras no eixo X
dy = np.ones_like(ypos)*0.3 #Grossura das barras no eixo Y
dz = [25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1] #Altura das barras no eixo Z (Total de consultas vai aqui)

colors = ["#8BC34A", "#4FC3F7", "#9E9E9E", "#FFCCBC", "#E53935"] #As cores para cada médico
colors_rptd = np.tile(colors, 5)  #Repete as cores dos médicos para cada dia da semana

fig = plt.figure(figsize=(12,8)) #Gera o vizualidor?
ax = plt.axes(projection="3d") #Seta o ambiente de plotagem
ax.set_title("Consultas marcadas essa semana", fontsize=18) #Coloca o titulo do grafico
ax.set_zlabel("Total de consultas", fontsize=15) #Coloca um nome ao lado do eixo Z
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color = colors_rptd, edgecolor='k', linewidth=0.5) #Coloca as barras no ambiente de plotagem

#Customização da legenda
legend_labels = ["Dra. Marina / Pediatra", "Dr. Ricardo / Oftamologista", "Dra. Ana / Ortopedista", "Dr. Jonatas / Dermatologista", "Dra. Leandra / Cardiologista"] #Coloca os nomes/especialidades na legenda
legend_handles = [mlines.Line2D([0], [0], color=color, marker="s", linestyle="", markersize=10) for color in colors] #Cria uma lista de "handles" que serão usados na legenda, pegando as cores dos médicos
ax.legend(legend_handles, legend_labels, title="Médicos/Especialidades", loc="upper left", bbox_to_anchor=(1.05, 1)) #Adiciona a legenda na direita superior do plot

ax.set_xticks([0, 1, 2, 3, 4]) #Seta os ticks do X para alinhar
ax.set_xticklabels(["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]) #Renomeia os ticks do X

ax.set_yticks([0, 1, 2, 3, 4]) #Seta os ticks do Y para alinhar
ax.set_yticklabels(["Dra. Marina", "Dr. Ricardo", "Dra. Ana", "Dr. Jonatas", "Dra. Leandra"]) #Renomeia os ticks do Y

plt.show()