INSERT INTO tipoutilizador(idtipoutilizador, descricao, permissoes)
VALUES (0, 'Utilizador com as fun��es b�sicas do sistema. Normalmente trabalhadores comuns ou acessos de utilizadores pontuais ao sistema.' , 'Permiss�o para ver o mapa da explora��o, tarefas, relat�rios. Condicionado � altera��o de informa��o da base de dados.');

INSERT INTO tipoutilizador(idtipoutilizador, descricao, permissoes)
VALUES (1, 'Utilizador com as fun��es avan�adas do sistema. Poder� ser o dono da explora��o ou trabalhadores da �rea inform�tica.' , 'Permiss�o para realizar todas as fun��es do sistema. AAssim como realizar a altera��o de informa��o da base de dados.');

INSERT INTO estadorelatorio(idestador, nome)
VALUES (1,'Em realiza��o');

INSERT INTO estadorelatorio(idestador, nome)
VALUES (0,'Conclu�do');


INSERT INTO estadotarefa(idestadot, nome)
VALUES (0,'Em realiza��o');


INSERT INTO estadotarefa(idestadot, nome)
VALUES (1,'Conclu�do');

DELETE FROM estadotarefa;
DELETE FROM estadorelatorio;
DELETE FROM tipoutilizador;


SELECT * FROM estadotarefa;
SELECT * FROM estadorelatorio;
SELECT * FROM tipoutilizador;
