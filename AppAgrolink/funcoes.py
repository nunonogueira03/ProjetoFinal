import pyodbc
from datetime import datetime
import hashlib
import random
import string

#Funcoes Genericas
#Adiciona os id's as tabelas automaticamente
def preencher_id_automaticamente(tabela):
    # Conectar base de dados
    conn = conectar_db()
    cursor = conn.cursor()

    # Obter as colunas da tabela
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tabela}'")
    colunas = cursor.fetchall()

    # Procurar por uma coluna que comece com 'id'
    for coluna in colunas:
        if coluna[0].lower().startswith('id'):
            # Consultar o máximo valor atual da coluna de ID
            cursor.execute(f"SELECT MAX({coluna[0]}) FROM {tabela}")
            max_id = cursor.fetchone()[0]

            # Se não houver nenhum dado na tabela, o máximo valor do ID será None
            # Neste caso, devolvemos 1 diretamente
            if max_id is None:
                return 1

            # Incrementar o máximo valor atual em 1 para obter o próximo ID disponível
            proximo_id = max_id + 1

            # Devolver o próximo ID disponível
            return proximo_id

    # Se nenhuma coluna de ID for encontrada, retornar None
    return None
#Coneccao com a base de dados
def conectar_db():
    # Conectar base de dados
    connection_string = f"DRIVER={{SQL SERVER}};SERVER=NUNO;DATABASE=projetofinal;Trust_Connection=yes;"
    return pyodbc.connect(connection_string)

#Funcoes Empresa
#Adicionar tabela empresa
def adicionar_empresa(nome, numerocontribuinte, morada, contacto):
    # Conectar à base de dados
    conn = conectar_db()
    cursor = conn.cursor()

    # Verifica se o número de contribuinte já existe
    if not validar_strings_de_uma_tabela(numerocontribuinte, 'empresa', 'numerocontribuinte'):
        conn.close()
        return False, "Número de contribuinte já existe, por favor, insira um valor diferente."

    # Verifica se o contacto já existe
    if not validar_strings_de_uma_tabela(contacto, 'empresa', 'contacto'):
        conn.close()
        return False, "Contacto já existe, por favor, insira um valor diferente."

    # Obter ID automático para a nova empresa
    idempresa = preencher_id_automaticamente('empresa')

    # Preparar a consulta SQL para inserir os dados da empresa
    query = """
    INSERT INTO empresa (idempresa, nome, numerocontribuinte, morada, contacto)
    VALUES (?, ?, ?, ?, ?)
    """
    values = (idempresa, nome, numerocontribuinte, morada, contacto)

    # Executar a consulta
    try:
        cursor.execute(query, values)
        conn.commit()
        print("Empresa adicionada com sucesso!")
        return True, "Empresa adicionada com sucesso!"
    except Exception as e:
        print(f"Erro ao adicionar a empresa: {e}")
        return False, f"Erro ao adicionar a empresa: {e}"
    finally:
        conn.close()

#Funcoes Utilizador
#Adicionar tabela utilizador 
def adicionar_utilizador(nome, password, numfuncionario, gmail, nome_empresa):
    # Conectar à base de dados
    conn = conectar_db()
    cursor = conn.cursor()

    # Validar o formato do email
    if not validar_email(gmail):
        conn.close()
        return False, "Email inválido."

    # Verificar se o número do funcionário e o email já existem
    if not validar_strings_de_uma_tabela(numfuncionario, 'utilizador', 'numfuncionario'):
        conn.close()
        return False, "Número de funcionário já existe."
    if not validar_strings_de_uma_tabela(gmail, 'utilizador', 'gmail'):
        conn.close()
        return False, "Email já existe."

    # Obter ID automático para o novo utilizador
    id_utilizador = preencher_id_automaticamente('utilizador')

    # Verificar se é o primeiro utilizador para definir o tipo de utilizador
    cursor.execute("SELECT COUNT(*) FROM utilizador")
    count = cursor.fetchone()[0]
    idtipoutilizador = 1 if count == 0 else 0

    # Gerar um novo sal e encriptar a senha
    sal = gerar_sal()
    encrypted_password = criptografar_password(sal + password)

    try:
        cursor.execute("""
            INSERT INTO utilizador (nome, id_utilizador, password, numfuncionario, gmail, sal, idtipoutilizador)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nome, id_utilizador, encrypted_password, numfuncionario, gmail, sal, idtipoutilizador))
        conn.commit()
    except Exception as e:
        conn.close()
        return False, f"Erro ao adicionar o utilizador: {e}"

    try:
        cursor.execute("SELECT idempresa FROM empresa WHERE nome = ?", (nome_empresa,))
        empresa_info = cursor.fetchone()
        if empresa_info is None:
            conn.close()
            return False, f"Empresa '{nome_empresa}' não encontrada."
        idempresa = empresa_info[0]
    except Exception as e:
        conn.close()
        return False, f"Erro ao buscar o ID da empresa: {e}"

    try:
        cursor.execute("""
            INSERT INTO contrato (id_utilizador, idempresa)
            VALUES (?, ?)
        """, (id_utilizador, idempresa))
        conn.commit()
    except Exception as e:
        conn.close()
        return False, f"Erro ao adicionar o contrato: {e}"

    conn.close()
    return True, "Utilizador e contrato adicionados com sucesso!"
#Validar se o email tem os caracteres caracteristicos
def validar_email(email):
    # Verificar se o email contém pelo menos um '@' e pelo menos um '.'
    if '@' in email and '.' in email:
        return True
    else:
        return False
#Função para gerar uma string aleatória de 20 caracteres (sal)
def gerar_sal():
    caracteres = string.ascii_letters + string.digits
    sal = ''.join(random.choice(caracteres) for i in range(20))
    return sal
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
    # Codificar a palavra em bytes
    password_bytes = password.encode('utf-8')

    # Criar um objeto de hash SHA-256
    sha256 = hashlib.sha256()

    # Atualizar o objeto de hash com os bytes da palavra
    sha256.update(password_bytes)

    # Gerar o hash da palavra
    hash_password = sha256.hexdigest()

    return hash_password
#Função para validar senha no login
def validar_password(idutilizador, input_password):
    # Conectar base de dados
    conn = conectar_db()
    cursor = conn.cursor()

    # Obter sal e senha criptografada da base de dados
    cursor.execute("SELECT sal, password FROM utilizador WHERE id_utilizador = ?", (idutilizador,))
    sal, stored_password = cursor.fetchone()
    # Criptografar senha de input com sal
    input_password_criptografada = criptografar_password(sal + input_password)
    conn.close()
    return input_password_criptografada == stored_password  
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
    # Conectar à base de dados
    conn = conectar_db()
    cursor = conn.cursor()

    try:
        # Gerar ID automático para a nova exploração
        idexploracao = preencher_id_automaticamente('exploracao')
        # Inserir a exploração
        cursor.execute("INSERT INTO exploracao (idexploracao, nome, idempresa) VALUES (?, ?, ?)", (idexploracao, nome_exploracao, idempresa))
        conn.commit()
        print("Exploração adicionada com sucesso.")
        return idexploracao  # Retorna o ID da exploração para uso subsequente
    except Exception as e:
        print(f"Erro ao adicionar exploração: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()
# Adicionar fracoes e pontos a uma exploracao
def adicionar_fracoes_pontos(idexploracao, fracoes, pontos):
    # Conectar à base de dados
    conn = conectar_db()
    cursor = conn.cursor()

    try:
        conn.autocommit = False
        
        # Inserir pontos no mapa com IDs automáticos
        pontos_ids = {}
        for i, ponto in enumerate(pontos):
            idponto = preencher_id_automaticamente('pontomapa')
            cursor.execute("INSERT INTO pontomapa (idponto, latitude, longitude, vertice) VALUES (?, ?, ?, 1)", (idponto, ponto['latitude'], ponto['longitude']))
            pontos_ids[i] = idponto

        # Inserir frações e associar pontos
        for fra in fracoes:
            if len(fra['indices_pontos']) < 3:
                # Se uma fração tem menos de 3 pontos, não continuar com a inserção
                print(f"Erro: A fração '{fra['nome']}' deve ter pelo menos 3 pontos para formar um polígono.")
                conn.rollback()
                return False

            idfracao = preencher_id_automaticamente('fracao')
            cursor.execute("INSERT INTO fracao (idfracao, nome, descricao, idexploracao) VALUES (?, ?, ?, ?)", (idfracao, fra['nome'], fra['descricao'], idexploracao))
            
            # Associar pontos da fração
            for indice_ponto in fra['indices_pontos']:
                idponto = pontos_ids[indice_ponto]
                cursor.execute("INSERT INTO tem (idponto, idfracao) VALUES (?, ?)", (idponto, idfracao))
        
        conn.commit()
        print("Frações e pontos adicionados com sucesso.")
        return True
    except Exception as e:
        print(f"Erro ao adicionar frações e pontos: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
#Função altera 4 tabelas sensor, medida, ponto mapa, tem
def adicionar_sensor(nome_sensor, unidade, latitude, longitude, idfracao):
    conn = conectar_db()
    cursor = conn.cursor()

    try:
        conn.autocommit = False

        # Adicionar ponto no mapa com vertice padrão como zero
        idponto = preencher_id_automaticamente('pontomapa')
        cursor.execute("INSERT INTO pontomapa (idponto, latitude, longitude, vertice) VALUES (?, ?, ?, 0)", (idponto, latitude, longitude))

        # Adicionar sensor associado a esse ponto
        idsensor = preencher_id_automaticamente('sensor')
        cursor.execute("INSERT INTO sensor (idsensor, nome, unidade, idponto) VALUES (?, ?, ?, ?)", (idsensor, nome_sensor, unidade, idponto))

        # Associar o ponto de mapa à fração na tabela 'tem'
        cursor.execute("INSERT INTO tem (idponto, idfracao) VALUES (?, ?)", (idponto, idfracao))

        # Adicionar uma medida inicial com valor zero e data atual
        idmedida = preencher_id_automaticamente('medida')
        data_atual = datetime.datetime.now().strftime('%Y-%m-%d')  # Formatação ISO da data
        cursor.execute("INSERT INTO medida (idmedida, data, valor, idsensor) VALUES (?, ?, ?, ?)", (idmedida, data_atual, 0, idsensor))

        conn.commit()
        print("Sensor adicionado com sucesso com dados de medida zero, data atual e associado à fração.")
        return True
    except Exception as e:
        print(f"Erro ao adicionar o sensor: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
#Função que atualiza o valor do sensor e a data
def atualizar_medida_sensor(idsensor, novo_valor):
    conn = conectar_db()
    cursor = conn.cursor()

    try:
        # Obter o ID da medida mais recente para o sensor especificado
        cursor.execute("SELECT idmedida FROM medida WHERE idsensor = ? ORDER BY data DESC LIMIT 1", (idsensor,))
        resultado = cursor.fetchone()
        if not resultado:
            print("Nenhuma medida encontrada para o sensor especificado.")
            return False

        idmedida = resultado[0]
        data_atual = datetime.datetime.now().strftime('%Y-%m-%d')  # Formatação ISO da data atual

        # Atualizar a medida com o novo valor e data atual
        cursor.execute("UPDATE medida SET valor = ?, data = ? WHERE idmedida = ?", (novo_valor, data_atual, idmedida))
        conn.commit()
        print("Medida do sensor atualizada com sucesso.")
        return True
    except Exception as e:
        print(f"Erro ao atualizar a medida do sensor: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
#Funcao para criar tabela relatorio
def criar_relatorio(nome, descricao, imagem, idfracao, nome_estado):
    conn = conectar_db()
    cursor = conn.cursor()

    try:
        conn.autocommit = False

        # Adicionar o relatório
        idrelatorio = preencher_id_automaticamente('registorelatorio')
        cursor.execute("INSERT INTO registorelatorio (idrelatorio, nome, descricao, imagem, idfracao) VALUES (?, ?, ?, ?, ?)",
                       (idrelatorio, nome, descricao, imagem, idfracao))

        # Obter o ID do estado com base no nome fornecido
        cursor.execute("SELECT idestador FROM estado WHERE nome = ?", (nome_estado,))
        resultado = cursor.fetchone()
        if not resultado:
            print("Estado não encontrado.")
            conn.rollback()
            return False
        idestador = resultado[0]

        # Associar o relatório ao estado na tabela 'estar'
        cursor.execute("INSERT INTO estar (idrelatorio, idestador) VALUES (?, ?)", (idrelatorio, idestador))

        conn.commit()
        print("Relatório criado com sucesso e estado associado.")
        return True
    except Exception as e:
        print(f"Erro ao criar o relatório: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()  

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
#Introduzir valores numa tabela em que uma das colunas é a data e introduz automáticmente a data
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
