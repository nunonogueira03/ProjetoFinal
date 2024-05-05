import pyodbc
from datetime import datetime
import datetime
import hashlib
import random
import string
from flask import Flask, request, send_file, jsonify
import json
import os
import io

app = Flask(__name__)

#Funcoes Genericas
#Adiciona os id's as tabelas automaticamente
def preencher_id_automaticamente(tabela):
    #Retorna o próximo ID disponível para uma tabela#
    caminho_arquivo = f"{tabela}.json"

    if not os.path.exists(caminho_arquivo):
        return 1

    # Ler os registros do arquivo JSON
    with open(caminho_arquivo, 'r') as f:
        registros = json.load(f)

    if not registros:
        return 1

    # Encontrar o maior ID
    coluna_id = next((chave for chave in registros[0].keys() if chave.lower().startswith('id')), None)
    max_id = max(registro[coluna_id] for registro in registros)

    return max_id + 1
#Coneccao com a base de dados
def conectar_db():
    # Conectar base de dados
    connection_string = f"DRIVER={{SQL SERVER}};SERVER=NUNO;DATABASE=projetofinal;Trust_Connection=yes;"
    return pyodbc.connect(connection_string)
#Ler e converter imagens em binario para poder ser guardado na base de dados
def armazenar_imagem_no_json(caminho_imagem, relatorio_info):
    # Adiciona a referência ao caminho da imagem nas informações do relatório
    relatorio_info['imagem'] = caminho_imagem

    # Caminho para o arquivo JSON
    caminho_arquivo = 'relatorios.json'

    # Ler os registros existentes
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r') as f:
            registros = json.load(f)
    else:
        registros = []

    # Adiciona o novo relatório à lista de registros
    registros.append(relatorio_info)

    # Salva a lista atualizada de volta no arquivo JSON
    with open(caminho_arquivo, 'w') as f:
        json.dump(registros, f, indent=4)

    print("Relatório com imagem armazenado no JSON.")

def obter_imagem_json(idrelatorio):
    # Caminho para o arquivo JSON
    caminho_arquivo = 'relatorios.json'

    if not os.path.exists(caminho_arquivo):
        return None

    # Ler o conteúdo do arquivo JSON
    with open(caminho_arquivo, 'r') as f:
        registros = json.load(f)

    # Procurar o relatório pelo ID
    for registro in registros:
        if registro.get('idrelatorio') == idrelatorio:
            return registro.get('imagem')

    return None

@app.route('/imagem/<int:idrelatorio>', methods=['GET'])
def devolver_imagem(idrelatorio):
    # Obter o caminho da imagem a partir do JSON
    caminho_imagem = obter_imagem_json(idrelatorio)

    if not caminho_imagem:
        return "Imagem não encontrada", 404

    # Enviar a imagem diretamente na resposta
    with open(caminho_imagem, 'rb') as f:
        dados_imagem = f.read()

    return send_file(io.BytesIO(dados_imagem), mimetype='image/jpeg')
#Validar se os valores já exitem...Utilizado no adicinar empresa, para o número de contribuinte...
def validar_unicidade(valor, chave, registros):
    #Verifica se um valor específico é único em uma lista de registros
    for registro in registros:
        if str(registro[chave]).lower() == str(valor).lower():
            return False
    return True
#Funcoes Empresa
#Adicionar tabela empresa
def adicionar_empresa(nome, numerocontribuinte, morada, contacto):
    caminho_arquivo = "empresa.json"

    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r') as f:
            registros = json.load(f)
    else:
        registros = []

    # Validar a unicidade de `numerocontribuinte` e `contacto`
    if not validar_unicidade(numerocontribuinte, 'numerocontribuinte', registros):
        return False, "Número de contribuinte já existe, por favor, insira um valor diferente."
    
    if not validar_unicidade(contacto, 'contacto', registros):
        return False, "Contacto já existe, por favor, insira um valor diferente."

    # Obter ID automático para a nova empresa
    idempresa = preencher_id_automaticamente("empresa")

    # Adicionar o novo registro
    nova_empresa = {
        'idempresa': idempresa,
        'nome': nome,
        'numerocontribuinte': numerocontribuinte,
        'morada': morada,
        'contacto': contacto
    }
    registros.append(nova_empresa)

    # Salvar a lista de registros de volta no arquivo JSON
    with open(caminho_arquivo, 'w') as f:
        json.dump(registros, f, indent=4)

    return True, "Empresa adicionada com sucesso!"

#Funcoes Utilizador
#Adicionar tabela utilizador 
def adicionar_utilizador(nome, password, numfuncionario, gmail, nome_empresa):
    # Validar o formato do e-mail
    if not validar_email(gmail):
        return False, "E-mail inválido."

    caminho_utilizadores = "utilizadores.json"
    if os.path.exists(caminho_utilizadores):
        with open(caminho_utilizadores, 'r') as f:
            registros = json.load(f)
    else:
        registros = []

    # Verificar unicidade de `numfuncionario` e `gmail`
    if not validar_unicidade(numfuncionario, 'numfuncionario', registros):
        return False, "Número de funcionário já existe."
    if not validar_unicidade(gmail, 'gmail', registros):
        return False, "E-mail já existe."

    # Preencher ID automaticamente para o novo usuário
    id_utilizador = preencher_id_automaticamente('utilizador')

    # Verificar o tipo de utilizador
    idtipoutilizador = 1 if not registros else 0

    # Gerar um novo sal e criptografar a senha
    sal = gerar_sal()
    encrypted_password = criptografar_password(sal + password)

    novo_utilizador = {
        'id_utilizador': id_utilizador,
        'nome': nome,
        'password': encrypted_password,
        'numfuncionario': numfuncionario,
        'gmail': gmail,
        'sal': sal,
        'idtipoutilizador': idtipoutilizador
    }

    registros.append(novo_utilizador)

    # Salvar a lista de registros de volta no arquivo JSON
    with open(caminho_utilizadores, 'w') as f:
        json.dump(registros, f, indent=4)

    # Associar o utilizador a uma empresa
    caminho_empresas = 'empresa.json'
    if os.path.exists(caminho_empresas):
        with open(caminho_empresas, 'r') as fe:
            empresas = json.load(fe)
    else:
        return False, f"Empresa '{nome_empresa}' não encontrada."

    idempresa = next((emp['idempresa'] for emp in empresas if emp['nome'].lower() == nome_empresa.lower()), None)

    if not idempresa:
        return False, f"Empresa '{nome_empresa}' não encontrada."

    caminho_contratos = 'contrato.json'
    if os.path.exists(caminho_contratos):
        with open(caminho_contratos, 'r') as fc:
            contratos = json.load(fc)
    else:
        contratos = []

    novo_contrato = {
        'id_utilizador': id_utilizador,
        'idempresa': idempresa
    }

    contratos.append(novo_contrato)

    with open(caminho_contratos, 'w') as fcw:
        json.dump(contratos, fcw, indent=4)

    return True, "Utilizador e contrato adicionados com sucesso!"

#Validar se o email tem os caracteres caracteristicos
def validar_email(email):
    #Verifica se o e-mail contém um '@' e um '.'
    return '@' in email and '.' in email
#Função para gerar uma string aleatória de 20 caracteres (sal)
def gerar_sal():
    #Gera uma string aleatória de 20 caracteres
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for i in range(20))

#Adiciona o sal a password introduzida e codifica
def criar_e_armazenar_password(idutilizador, password):
    # Conectar base de dados
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Gerar um novo sal
    sal = gerar_sal()
    # Armazenar o novo sal na base de dados
    cursor.execute("UPDATE utilizador SET sal = ? WHERE id_utilizador = ?", (sal, idutilizador))
    # Concatenar sal e senha e criptografar
    encrypted_password = criptografar_password(sal + password)
    # Atualizar a senha base ded dados
    cursor.execute("UPDATE utilizador SET password = ? WHERE id_utilizador = ?", (encrypted_password, idutilizador))
    # Commit e fechar conexão
    conn.commit()
    conn.close()
#Funcao de criptografar a string password
def criptografar_password(password):
    #Criptografa uma senha usando SHA-256.
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()

#Função para validar senha no login
def validar_password(idutilizador, input_password):
    caminho_utilizadores = "utilizadores.json"

    if not os.path.exists(caminho_utilizadores):
        print("Arquivo de utilizadores não encontrado.")
        return False, "Arquivo de utilizadores não encontrado."

    with open(caminho_utilizadores, 'r') as f:
        registros = json.load(f)

    # Localizar o utilizador correspondente
    for registro in registros:
        if registro['id_utilizador'] == idutilizador:
            # Obter o sal e a senha armazenada
            sal = registro['sal']
            stored_password = registro['password']

            # Criptografar a senha de entrada
            input_password_criptografada = criptografar_password(sal + input_password)

            return input_password_criptografada == stored_password, "Senha válida" if input_password_criptografada == stored_password else "Senha inválida"

    return False, "Utilizador não encontrado."
#Funcao de login
def login(nome_empresa, numfuncionario, input_password):
    # Conectar à base de dados
    conn = conectar_db()
    cursor = conn.cursor()

    # Procurar o ID da empresa pelo nome
    try:
        cursor.execute("SELECT idempresa FROM empresa WHERE nome = ?", (nome_empresa,))
        resultado_empresa = cursor.fetchone()
        if resultado_empresa is None:
            print("Empresa não encontrada.")
            return False
        idempresa = resultado_empresa[0]
    except Exception as e:
        print(f"Erro ao buscar o ID da empresa: {e}")
        conn.close()
        return False

    # Procurar o ID do utilizador pelo número de funcionário e ID da empresa
    try:
        cursor.execute("SELECT id_utilizador FROM utilizador WHERE numfuncionario = ? AND idtipoutilizador = ?",
                       (numfuncionario, idempresa))
        resultado_utilizador = cursor.fetchone()
        if resultado_utilizador is None:
            print("Utilizador não encontrado para a empresa e número de funcionário fornecidos.")
            return False
        idutilizador = resultado_utilizador[0]
    except Exception as e:
        print(f"Erro ao procurar o ID do utilizador: {e}")
        conn.close()
        return False

    # Validar a senha usando a função existente
    if validar_password(idutilizador, input_password):
        print("Login realizado com sucesso!")
        return True
    else:
        print("Senha incorreta.")
        return False

    conn.close()

#Funcoes de Exploracao
# Adicionar nova uma exploração a uma empresa
def adicionar_exploracao(nome_exploracao, idempresa):
    caminho_arquivo = "exploracao.json"

    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r') as f:
            registros = json.load(f)
    else:
        registros = []

    # Preencher ID automaticamente para a nova exploração
    idexploracao = preencher_id_automaticamente("exploracao")

    # Adicionar o novo registro
    nova_exploracao = {
        'idexploracao': idexploracao,
        'nome': nome_exploracao,
        'idempresa': idempresa
    }
    registros.append(nova_exploracao)

    # Salvar a lista de registros de volta no arquivo JSON
    with open(caminho_arquivo, 'w') as fw:
        json.dump(registros, fw, indent=4)

    print("Exploração adicionada com sucesso.")
    return idexploracao
# Adicionar fracoes e pontos a uma exploracao
def adicionar_fracoes_pontos(idexploracao, fracoes, pontos):
    caminho_pontos = "pontomapa.json"
    caminho_fracoes = "fracao.json"
    caminho_tem = "tem.json"

    # Ler os arquivos JSON existentes
    if os.path.exists(caminho_pontos):
        with open(caminho_pontos, 'r') as fp:
            registros_pontos = json.load(fp)
    else:
        registros_pontos = []

    if os.path.exists(caminho_fracoes):
        with open(caminho_fracoes, 'r') as ff:
            registros_fracoes = json.load(ff)
    else:
        registros_fracoes = []

    if os.path.exists(caminho_tem):
        with open(caminho_tem, 'r') as ft:
            registros_tem = json.load(ft)
    else:
        registros_tem = []

    # Inserir pontos no mapa
    pontos_ids = {}
    for i, ponto in enumerate(pontos):
        idponto = preencher_id_automaticamente('pontomapa')
        novo_ponto = {
            'idponto': idponto,
            'latitude': ponto['latitude'],
            'longitude': ponto['longitude'],
            'vertice': 1  # Todos os pontos são considerados vértices por padrão
        }
        registros_pontos.append(novo_ponto)
        pontos_ids[i] = idponto

    # Inserir frações e associar pontos
    for fra in fracoes:
        if len(fra['indices_pontos']) < 3:
            print(f"Erro: A fração '{fra['nome']}' precisa de pelo menos 3 pontos.")
            return False

        idfracao = preencher_id_automaticamente('fracao')
        nova_fracao = {
            'idfracao': idfracao,
            'nome': fra['nome'],
            'descricao': fra['descricao'],
            'idexploracao': idexploracao
        }
        registros_fracoes.append(nova_fracao)

        # Associar pontos à fração
        for indice_ponto in fra['indices_pontos']:
            idponto = pontos_ids[indice_ponto]
            novo_tem = {
                'idponto': idponto,
                'idfracao': idfracao
            }
            registros_tem.append(novo_tem)

    # Salvar os arquivos atualizados
    with open(caminho_pontos, 'w') as fpw:
        json.dump(registros_pontos, fpw, indent=4)

    with open(caminho_fracoes, 'w') as ffw:
        json.dump(registros_fracoes, ffw, indent=4)

    with open(caminho_tem, 'w') as ftw:
        json.dump(registros_tem, ftw, indent=4)

    print("Frações e pontos adicionados com sucesso.")
    return True
#Função que permitirá desenhar a exploração no mapa com todas as frações
def recuperar_fracoes_e_pontos(idexploracao):
    # Caminho para os arquivos JSON
    caminho_fracoes = "fracao.json"
    caminho_pontos = "pontomapa.json"
    caminho_tem = "tem.json"

    # Carregar dados dos arquivos JSON
    try:
        with open(caminho_fracoes, 'r') as ff:
            fracoes = json.load(ff)
        with open(caminho_pontos, 'r') as fp:
            pontos = json.load(fp)
        with open(caminho_tem, 'r') as ft:
            tem = json.load(ft)
    except FileNotFoundError as e:
        print(f"Erro ao carregar arquivos JSON: {e}")
        return None

    # Filtrar frações pela exploração
    fracoes_exploracao = [fra for fra in fracoes if fra['idexploracao'] == idexploracao]

    # Preparar dados para retorno
    resultado = []
    for fra in fracoes_exploracao:
        # Encontrar todos os pontos associados à fração
        pontos_fracao = [p for p in pontos if any(t['idponto'] == p['idponto'] and t['idfracao'] == fra['idfracao'] for t in tem)]
        resultado.append({
            'idfracao': fra['idfracao'],
            'nome': fra['nome'],
            'pontos': pontos_fracao
        })

    return resultado
#Função altera 4 tabelas sensor, medida, ponto mapa, tem
def adicionar_sensor(nome_sensor, unidade, latitude, longitude, idfracao):
    caminho_pontos = "pontomapa.json"
    caminho_sensores = "sensor.json"
    caminho_tem = "tem.json"
    caminho_medidas = "medida.json"

    # Ler os arquivos existentes
    if os.path.exists(caminho_pontos):
        with open(caminho_pontos, 'r') as fp:
            registros_pontos = json.load(fp)
    else:
        registros_pontos = []

    if os.path.exists(caminho_sensores):
        with open(caminho_sensores, 'r') as fs:
            registros_sensores = json.load(fs)
    else:
        registros_sensores = []

    if os.path.exists(caminho_tem):
        with open(caminho_tem, 'r') as ft:
            registros_tem = json.load(ft)
    else:
        registros_tem = []

    if os.path.exists(caminho_medidas):
        with open(caminho_medidas, 'r') as fm:
            registros_medidas = json.load(fm)
    else:
        registros_medidas = []

    # Adicionar ponto no mapa
    idponto = preencher_id_automaticamente('pontomapa')
    novo_ponto = {
        'idponto': idponto,
        'latitude': latitude,
        'longitude': longitude,
        'vertice': 0
    }
    registros_pontos.append(novo_ponto)

    # Adicionar sensor associado a esse ponto
    idsensor = preencher_id_automaticamente('sensor')
    novo_sensor = {
        'idsensor': idsensor,
        'nome': nome_sensor,
        'unidade': unidade,
        'idponto': idponto
    }
    registros_sensores.append(novo_sensor)

    # Associar o ponto de mapa à fração
    novo_tem = {
        'idponto': idponto,
        'idfracao': idfracao
    }
    registros_tem.append(novo_tem)

    # Adicionar uma medida inicial
    idmedida = preencher_id_automaticamente('medida')
    data_atual = datetime.datetime.now().strftime('%Y-%m-%d')

    nova_medida = {
        'idmedida': idmedida,
        'data': data_atual,
        'valor': 0,
        'idsensor': idsensor
    }
    registros_medidas.append(nova_medida)

    # Salvar os arquivos atualizados
    with open(caminho_pontos, 'w') as fpw:
        json.dump(registros_pontos, fpw, indent=4)

    with open(caminho_sensores, 'w') as fsw:
        json.dump(registros_sensores, fsw, indent=4)

    with open(caminho_tem, 'w') as ftw:
        json.dump(registros_tem, ftw, indent=4)

    with open(caminho_medidas, 'w') as fmw:
        json.dump(registros_medidas, fmw, indent=4)

    print("Sensor e informações associadas adicionados com sucesso.")
    return True
#Função que atualiza o valor do sensor e a data
def atualizar_medida_sensor(idsensor, novo_valor):
    caminho_medidas = "medida.json"

    if not os.path.exists(caminho_medidas):
        print("Arquivo de medidas não encontrado.")
        return False

    # Ler as medidas existentes
    with open(caminho_medidas, 'r') as f:
        registros_medidas = json.load(f)

    # Encontrar a medida mais recente para o sensor especificado
    medidas_sensor = [medida for medida in registros_medidas if medida['idsensor'] == idsensor]
    if not medidas_sensor:
        print("Nenhuma medida encontrada para o sensor especificado.")
        return False

    # Ordenar por data (do mais recente para o mais antigo)
    medidas_sensor.sort(key=lambda m: datetime.datetime.strptime(m['data'], '%Y-%m-%d'), reverse=True)
    idmedida = medidas_sensor[0]['idmedida']

    # Atualizar o registro
    data_atual = datetime.datetime.now().strftime('%Y-%m-%d')
    for medida in registros_medidas:
        if medida['idmedida'] == idmedida:
            medida['valor'] = novo_valor
            medida['data'] = data_atual
            break

    # Salvar o arquivo atualizado
    with open(caminho_medidas, 'w') as fw:
        json.dump(registros_medidas, fw, indent=4)

    print("Medida do sensor atualizada com sucesso.")
    return True
#Funcao para criar tabela relatorio
def criar_relatorio(nome, descricao, caminho_imagem, idfracao):
    caminho_relatorios = "registorelatorio.json"
    caminho_estar = "estar.json"
    caminho_fracao = "fracao.json"

    # Ler os registros existentes
    registros_relatorios, registros_estar = [], []
    try:
        with open(caminho_relatorios, 'r') as fr:
            registros_relatorios = json.load(fr)
        with open(caminho_estar, 'r') as fe:
            registros_estar = json.load(fe)
    except FileNotFoundError:
        print("Alguns arquivos JSON não foram encontrados e serão criados.")

    # Verificar se a fração fornecida existe
    registros_fracao = []
    try:
        with open(caminho_fracao, 'r') as ff:
            registros_fracao = json.load(ff)
    except FileNotFoundError:
        print("Erro: O arquivo de frações não existe.")
        return False

    if not any(f['idfracao'] == idfracao for f in registros_fracao):
        print("Erro: A fração fornecida não existe.")
        return False

    # Converter a imagem para dados armazenáveis
    dados_imagem = armazenar_imagem_no_json(caminho_imagem)

    # Obter ID automático para o novo relatório
    idrelatorio = preencher_id_automaticamente('registorelatorio')

    # Adicionar o novo relatório
    novo_relatorio = {
        'idrelatorio': idrelatorio,
        'nome': nome,
        'descricao': descricao,
        'imagem': dados_imagem,
        'idfracao': idfracao
    }
    registros_relatorios.append(novo_relatorio)

    # Associar o relatório ao estado inicial
    data_atual = datetime.datetime.now().strftime('%Y-%m-%d')
    novo_estar = {
        'idrelatorio': idrelatorio,
        'idestado': 0,
        'data': data_atual
    }
    registros_estar.append(novo_estar)

    # Salvar os arquivos atualizados
    with open(caminho_relatorios, 'w') as frw:
        json.dump(registros_relatorios, frw, indent=4)
    with open(caminho_estar, 'w') as few:
        json.dump(registros_estar, few, indent=4)

    print("Relatório criado com sucesso.")
    return True
#Cria as tarefas associadas ao relatorio
def criar_tarefa_associada_relatorio(nome_tarefa, descricao, idrelatorio):
    caminho_tarefa = "tarefa.json"
    caminho_estat = "estat.json"
    caminho_fornece = "fornece.json"

    # Carregar ou inicializar os dados JSON
    tarefas, estados, fornecimentos = [], [], []
    for caminho, lista in [(caminho_tarefa, tarefas), (caminho_estat, estados), (caminho_fornece, fornecimentos)]:
        if os.path.exists(caminho):
            with open(caminho, 'r') as file:
                lista.extend(json.load(file))

    # Adicionar nova tarefa
    idtarefa = preencher_id_automaticamente('tarefa')
    nova_tarefa = {
        'idtarefa': idtarefa,
        'nome': nome_tarefa,
        'descricao': descricao
    }
    tarefas.append(nova_tarefa)

    # Adicionar estado inicial da tarefa
    idestat = preencher_id_automaticamente('estat')
    novo_estat = {
        'data': datetime.datetime.now().strftime('%Y-%m-%d'),
        'idestat': idestat,
        'idtarefa': idtarefa
    }
    estados.append(novo_estat)

    # Associar tarefa ao relatório
    novo_fornece = {
        'idrelatorio': idrelatorio,
        'idtarefa': idtarefa
    }
    fornecimentos.append(novo_fornece)

    # Salvar dados atualizados
    for caminho, dados in [(caminho_tarefa, tarefas), (caminho_estat, estados), (caminho_fornece, fornecimentos)]:
        with open(caminho, 'w') as file:
            json.dump(dados, file, indent=4)

    print(f"Tarefa '{nome_tarefa}' criada e associada ao relatório ID {idrelatorio} com estado inicializado.")
    return True


#Outras
#Testes
def sao_iguais(valor1, valor2):
    # Converte os valores para minúsculas antes de compará-los
    valor1_lower = str(valor1).lower()
    valor2_lower = str(valor2).lower()

    if valor1_lower == valor2_lower:
        return print("sim")
    else:
        return print("nao")
#teste para escrever na base de dados
def escreverdb():
    connection_string = f"""
        DRIVER={{{'SQL SERVER'}}};
        SERVER={'NUNO'};
        DATABASE={'projetofinal'};
        Trust_Connection=yes;
    """
    conn = pyodbc.connect(connection_string)
    print(conn)
    # Criação de um cursor
    cursor = conn.cursor()

    # Pedir ao usuário para inserir os valores
    idempresa = input("Digite o ID da empresa: ")
    nome = input("Digite o nome da empresa: ")

    # Query SQL para inserir os valores
    sql_query = "INSERT INTO empresa (idempresa, nome) VALUES (?, ?)"

    # Executar a query
    cursor.execute(sql_query, (idempresa, nome))

    # Confirmar a transação
    conn.commit()

    # Fechar a conexão
    conn.close()
#verificar se existe alguma coluna com data na tabela
def validar_se_possui_data_na_tabela(tabela, *args):
    # Conectar base de dados
    conn = conectar_db()
    cursor = conn.cursor()

    if [arg for arg in args if arg == "data"]:
           return True
    return False
#Introduzir valores numa tabela em que uma das colunas é a data e introduz automáticamente a data
def tabela_com_data(tabela, *args):
    # Conectar base de dados
    conn = conectar_db()
    cursor = conn.cursor()

    args_sem_data = [arg for arg in args if arg != "data"]
    data_atual = datetime.now()

    placeholders = ",".join(["?" for _ in args_sem_data])
    sql_query = f"INSERT INTO {tabela} VALUES ({placeholders}, ?)"
    cursor.execute(sql_query, args_sem_data + [data_atual])

    # Confirmar a transação e fechar a conexão
    conn.commit()
    conn.close()
#Introduzir valores numa tabela em que nenhuma das colunas possui data
def tabela_sem_data(tabela, *args):
    # Conectar base de dados
    conn = conectar_db()
    cursor = conn.cursor()

    placeholders = ",".join(["?" for _ in args])
    sql_query = f"INSERT INTO {tabela} VALUES ({placeholders})"
    cursor.execute(sql_query, args)

    # Confirmar a transação e fechar a conexão
    conn.commit()
    conn.close()
# Verificar se ja existe algum valor igual na tabela
def validar_strings_de_uma_tabela(valor, tabela, coluna):
    # Conectar base de dados
    conn = conectar_db()
    cursor = conn.cursor()
    
   # Consultar todos os valores da coluna na tabela
    cursor.execute(f"SELECT {coluna} FROM {tabela}")
    valores_bd = [str(row[0]).lower() for row in cursor.fetchall()]

    # Converter o valor introduzido para minúsculas (se for uma string)
    if isinstance(valor, str):
        valor_lower = valor.lower()
    else:
        valor_lower = valor

    # Verificar se o valor é diferente de todos os outros valores
    if valor_lower not in valores_bd:
        return True
    else:
        return False
def ler_valor_db(coluna_retorno, tabela, coluna_condicao, valor_condicao):
    # Conectar base de dados
    conn = conectar_db()
    cursor = conn.cursor()

    # Construir a consulta SQL
    sql_query = f"SELECT {coluna_retorno} FROM {tabela} WHERE {coluna_condicao} = ?"

    # Executar a consulta SQL com o valor da condição como parâmetro
    cursor.execute(sql_query, (valor_condicao,))

    # Ler o valor da coluna de retorno
    valor = cursor.fetchone()[0]

    # Fechar a conexão com a base de dados
    conn.close()

    return valor
def alterar_valor_db(tabela, coluna, novo_valor, condicao_coluna, condicao_valor):
    # Conectar base de dados
    conn = conectar_db()
    cursor = conn.cursor()

    # Construir a consulta SQL para a atualização
    sql_query = f"UPDATE {tabela} SET {coluna} = ? WHERE {condicao_coluna} = ?"

    # Executar a consulta SQL com os novos valores e a condição
    cursor.execute(sql_query, (novo_valor, condicao_valor))

    # Confirmar a transação e fechar a conexão
    conn.commit()
    conn.close()
def pontos_do_mapa_por_fracao(id_fracao):
    # Conectar base de dados
    conn = conectar_db()
    cursor = conn.cursor()

    sql_query = """
        SELECT *
        FROM pontomapa
        WHERE idfracao = ?
    """

    cursor.execute(sql_query, (id_fracao,))
    pontos = cursor.fetchall()

    conn.close()

    return pontos
def fracoes_por_exploracao(id_exploracao):
    # Conectar base de dados
    conn = conectar_db()
    cursor = conn.cursor()

    sql_query = """
        SELECT *
        FROM fracao
        WHERE idexploracao = ?
    """

    cursor.execute(sql_query, (id_exploracao,))
    fracoes = cursor.fetchall()

    conn.close()

    return fracoes
def exploracao_por_empresa(id_empresa):
    # Conectar base de dados
    conn = conectar_db()
    cursor = conn.cursor()

    sql_query = """
        SELECT *
        FROM exploracao
        WHERE idempresa = ?
    """

    cursor.execute(sql_query, (id_empresa,))
    exploracao = cursor.fetchall()

    conn.close()

    return exploracao

if __name__ == '__main__':
    app.run(debug=True)