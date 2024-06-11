# app.py
from flask import Flask, request, jsonify, make_response
import json
import mysql.connector as mysql
import hashlib
import random
import string
import jwt
import datetime

# HTTP codes
from http import HTTPStatus

# Constants in the code
SALT_SIZE = 20
JWT_SECRET_SIZE = 20

# Tipos de Utilizador
ADMIN = 1
ADMINCOMPANY = 2
ADMINSTANDBY = 3
WORKER = 4
WORKERSTANDBY = 5

app = Flask(__name__)

app.config['secret_key'] = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(JWT_SECRET_SIZE))

mydb = mysql.connect(
    host='localhost',
    user='agrolink',
    password='agrolink!%secure',
    database='projetofinal',
)

mycursor = mydb.cursor()


# Funcoes de validacao
def gerar_sal():
    # Gera uma string aleatória de SALT_SIZE caracteres
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(SALT_SIZE))


# Adiciona o sal a password introduzida e codifica
def criptografar_password(password):
    # Criptografa uma senha usando SHA-256.
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()


def token_required(f):
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'error': 'token is missing'}), HTTPStatus.FORBIDDEN
        try:
            jwt.decode(token, app.config['secret_key'], algorithms="HS256")
        except Exception as error:
            return jsonify({'error': 'token is invalid/expired'}), HTTPStatus.UNAUTHORIZED
        return f(*args, **kwargs)

    decorated.__name__ = f.__name__
    return decorated


def renew_token(session):
    session['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

    return jwt.encode(session, app.config['secret_key'])


# SERVICES
@app.get("/access")
@token_required
def access():
    return jsonify({'message': 'valid jwt token'})


@app.get("/empresas")
def get_empresas():
    sql = "SELECT nome FROM empresa"
    mycursor.execute(sql)

    records = mycursor.fetchall()

    mydb.commit()

    return json.dumps(records)


@app.get("/utilizadores")
def get_utilizadores():
    sql = "SELECT * FROM utilizador"
    mycursor.execute(sql)

    records = mycursor.fetchall()

    mydb.commit()

    return jsonify(records)


@app.post("/login")
def login():
    password = request.json['password']
    email = request.json['email']
    empresa = request.json['nome_empresa']

    mycursor.execute("SELECT sal, password FROM utilizador WHERE email = %s AND idtipoutilizador = 1", (email,))
    row = mycursor.fetchone()

    mydb.commit()

    if row is None:
        return {}, HTTPStatus.UNAUTHORIZED

    passwordDB = row[1]
    sal = row[0]

    encrypted_password = criptografar_password(sal + password)

    prazo = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

    token = jwt.encode({'user': email, 'exp': prazo, 'type': 1, 'empresa': empresa}, app.config['secret_key'])

    if encrypted_password == passwordDB:
        return {'token': token, "type": 1}, HTTPStatus.OK
    else:
        return {}, HTTPStatus.UNAUTHORIZED


@app.post("/inserirutilizador")
def inserirutilizador():
    password = request.json['password']
    nome = request.json['nome']
    numfuncionario = request.json['numfuncionario']
    email = request.json['email']
    empresa = request.json['nome_empresa']

    if empresa == "Sem Empresa":
        idtipoutilizador = ADMINSTANDBY
    else:
        idtipoutilizador = WORKERSTANDBY

    #Gerar um novo sal e encriptar a senha
    sal = gerar_sal()
    encrypted_password = criptografar_password(sal + password)

    try:
        sql = "INSERT INTO utilizador (nome, password, numfuncionario, email, sal, idtipoutilizador) values (%s, %s, %s, %s, %s, %s)"
        val = (nome, encrypted_password, numfuncionario, email, sal, idtipoutilizador)
        mycursor.execute(sql, val)
        mydb.commit()

    except mysql.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))
        return {}, HTTPStatus.CONFLICT
    return {}, HTTPStatus.CREATED


@app.get("/utilizadoresvalidar")
@token_required
def utilizadoresvalidar():
    session = jwt.decode(request.args.get('token'), app.config['secret_key'], algorithms="HS256")

    perfil = session['type']
    empresa = session['empresa']

    print("Dados VALIDAR")
    print(request.args.get('token'))
    print(f"perfil {perfil} e empresa {empresa}")

    if perfil not in (ADMIN, ADMINCOMPANY):
        return request.args.get('token'), HTTPStatus.FORBIDDEN

    sql = ""
    if perfil == ADMIN:
        sql = "SELECT email FROM utilizador WHERE idtipoutilizador = " + str(ADMINSTANDBY)
        print(sql)

    if perfil == ADMINCOMPANY:
        sql = ("SELECT email FROM utilizador INNER JOIN contrato ON utilizador.id_utilizador = contrato.id_utilizador "
               "INNER JOIN empresa ON contrato.idempresa = empresa.idempresa WHERE idtipoutilizador = ") + str(
            WORKERSTANDBY) + " AND empresa.nome = " + str(empresa)

    mycursor.execute(sql)
    results = [record[0] for record in mycursor.fetchall()]
    print(results)
    print(mycursor.rowcount)
    print({'records2': results, 'token': renew_token(session)})
    mydb.commit()
    return {'records': results, 'token': renew_token(session)}


@app.post("/autorizarutilizadores")
@token_required
def autorizarutilizadores():
    session = jwt.decode(request.args.get('token'), app.config['secret_key'], algorithms="HS256")

    perfil = session['type']
    empresa = session['empresa']

    print("Dados")
    print(request.args.get('token'))

    if perfil not in (ADMIN, ADMINCOMPANY):
        return request.args.get('token'), HTTPStatus.FORBIDDEN

    lista = request.json['lista']

    print("Dados")
    print(request.args.get('token'))

    sql = ""
    if perfil == ADMIN:
        sql = "UPDATE utilizador SET idtipoutilizador = " + str(ADMINCOMPANY) + " WHERE idtipoutilizador = " + str(
            ADMINSTANDBY) + " AND email in ('" + "','".join(lista) + "')"
        print(sql)

    if perfil == ADMINCOMPANY:
        sql = (("UPDATE utilizador as u"
                "INNER JOIN contrato as c"
                "ON u.id_utilizador = c.utilizador"
                "INNER JOIN empresa as e"
                "ON c.idempresa = e.idempresa"
                "SET u.idtipoutilizador = ") + str(WORKER)
               + " WHERE u.idtipoutilizador = " + str(WORKERSTANDBY)
               + " AND e.nome = " + empresa
               + " AND email in (" + ",".join(lista) + ")")

    mycursor.execute(sql)

    mydb.commit()

    return {'token': renew_token(session)}


############## Lixo ##################


@app.post("/inserir_empresa")
def add_empresa(nome, numerocontribuinte, morada, contacto):
    # Verifica se o número de contribuinte já existe
    if not validar_strings_de_uma_tabela(numerocontribuinte, 'empresa', 'numerocontribuinte'):
        return jsonify(False)

    # Verifica se o contacto já existe
    if not validar_strings_de_uma_tabela(contacto, 'empresa', 'contacto'):
        return jsonify(False)

    # Obter ID automático para a nova empresa
    idempresa = preencher_id_automaticamente('empresa')
    idempresa = preencher_id_automaticamente("empresa")

    # Preparar a consulta SQL para inserir os dados da empresa
    sql = "INSERT INTO empresa (idempresa, nome, numerocontribuinte, morada, contacto) VALUES (%s, %s, %s, %s, %s)"
    val = (idempresa, nome, numerocontribuinte, morada, contacto)

    # Executar a consulta
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        print("Empresa adicionada com sucesso!")
        return jsonify(True)
    except Exception as e:
        print(f"Erro ao adicionar a empresa: {e}")
        mydb.rollback()
        return jsonify(False)


@app.post("/inserir_exploracao")
def add_exploracao(nome_exploracao, idempresa):
    try:
        # Gerar ID automático para a nova exploração
        idexploracao = preencher_id_automaticamente('exploracao')
        # Inserir a exploração
        sql = "INSERT INTO exploracao (idexploracao, nome, idempresa) VALUES (%s, %s, %s)"
        val = (idexploracao, nome_exploracao, idempresa)
        mycursor.execute(sql, val)
        mydb.commit()

        return True
    except Exception as e:
        print(f"Erro ao adicionar exploração: {e}")
        mydb.rollback()
        return jsonify(False)


@app.post("/inserir_fracoes_pontos")
def add_fracoes_pontos(idexploracao, fracoes, pontos):
    try:
        # Inserir pontos no mapa com IDs automáticos
        pontos_ids = {}
        for i, ponto in enumerate(pontos):
            idponto = preencher_id_automaticamente('pontomapa')
            sql = "INSERT INTO pontomapa (idponto, latitude, longitude, vertice) VALUES (%s, %s, %s, %s)"
            val = (idponto, ponto['latitude'], ponto['longitude'], 1)
            mycursor.execute(sql, val)
            mydb.commit()
            pontos_ids[i] = idponto

        # Inserir frações e associar pontos
        for fra in fracoes:
            if len(fra['indices_pontos']) < 3:
                # Se uma fração tem menos de 3 pontos, não continuar com a inserção
                print(f"Erro: A fração '{fra['nome']}' deve ter pelo menos 3 pontos para formar um polígono.")
                mydb.rollback()
                return jsonify(False)

            idfracao = preencher_id_automaticamente('fracao')
            sql = "INSERT INTO fracao (idfracao, nome, descricao, idexploracao) VALUES (%s, %s, %s, %s)"
            val = (idfracao, fra['nome'], fra['descricao'], idexploracao)
            mycursor.execute(sql, val)
            mydb.commit()

            # Associar pontos da fração
            for indice_ponto in fra['indices_pontos']:
                idponto = pontos_ids[indice_ponto]
                sql = "INSERT INTO tem (idponto, idfracao) VALUES (%s, %s, %s, %s)"
                val = (idponto, idfracao)
                mycursor.execute(sql, val)
                mydb.commit()

        print("Frações e pontos adicionados com sucesso.")
        return jsonify(True)
    except Exception as e:
        print(f"Erro ao adicionar frações e pontos: {e}")
        mydb.rollback()
        return jsonify(False)


@app.post("/inserir_sensor")
def add_sensor(nome_sensor, unidade, latitude, longitude, idfracao):
    idponto = preencher_id_automaticamente('pontomapa')
    sql = "INSERT INTO pontomapa (idponto, latitude, longitude, vertice) VALUES (%s, %s, %s, %s)"
    val = (idponto, latitude, longitude, 1)
    mycursor.execute(sql, val)
    mydb.commit()

    # Adicionar ponto no mapa com vertice padrão como zero
    # Inserir pontos no mapa
    idsensor = preencher_id_automaticamente('sensor')
    sql = "INSERT INTO sensor (idsensor, nome, unidade, idponto) VALUES (%s, %s, %s, %s)"
    val = (idsensor, nome_sensor, unidade, 0)
    mycursor.execute(sql, val)
    mydb.commit()

    sql = "INSERT INTO tem (idponto, idfracao) VALUES (%s, %s, %s, %s)"
    val = (idponto, idfracao)
    mycursor.execute(sql, val)
    mydb.commit()

    jsonify(True)


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
