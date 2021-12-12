import requests as r
import re
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def print_bold(text):
    print("\033[1m" + text + "\033[0;0m")

def print_green(text):
    print("\033[92m" + text + "\033[0;0m")

def print_red(text):
    print("\033[91m" + text + "\033[0;0m")

def ler_cartas():
    with open("cartas", "r") as f:
        linhas = f.readlines()
        return set([" ".join(linha.split()[1:]) for linha in linhas])

def vendedoras_da_carta(carta):
    lojas = set()
    res = r.get(f"https://www.ligamagic.com.br/?view=cards/card&card={quote_plus(carta)}")
    print("Analisando", carta)
    soup = BeautifulSoup(res.content, 'lxml')
    lojas_linhas = soup.find_all("div", {"class": "estoque-linha ecom-marketplace ecom-aval-on"})
    for linha in lojas_linhas:
        for loja in linha.find_all("div", {"class": "e-col1"}):
            nome_loja = re.findall(r'title="(.*)"\/>', str(loja))[0]
            lojas.add(nome_loja)
    return lojas

def criar_lojas_dict(cartas):
    lojas = {}
    for carta in cartas:
        for loja in vendedoras_da_carta(carta):
            if loja in lojas:
                lojas[loja].add(carta)
            else:
                lojas[loja] = {carta}
    return lojas

def mostrar_lojas_full(lojas, cartas):
    print()
    print_bold("========== LOJAS QUE VENDEM TODAS CARTAS ==========")
    for loja in lojas:
        if len(lojas[loja]) == len(cartas):
            print(loja)

def ver_loja_especifica(lojas, loja, cartas):
    s = f"\n========== {loja.upper()} ==========\n"
    print_bold(s)
    print_green("Cards vendidos:\n")
    for carta in lojas[loja]:
        print(carta)
    print_red("\nCards faltantes:\n")
    for carta in cartas - lojas[loja]:
        print(carta)
    print("\n"+len(s)*"="+"\n")


if __name__ == "__main__":
    cartas = ler_cartas()
    lojas = criar_lojas_dict(cartas)
    mostrar_lojas_full(lojas, cartas)
    print()
    print("Digite lista para ver o nome de todas as lojas")
    print("Aperte ENTER para sair")
    s = input("Digite o nome de loja para ver as cartas específicas: ")
    
    while s != "":
        if s == "lista":
            print()
            for loja in sorted(list(lojas.keys())):
                print(loja)
            print()
        else:
            if s in lojas:
                ver_loja_especifica(lojas, s, set(cartas))
            else:
                print_red("\nLoja não encontrada\n")
        print("Digite lista para ver o nome de todas as lojas")
        print("Aperte ENTER para sair")
        s = input("Digite o nome de loja para ver as cartas específicas: ")