INSERT INTO tipoutilizador(idtipoutilizador, descricao, permissoes)
VALUES (0, 'Utilizador com as funções básicas do sistema. Normalmente trabalhadores comuns ou acessos de utilizadores pontuais ao sistema.' , 'Permissão para ver o mapa da exploração, tarefas, relatórios. Condicionado à alteração de informação da base de dados.');

INSERT INTO tipoutilizador(idtipoutilizador, descricao, permissoes)
VALUES (1, 'Utilizador com as funções avançadas do sistema. Poderá ser o dono da exploração ou trabalhadores da àrea informática.' , 'Permissão para realizar todas as funções do sistema. AAssim como realizar a alteração de informação da base de dados.');

INSERT INTO estadorelatorio(idestador, nome)
VALUES (1,'Em realização');

INSERT INTO estadorelatorio(idestador, nome)
VALUES (0,'Concluído');


INSERT INTO estadotarefa(idestadot, nome)
VALUES (0,'Em realização');


INSERT INTO estadotarefa(idestadot, nome)
VALUES (1,'Concluído');

DELETE FROM estadotarefa;
DELETE FROM estadorelatorio;
DELETE FROM tipoutilizador;


SELECT * FROM estadotarefa;
SELECT * FROM estadorelatorio;
SELECT * FROM tipoutilizador;
