
# importação das bibliotecas
import math
import pyautogui
import pandas as pd
import time

# esperas para não dar erros
pyautogui.PAUSE = 1


def converter_valor(valor):

    if pd.isna(valor):
        return float("nan")

    return float(
        str(valor)
        .replace("R$", "")
        .replace(" ", "")
        .replace(",", ".")
    )


time.sleep(5)

# lendo as planilhas
planilha_canhoto = pd.read_excel("planilha_canhotos.xlsx")
planilha_produtos = pd.read_excel("planilha_produtos.xlsx")

# dados dos canhotos
metodo_de_pagamento = planilha_canhoto["METODO DE PAGAMENTO"]
codigo_canhoto = planilha_canhoto["CODIGO"]
valor_canhoto = planilha_canhoto["VALOR"]

# dados dos produtos
preco_produto = planilha_produtos["VALOR PRODUTO"]
codigo_produto = planilha_produtos["CODIGO DO PRODUTO"]

# cadastro dos canhotos
for i in range(len(planilha_canhoto)):

    # ignora linhas sem valor
    if pd.isna(valor_canhoto[i]):
        print(f"Linha {i + 1}: valor vazio")
        continue

    valor = converter_valor(valor_canhoto[i])

    metodo = str(
        metodo_de_pagamento[i]
    ).strip().upper()

    # corrige PX -> PIX
    if metodo == "PX":
        metodo = "PIX"

    # código só é necessário para débito e crédito
    codigo = ""

    if metodo in ["DEBITO", "CREDITO"]:

        if pd.notna(codigo_canhoto[i]):
            codigo = str(
                int(float(codigo_canhoto[i]))
            )
        else:
            print(
                f"Linha {i + 1}: código vazio para {metodo}"
            )
            continue

    produto_escolhido = None
    quantidade_escolhida = 1
    menor_diferenca = float("inf")

    # =====================================================
    # PASSO 1: procurar produto único acima do valor
    # =====================================================

    for j in range(len(planilha_produtos)):

        if pd.isna(preco_produto[j]):
            continue

        preco = converter_valor(
            preco_produto[j]
        )

        if pd.isna(preco):
            continue

        if preco >= valor:

            diferenca = preco - valor

            if diferenca < menor_diferenca:

                menor_diferenca = diferenca
                produto_escolhido = j
                quantidade_escolhida = 1

    # =====================================================
    # PASSO 2: se não encontrou, usa o produto mais caro
    # =====================================================

    if produto_escolhido is None:

        maior_preco = 0

        for j in range(len(planilha_produtos)):

            if pd.isna(preco_produto[j]):
                continue

            preco = converter_valor(
                preco_produto[j]
            )

            if pd.isna(preco):
                continue

            if preco > maior_preco:

                maior_preco = preco
                produto_escolhido = j

        if (
            produto_escolhido is not None
            and maior_preco > 0
        ):
            quantidade_escolhida = math.ceil(
                valor / maior_preco
            )

    # =====================================================
    # LANÇAMENTO
    # =====================================================

    if produto_escolhido is not None:

        preco = converter_valor(
            preco_produto[produto_escolhido]
        )

        codigo_prod = str(
            codigo_produto[produto_escolhido]
        )

        total_produtos = (
            quantidade_escolhida * preco
        )

        diferenca = round(
            total_produtos - valor,
            2
        )

        diferenca_formatada = (
            f"{diferenca:.2f}"
            .replace(".", ",")
        )

        texto = (
            f"{quantidade_escolhida}"
            f"*{codigo_prod}"
        )

        # lança o produto
        pyautogui.click(
            x=44,
            y=79
        )

        pyautogui.write(texto)
        pyautogui.press("enter")

        # abre tela de pagamento
        pyautogui.press("f10")
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("tab")

        # escreve a diferença
        pyautogui.write(
            diferenca_formatada
        )

        pyautogui.press("tab")

        # PIX
        if metodo == "PIX":

            pyautogui.write("4")
            pyautogui.press("enter")
            pyautogui.press("enter")

            time.sleep(3)

            pyautogui.click(
                x=694,
                y=437
            )

            time.sleep(3)

        # CRÉDITO
        elif metodo == "CREDITO":

            pyautogui.write("2")
            pyautogui.press("enter")

            time.sleep(3)

            pyautogui.click(
                x=673,
                y=354
            )

            pyautogui.write(codigo)

            pyautogui.click(
                x=640,
                y=388
            )

            time.sleep(3)

            pyautogui.click(
                x=696,
                y=437
            )

            time.sleep(3)

        # DÉBITO
        elif metodo == "DEBITO":

            pyautogui.write("3")
            pyautogui.press("enter")

            time.sleep(3)

            pyautogui.click(
                x=673,
                y=354
            )

            pyautogui.write(codigo)

            pyautogui.click(
                x=640,
                y=388
            )

            time.sleep(3)

            pyautogui.click(
                x=696,
                y=437
            )

            time.sleep(3)

        else:

            print(
                f"Linha {i + 1}: método "
                f"não reconhecido ({metodo})"
            )

    else:

        print(
            f"Nenhum produto encontrado "
            f"para o canhoto de "
            f"R$ {valor:.2f}"
        )

print("Processamento finalizado!")
