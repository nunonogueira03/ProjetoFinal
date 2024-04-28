from funcoes import *

def main():
    #escrever_na_tabela("empresa",786,"teste3")
    #escreverdb()
    #tabela_sem_data("sensor",preencher_id_automaticamente("sensor"),"humidade","mm3")
    #tabela_com_data("registorelatorio",preencher_id_automaticamente("registorelatorio"),"humidade","dois","tres")
    #possui_data_na_tabela("registorelatorio")
    #possui_data_na_tabela("registorelatorio")

    palavra = input("Digite a palavra a ser criptografada: ")
    hash_password = criptografar_password(palavra)
    print("Palavra criptografada:", hash_password)

    #email = input("Digite o email: ")
    #if validar_email(email):
    #    print("Email válido!")
    #else:
    #    print("Email inválido!")

    #valor = input("Digite o valor a ser validado: ")
    #tabela = "sensor"
    #coluna = "idsensor"
    #if validar_strings_de_uma_tabela(valor, tabela, coluna):
    #    print("O valor é diferente de todos os outros valores na coluna.")
    #else:
    #    print("O valor já existe na coluna.")

    #coluna_retorno = "unidade"
    #tabela = "sensor"
    #coluna_condicao = "idsensor"  # Coluna usada como condição
    #valor_condicao = input("Digite o valor da condição: ")
    #valor_retornado = ler_valor_db(coluna_retorno, tabela, coluna_condicao, valor_condicao)
    #print(f"O valor da coluna '{coluna_retorno}' correspondente ao '{coluna_condicao}' '{valor_condicao}' é: {valor_retornado}")

    # tabela = "sensor"
    # coluna = "unidade"  # Coluna que será alterada
    # novo_valor = "mm2"  # Novo valor para a coluna
    # condicao_coluna = "idsensor"  # Coluna usada como condição
    # condicao_valor = 1  # Valor da condição
    # alterar_valor_db(tabela, coluna, novo_valor, condicao_coluna, condicao_valor)
    # print(f"O valor da coluna '{coluna}' na linha com '{condicao_coluna}' igual a '{condicao_valor}' foi alterado para '{novo_valor}'.")

    #tabela_sem_data("empresa",preencher_id_automaticamente("empresa"),"EmpresaTeste")
    #tabela_sem_data("pontomapa",preencher_id_automaticamente("pontomapa"),9839281,-123334,True)
    #tabela_sem_data("pontomapa",preencher_id_automaticamente("pontomapa"),4365464,-95096,1)
    #tabela_com_data("registorelatorio",preencher_id_automaticamente("registorelatorio"),"testenome","testedescricao","testeimagem")
    #tabela_sem_data("fracao",preencher_id_automaticamente("fracao"),"testenome","testedescricao",2,1)
    #tabela_sem_data("exploracao",preencher_id_automaticamente("exploracao"),"testenome","testedescricao",2,1)
    #sao_iguais(2,2)

if __name__ == "__main__":
    main()