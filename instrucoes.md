0. antes de alterar qualquer coisa, dar 'git pull' para pegar alterações dos outros
1. alguem altera algum arquivo
2. essa pessoa adiciona as alterações com 'git add'
3. faz commit(cria uma nova "versão") com 'git commit'
4. dá push (envia) a versão nova para oo github com 'git push'

# ---> arrumar a criação do arquivo .db (tem que ser criado sempre no mesmo diretório)

# como lidar com agendamento de consultas:
> (opção onde Lorenzo usa Jinja)
1. ao invés de ter vários arquivos horario_medicoN > ter só um horario que recebe os parâmetros (nome do médico e horários pra mostrar na tela)
2. ter uma tabela com os horários de cada médico (para utilizar na renderização da lista de médicos e do médico em si)
3. adicionar javascript ao botão "agendar consulta" que envie um POST ao back-end com o horário e médico escolhido
3.1 caso o horário esteja disponível, retornar algo que indique o mesmo (e no front-end usar isso para mostrar uma janela de confirmação)
3.2 caso não esteja, retornar algo que indique (e no front-end uasr isso para mostrar uma janela de erro)

### FALTA FAZER ### 
1. Integrar o gráfico ao site 
2. Adicionar sistema de pagamentos baseado no convênio 
