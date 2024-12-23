# users/views.py
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from projeto_clinica import db
from projeto_clinica.models import Paciente, Medico, Consulta
from projeto_clinica.usuarios.forms import RegistrationForm, LoginForm, UpdateUserForm
from datetime import datetime
from datetime import timedelta
from werkzeug.security import generate_password_hash
from email.message import EmailMessage
import smtplib

usuarios = Blueprint('users', __name__)

from datetime import datetime, timedelta


@usuarios.route('/login', methods=['GET', 'POST'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        
        usuario = Paciente.query.filter_by(email=form.email.data).first()
        
        if usuario is not None and usuario.check_password(form.password.data):
            
            login_user(usuario)
            flash('Log in feito com sucesso!')
            
            next = request.args.get('next')
            
            if next == None or not next[0] == '/':
                next = url_for('core.index')
            
            return redirect(next)
    
    return render_template('login.html', form = form)



@usuarios.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = RegistrationForm()  
    
    if form.validate_on_submit():
        # The hashed password is handled in the __init__ method
        novo_paciente = Paciente(
            nome=form.nome.data,
            idade=form.idade.data,
            cpf=form.cpf.data,
            email=form.email.data,
            convenio=form.convenio.data,
            pagamento=form.pagamento.data,
            senha=form.password.data  # Just pass the plain password
        )
        
        db.session.add(novo_paciente)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso!', 'success')
        
        return redirect(url_for('core.index'))  # Adjust the redirect if necessary
    
    return render_template('cadastro.html', form=form)


def send_email(user_email, nome_paciente, data_consulta, horario_consulta, nome_medico):
    email_body = f"""\
    <p> Prezado(a) {nome_paciente}, </p>
    <p> Estamos enviando este e-mail para confirmar sua consulta agendada. </p>
    <p> <strong>Detalhes da Consulta:</strong> </p>
    <p> Data: {data_consulta} </p>
    <p> Horário: {horario_consulta} </p>
    <p> Médico: Dr(a). {nome_medico} </p>
    <p> Atenciosamente, </p>
    <p> Clínica Cuidado Integral</p>
    """

    msg = EmailMessage()
    msg["Subject"] = "Consulta Agendada"  # Título do e-mail
    msg["From"] = "t3st.dummy2077@gmail.com"  # Conta que manda o e-mail
    msg["To"] = user_email  # Enviar para o e-mail do usuário
    password = "anfmvkkdzojdymcf"  # Senha da conta

    msg.set_content(email_body, subtype='html')  # Define o corpo do e-mail como HTML

    # Configuração do servidor SMTP
    smt = smtplib.SMTP("smtp.gmail.com", 587)
    smt.starttls()  # Inicia a conexão
    try:
        smt.login(msg["From"], password)  # Login no servidor SMTP
        smt.sendmail(msg["From"], msg["To"], msg.as_string())  # Envio do e-mail
        print("E-mail enviado com sucesso!")

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")  # Trata as exceções
    finally:
        smt.quit()  # Encerra a conexão com o servidor SMTP

@usuarios.route('/conta', methods=['GET', 'POST'])
@login_required
def conta():
    form = UpdateUserForm()

    if request.method == 'GET':
        # Preencher os campos do formulário com os dados atuais do usuário
        form.email.data = current_user.email
        form.nome.data = current_user.nome
        form.pagamento.data = current_user.pagamento  # Definir o valor atual do método de pagamento
        form.convenio.data = current_user.convenio  # Definir o valor atual do convênio

    if form.validate_on_submit():
        # Atualizar os dados do usuário
        current_user.email = form.email.data
        current_user.nome = form.nome.data
        current_user.pagamento = form.pagamento.data  # Atualizar o método de pagamento
        current_user.convenio = form.convenio.data  # Atualizar o status de convênio
        
        # Atualizar a senha se o usuário forneceu uma nova
        if form.nova_senha.data:
            current_user.password_hash = generate_password_hash(form.nova_senha.data)

        # Confirmar as mudanças no banco de dados
        db.session.commit()

        # Atualizar a sessão do usuário para aplicar as alterações imediatamente
        login_user(current_user)

        flash('Informações atualizadas com sucesso!', 'success')
        return redirect(url_for('users.conta'))

    return render_template('conta.html', form=form)

@usuarios.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


@usuarios.route('/pagina_usuario')
@login_required
def pagina_usuario():
    usuario = Paciente.query.get(current_user.id)
    consultas_agendadas = Consulta.query.filter_by(paciente_id=current_user.id).all()
    
    # Converter "y"/"n" em "Sim"/"Não" para o convênio
    convenio_formatado = "Sim" if usuario.convenio == "y" else "Não"

    # Passa as informações de pagamento e convênio para o template
    return render_template(
        'pagina_usuario.html', 
        consultas=consultas_agendadas,
        usuario=usuario,
        convenio_formatado=convenio_formatado,
        metodo_pagamento=usuario.pagamento
    )

@usuarios.route('/deletar_conta', methods=['POST'])
@login_required
def deletar_conta():
    usuario = current_user

    # Remover todas as consultas associadas ao usuário
    consultas = Consulta.query.filter_by(paciente_id=usuario.id).all()
    for consulta in consultas:
        db.session.delete(consulta)

    # Excluir o usuário do banco de dados
    db.session.delete(usuario)
    db.session.commit()
    
    flash("Sua conta foi excluída com sucesso.", "success")
    logout_user()  # Logout do usuário após a exclusão
    return redirect(url_for("core.index"))

@usuarios.route('/consultas/cancelar/<int:consulta_id>', methods=['POST'])
@login_required
def cancelar_consulta(consulta_id):
    consulta = Consulta.query.get_or_404(consulta_id)

    # Verifica se o usuário atual é o paciente que agendou a consulta
    if consulta.paciente_id == current_user.id:
        db.session.delete(consulta)
        db.session.commit()
        flash("Consulta cancelada com sucesso!", "success")
    else:
        flash("Acesso não autorizado para cancelar esta consulta.", "danger")

    return redirect(url_for('users.pagina_usuario'))



def parse_horario(horario_str):
    if not horario_str:
        raise ValueError("Horário selecionado não pode ser vazio.")
    
    partes = horario_str.split(' - ')
    if len(partes) != 2:
        raise ValueError("Formato de horário inválido. Use 'dia hora_inicio - hora_fim'.")
    
    hora_range = partes[1].strip()
    dia_hora = partes[0].strip().split(' ', 1)

    if len(dia_hora) != 2:
        raise ValueError("Formato de dia inválido. Use 'dia hora_inicio'.")
    
    dia = dia_hora[0].strip()
    hora_inicio = dia_hora[1].strip()
    
    dias_da_semana = {
    "segunda": 0, "terça": 1, "terca": 1, "quarta": 2,
    "quinta": 3, "sexta": 4, "sabado": 5, "domingo": 6,
    "sabádo": 5  # Adicionando a variante com acento
    }   

    if dia.lower() not in dias_da_semana:
        raise KeyError(f'Dia inválido: {dia}. Use um dia da semana válido.')
    
    hora_fim = hora_range.strip()
    hoje = datetime.now().date()
    dia_atual = hoje.weekday()
    dias_ate_dia = (dias_da_semana[dia.lower()] - dia_atual) % 7
    data_horario = hoje + timedelta(days=dias_ate_dia)
    
    horario_inicio = datetime.strptime(f"{data_horario} {hora_inicio}", "%Y-%m-%d %H:%M")
    horario_fim = datetime.strptime(f"{data_horario} {hora_fim}", "%Y-%m-%d %H:%M")
    
    return horario_inicio, horario_fim

@usuarios.route('/agendar/<int:medico_id>', methods=['GET', 'POST'])
@login_required
def agendar_consulta(medico_id):
    medico = Medico.query.get_or_404(medico_id)
    preco_base = 200.00
    preco_final = preco_base  # Define preco_final também no método GET
    desconto_aplicado = 0

    # Aplica descontos de forma composta
    if current_user.pagamento == 'avst':  # À vista
        preco_final *= 0.95  # Aplica desconto de 5%
        desconto_aplicado += 5  # Desconto de 5% por pagamento à vista
    if current_user.convenio == 'y':  # Com convênio
        preco_final *= 0.85  # Aplica desconto adicional de 15% sobre o valor com desconto
        desconto_aplicado += 15  # Desconto de 15% por convênio

    if request.method == 'POST':
        horario_selecionado = request.form['horario']
        descricao = request.form['descricao']
        horario_inicio, horario_fim = parse_horario(horario_selecionado)
        dia_da_semana = horario_inicio.strftime('%A')

        # Verificação de sobreposição de horários
        consultas_agendadas = Consulta.query.filter_by(medico_id=medico_id).all()
        for consulta in consultas_agendadas:
            if (horario_inicio < consulta.data + timedelta(hours=1) and
                horario_fim > consulta.data):
                flash('Esse horário já está ocupado. Por favor, escolha outro.', 'danger')
                return redirect(url_for('users.agendar_consulta', medico_id=medico_id))

        nova_consulta = Consulta(
            data=horario_inicio,
            descricao=descricao,
            paciente_id=current_user.id,
            medico_id=medico_id,
            dia_da_semana=dia_da_semana,
            preco=preco_final
        )

        db.session.add(nova_consulta)
        db.session.commit()

        # Envia e-mail para o usuário com os detalhes da consulta
        send_email(current_user.email, current_user.nome, horario_inicio.strftime('%d/%m/%Y'), 
                   horario_inicio.strftime('%H:%M'), medico.nome)

        flash(f'Consulta agendada com sucesso! Preço final: R$ {preco_final:.2f}', 'success')
        return redirect(url_for('users.confirmacao_agendamento'))

    # Configura horários disponíveis e ocupados
    consultas_agendadas = Consulta.query.filter_by(medico_id=medico_id).all()
    horarios_disponiveis = []
    horarios_ocupados = []

    if medico.horarios:
        horarios_trabalho = medico.horarios.split(",")
        for consulta in consultas_agendadas:
            horarios_ocupados.append(consulta.data.strftime('%A %H:%M - %H:%M'))
        for horario in horarios_trabalho:
            horario_base = " ".join(horario.split()[:2])
            if horario_base not in horarios_ocupados:
                horarios_disponiveis.append(horario)

    return render_template(
        'consulta_agendamento.html',
        medico=medico,
        horarios_disponiveis=horarios_disponiveis,
        horarios_ocupados=horarios_ocupados,
        preco_base=preco_base,  # Passa preco_base para o template
        preco_final=preco_final,  # Passa preco_final para o template
        desconto_aplicado=desconto_aplicado  # Passa desconto_aplicado para o template
    )
    

@usuarios.route('/confirmacao_agendamento')
@login_required
def confirmacao_agendamento():
    return render_template('confirmacao_agendamento.html')



@usuarios.route('/medicos')
def acessar_medicos():
    medicos = Medico.query.all()  # Obtém todos os médicos do banco de dados
    return render_template('medicos.html', medicos=medicos)