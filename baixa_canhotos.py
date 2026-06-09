#importação das blibliotecas
import pyautogui
import pandas as pd
import time

# lendo as planilhas de canhoto e produtos.
planilha_canhoto = pd.read_excel("planilha_canhotos.xlsx")
planilha_produtos = pd.read_excel("planilha_produtos.xlsx")

# pegando dados das planilhas de canhoto.
metodo_de_pagamento = planilha_canhoto["METODO DE PAGAMENTO"]
codigo_canhoto = planilha_canhoto["CODIGO"]
valor_canhoto = planilha_canhoto["VALOR"]

# pegando dados da planinlha de produtos.
preco_produto = planilha_produtos["VALOR PRODUTO"]
qtd_estoque = planilha_produtos["QUANTIDADE ESTOUQE"]


# cadastro dos canhotos automatico.
for i in range(len(planilha_canhoto)):
    pyautogui.press("f1");

    # lendo os produtos disponveis para cadastro dos canhotos.
    metodo = str(metodo_de_pagamento[i]).upper()
    codigo = codigo_canhoto[i]

    if metodo in ["CREDITO", "DEBITO"]:
        print(codigo)
