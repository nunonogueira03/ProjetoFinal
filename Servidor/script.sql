use projetofinal

drop table if exists estar;
drop table if exists estadorelatorio;
drop table if exists fornece;
drop table if exists registorelatorio;
drop table if exists medida;
drop table if exists sensor;
drop table if exists tem;
drop table if exists pontomapa;
drop table if exists fracao;
drop table if exists exploracao;
drop table if exists contrato;
drop table if exists utilizador;
drop table if exists tipoutilizador;
drop table if exists empresa;
drop table if exists estat;
drop table if exists estadotarefa;
drop table if exists usada;
drop table if exists ferramenta;
drop table if exists tarefa;

CREATE TABLE empresa
(
  idempresa INT NOT NULL,
  nome VARCHAR(50) NOT NULL,
  numerocontribuinte INT NOT NULL,
  morada VARCHAR(100) NOT NULL,
  contacto INT NOT NULL,
  PRIMARY KEY (idempresa)
);

CREATE TABLE tipoutilizador
(
  idtipoutilizador INT NOT NULL,
  descricao VARCHAR(500) NOT NULL,
  PRIMARY KEY (idtipoutilizador)
);

CREATE TABLE pontomapa
(
  idponto INT NOT NULL,
  latitude FLOAT NOT NULL,
  longitude FLOAT NOT NULL,
  vertice INT NOT NULL,
  PRIMARY KEY (idponto)
);

CREATE TABLE exploracao
(
  idexploracao INT NOT NULL,
  nome VARCHAR(100) NOT NULL,
  idempresa INT NOT NULL,
  PRIMARY KEY (idexploracao),
  FOREIGN KEY (idempresa) REFERENCES empresa(idempresa)
);

CREATE TABLE estadorelatorio
(
  idestador INT NOT NULL,
  nome VARCHAR(50) NOT NULL,
  PRIMARY KEY (idestador)
);

CREATE TABLE tarefa
(
  idtarefa INT NOT NULL,
  nome VARCHAR(100) NOT NULL,
  descricao VARCHAR(500) NOT NULL,
  PRIMARY KEY (idtarefa)
);

CREATE TABLE ferramenta
(
  idferramenta INT NOT NULL,
  nome VARCHAR(50) NOT NULL,
  quantidade INT NOT NULL,
  PRIMARY KEY (idferramenta)
);

CREATE TABLE sensor
(
  idsensor INT NOT NULL,
  nome VARCHAR(50) NOT NULL,
  unidade VARCHAR(50) NOT NULL,
  idponto INT NOT NULL,
  PRIMARY KEY (idsensor),
  FOREIGN KEY (idponto) REFERENCES pontomapa(idponto)
);

CREATE TABLE medida
(
  data DATE NOT NULL,
  valor FLOAT NOT NULL,
  idmedida INT NOT NULL,
  idsensor INT,
  PRIMARY KEY (idmedida),
  FOREIGN KEY (idsensor) REFERENCES sensor(idsensor)
);

CREATE TABLE estadotarefa
(
  nome VARCHAR(50) NOT NULL,
  idestadot INT NOT NULL,
  PRIMARY KEY (idestadot)
);

CREATE TABLE usada
(
  idferramenta INT NOT NULL,
  idtarefa INT NOT NULL,
  PRIMARY KEY (idferramenta, idtarefa),
  FOREIGN KEY (idferramenta) REFERENCES ferramenta(idferramenta),
  FOREIGN KEY (idtarefa) REFERENCES tarefa(idtarefa)
);

CREATE TABLE estat
(
  data DATE NOT NULL,
  idestadot INT NOT NULL,
  idtarefa INT NOT NULL,
  PRIMARY KEY (idestadot, idtarefa),
  FOREIGN KEY (idestadot) REFERENCES estadotarefa(idestadot),
  FOREIGN KEY (idtarefa) REFERENCES tarefa(idtarefa)
);

CREATE TABLE utilizador
(
  nome VARCHAR(100) NOT NULL,
  id_utilizador INT NOT NULL AUTO_INCREMENT,
  password VARCHAR(500) NOT NULL,
  numfuncionario INT NOT NULL,
  email VARCHAR(50) NOT NULL UNIQUE,
  sal VARCHAR(100) NOT NULL,
  idtipoutilizador INT NOT NULL,
  PRIMARY KEY (id_utilizador),
  FOREIGN KEY (idtipoutilizador) REFERENCES tipoutilizador(idtipoutilizador)
);

CREATE TABLE fracao
(
  idfracao INT NOT NULL,
  nome VARCHAR(100) NOT NULL,
  descricao VARCHAR(500) NOT NULL,
  idexploracao INT NOT NULL,
  PRIMARY KEY (idfracao),
  FOREIGN KEY (idexploracao) REFERENCES exploracao(idexploracao)
);

CREATE TABLE registorelatorio
(
  idrelatorio INT NOT NULL,
  nome VARCHAR(50) NOT NULL,
  descricao VARCHAR(500) NOT NULL,
  imagem VARCHAR(500) NOT NULL,
  idfracao INT,
  PRIMARY KEY (idrelatorio),
  FOREIGN KEY (idfracao) REFERENCES fracao(idfracao)
);

CREATE TABLE contrato
(
  id_utilizador INT NOT NULL,
  idempresa INT NOT NULL,
  PRIMARY KEY (id_utilizador, idempresa),
  FOREIGN KEY (id_utilizador) REFERENCES utilizador(id_utilizador),
  FOREIGN KEY (idempresa) REFERENCES empresa(idempresa)
);

CREATE TABLE tem
(
  idponto INT NOT NULL,
  idfracao INT NOT NULL,
  PRIMARY KEY (idponto, idfracao),
  FOREIGN KEY (idponto) REFERENCES pontomapa(idponto),
  FOREIGN KEY (idfracao) REFERENCES fracao(idfracao)
);

CREATE TABLE estar
(
  data DATE NOT NULL,
  idrelatorio INT NOT NULL,
  idestador INT NOT NULL,
  PRIMARY KEY (idrelatorio, idestador),
  FOREIGN KEY (idrelatorio) REFERENCES registorelatorio(idrelatorio),
  FOREIGN KEY (idestador) REFERENCES estadorelatorio(idestador)
);

CREATE TABLE fornece
(
  idrelatorio INT NOT NULL,
  idtarefa INT NOT NULL,
  PRIMARY KEY (idrelatorio, idtarefa),
  FOREIGN KEY (idrelatorio) REFERENCES registorelatorio(idrelatorio),
  FOREIGN KEY (idtarefa) REFERENCES tarefa(idtarefa)
);

insert into tipoutilizador(idtipoutilizador, descricao) values(1,'Admin');
insert into tipoutilizador(idtipoutilizador, descricao) values(2,'Admin Lvl2');
insert into tipoutilizador(idtipoutilizador, descricao) values(3,'Admin LVl2 Standby');
insert into tipoutilizador(idtipoutilizador, descricao) values(4,'Trabalhador');
insert into tipoutilizador(idtipoutilizador, descricao) values(5,'Trabalhador Standby');

insert into empresa(idempresa, nome, numerocontribuinte, morada, contacto) values (1, 'Sem Empresa', 0, 'Sem Morada', 0);
