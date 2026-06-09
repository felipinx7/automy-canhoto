#importação das blibliotecas
import pyautogui
import pandas as pd
import time

planilha_canhoto = pd.read_excel("Pasta1.xlsx")
metodo_de_pagamento = planilha_canhoto["METODO DE PAGAMENTO"]
codigo_canhoto = planilha_canhoto["CODIGO"]

for i in range(len(planilha_canhoto)):
    metodo = str(metodo_de_pagamento[i]).upper()
    codigo = codigo_canhoto[i]

    if metodo in ["CREDITO", "DEBITO"]:
        print(codigo)

# #lógica da automação.
# pyautogui.press("win")
# time.sleep(2)

# pyautogui.write("chrome")
# pyautogui.press("enter")