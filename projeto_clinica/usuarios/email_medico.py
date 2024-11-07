from email.message import EmailMessage
import smtplib

def send_email():
    email_body = """\
    <p> Prezado(a) Dr(a). [Nome do Médico], </p>
    <p> Gostaria de confirmar a consulta agendada para [data], às [horário] e com o paciente [nome do paciente] </p>
    <p> Atenciosamente, </p>
    <p> Clínica UEPB </p>
    """

    msg = EmailMessage()
    msg["Subject"] = "Consulta Agendada" # Titulo do e-mail
    msg["From"] = "t3st.dummy2077@gmail.com" # Conta que manda o e-mail
    msg["To"] = "t3st.dummy2077@gmail.com" # Conta que recebe o e-mail
    password = "anfmvkkdzojdymcf"

    msg.set_content(email_body, subtype='html') # Define o corpo do e-mail como HTML

    # Configuração do servidor SMTP
    smt = smtplib.SMTP("smtp.gmail.com", 587)
    smt.starttls()  # Inicia a conexão
    try:
        smt.login(msg["From"], password)  # Login no servidor SMTP
        smt.sendmail(msg["From"], msg["To"], msg.as_string())  # Envio do e-mail
        print("E-mail enviado com sucesso!")

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}") # Trata as exceções
    finally:
        smt.quit()  # Encerra a conexão com o servidor SMTP

send_email()