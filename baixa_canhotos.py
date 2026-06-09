#importação das blibliotecas
import pyautogui
import pandas as pd
import time

# esperas para não dar erros.
pyautogui.PAUSE = 0.3


time.sleep(5)
# lendo as planilhas de canhoto e produtos.
planilha_canhoto = pd.read_excel("planilha_canhotos.xlsx")
planilha_produtos = pd.read_excel("planilha_produtos.xlsx")

# pegando dados das planilhas de canhoto.
metodo_de_pagamento = planilha_canhoto["METODO DE PAGAMENTO"]
codigo_canhoto = planilha_canhoto["CODIGO"]
valor_canhoto = planilha_canhoto["VALOR"]

# pegando dados da planinlha de produtos.
preco_produto = planilha_produtos["VALOR PRODUTO"]
qtd_estoque = planilha_produtos["QUANTIDADE ESTOQUE"]
codigo_produto = planilha_produtos["CODIGO DO PRODUTO"]

# cadastro dos canhotos automatico.
for i in range(len(planilha_canhoto)):
    pyautogui.click(44, 79)

    valor = float(valor_canhoto[i])

    # percorrendo produtos no sistema.
    for j in range(len(planilha_produtos)):
        preco = float(preco_produto[j])
        codigo_prod = codigo_produto[j]

        if valor >= preco:
            quantidade_produtos_a_ser_adicionados = int(valor // preco)
            resto = valor % preco

            resto_inteiro = int(resto)

            if quantidade_produtos_a_ser_adicionados == 0:
                quantidade_produtos_a_ser_adicionados = 1
                pyautogui.write(f"{quantidade_produtos_a_ser_adicionados}*{codigo_prod}")
                pyautogui.press("enter")

            break

    # lendo os produtos disponveis para cadastro dos canhotos.
    metodo = str(metodo_de_pagamento[i]).upper()
    codigo = codigo_canhoto[i]

    if metodo in ["CREDITO", "DEBITO"]:
        print(codigo)