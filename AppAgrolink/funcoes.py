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
import sqlite3
import requests
from email_validator import validate_email, EmailNotValidError

from http import HTTPStatus

cert_path = 'agrolink.crt'

app = Flask(__name__)

# Constantes
SERVER = 'https://firepuma.isr.tecnico.ulisboa.pt'
PORT = '5000'

# Dados Sessão
auth_token = None
typeUser = -1
nomeEmpresa = ''




# send_file(io.BytesIO(dados_imagem), mimetype='image/jpeg')

################# Serviços #################

# retornar empresas existentes
def nome_empresas():

    r = requests.get(SERVER + ':' + PORT + '/empresas', verify=cert_path)
    
    return [str(item[0]) for item in r.json()]

#Funcoes Utilizador
#Adicionar tabela utilizador 
def adicionar_utilizador(dados_utilizador):

    r = requests.post(SERVER + ':' + PORT + '/inserirutilizador',json=dados_utilizador,verify=cert_path)

    if r.status_code == HTTPStatus.CREATED:
        return True, "Utilizador e contrato adicionados com sucesso!"
    else:
        return False, "Email ou Nº Funcionário já existente!"

#Funcao de login
def login(dados_utilizador):

    r = requests.post(SERVER + ':' + PORT + '/login',json=dados_utilizador, verify=cert_path)
    print("HTTP resultado:" + str(r.status_code))
    if r.status_code == HTTPStatus.OK:
        global auth_token
        global typeUser
        global nomeEmpresa

        auth_token = {'token': r.json()['token']}
        typeUser = r.json()['type']
        nomeEmpresa = dados_utilizador['nome_empresa']

        print("Acabei de fazer login")
        print(typeUser) 

        return True, r.json()['type']
    else:
        return False, "Falha Login!"
    
# Serviço para retornar lista de utilizadores por validar
def utilizadores_verificar():
    print("Vamos validar")
    print(typeUser)
    print(auth_token)

    r = requests.get(SERVER + ':' + PORT + '/utilizadoresvalidar',params=auth_token,verify=cert_path)
    
    print(" Server DEVOLVEU ISTO")
    print(r.json())

    if r.status_code == HTTPStatus.OK:
        return True, r.json()['records']
    else:
        return False, r.json()

# Serviço para autorizar utilizadores
def autorizarutilizadores(lista):
    global auth_token
    r = requests.post(SERVER + ':' + PORT + '/autorizarutilizadores',json={'lista':lista},params=auth_token,verify=cert_path)

    if r.status_code == HTTPStatus.OK:
        auth_token = {'token': r.json()['token']}
        return True, "Utilizadores autorizados!"
    else:
        return False, "Erro na autorização!"

# Serviço para chamar os pontos    
def listapontos():
    pontos = [
        {'latitude': 40.2056246776543, 'longitude': -8.452967617140807},
        {'latitude': 40.20599275016009, 'longitude': -8.452816137126316},
        {'latitude': 40.205842122921936, 'longitude': -8.451877600410231},
        {'latitude': 40.20554789776591, 'longitude': -8.45205465355142},
        {'latitude': 40.208533928548924, 'longitude': -8.452068378147759},
        {'latitude': 40.20815954269777, 'longitude': -8.45066852981359}
    ]
    
    return json.dumps(pontos)


# Serviço para chamar os pontos    
def listasensores():
    dadossensor = [
        {'nome': 'Sensor de Temperatura','valor': 20, 'unidade': '°C'}]
    
    return json.dumps(dadossensor)

#Adicionar tabela empresa s
def adicionar_empresa(dados_empresa):

    r = requests.post(SERVER + ':' + PORT + '/inserirempresa',json=dados_empresa,params=auth_token,verify=cert_path)

    if r.status_code == HTTPStatus.CREATED:
        return True, "Empresa adicionada com sucesso!"
    else:
        return False, "Erro ao adicionar Empresa"


################# Funções Auxiliares #################

#Validar se o email tem os caracteres caracteristicos
def validar_email(email):
    try:
      # validate and get info
        v = validate_email(email) 
        # replace with normalized form
        email = v["email"]  
        return True
    except EmailNotValidError as e:
        return False
    




if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')