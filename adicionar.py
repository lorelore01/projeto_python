from projeto_clinica import app, db
from projeto_clinica.models import Medico
from datetime import datetime

dias_da_semana = {
    'segunda': 'Monday',
    'terça': 'Tuesday',
    'quarta': 'Wednesday',
    'quinta': 'Thursday',
    'sexta': 'Friday',
    'sábado': 'Saturday',
    'domingo': 'Sunday'
}

def parse_horario(horario_str):
    for pt, en in dias_da_semana.items():
        horario_str = horario_str.replace(pt, en)
    
    if ' ' in horario_str:
        return datetime.strptime(horario_str.strip(), '%A %H:%M - %H:%M')
    else:
        return datetime.strptime(horario_str.strip(), '%H:%M - %H:%M')

def adicionar_horarios():
    print("Iniciando adição de horários...")
    with app.app_context():
        try:
            horarios_por_medico = {
                1: ['segunda 09:00 - 10:00', 'quarta 14:00 - 15:00', 'sexta 16:00 - 17:00'],
                2: ['segunda 16:00 - 17:00', 'terça 14:00 - 15:00', 'quarta 16:00 - 17:00'],
                3: ['quarta 09:00 - 10:00', 'quinta 15:00 - 16:00', 'sexta 15:00 - 16:00'],
                4: ['segunda 14:00 - 15:00', 'terça 14:00 - 15:00', 'quarta 14:00 - 15:00'],
                5: ['segunda 13:00 - 14:00', 'terça 15:00 - 16:00', 'quarta 13:00 - 14:00']
            }

            for medico_id, horarios in horarios_por_medico.items():
                medico = Medico.query.get(medico_id)
                if medico:
                    horarios_formatados = []
                    for horario in horarios:
                        horario_str = horario.strip()
                        horarios_formatados.append(horario_str)

                    medico.horarios = ', '.join(horarios_formatados)
                    print(f"Horários atualizados para {medico.nome}: {medico.horarios}")
                else:
                    print(f"Médico com ID {medico_id} não encontrado.")

            db.session.commit()
            print("Atualizações confirmadas no banco de dados.")

        except Exception as e:
            print(f"Ocorreu um erro ao adicionar os horários: {e}")
            db.session.rollback()

if __name__ == '__main__':
    adicionar_horarios()
