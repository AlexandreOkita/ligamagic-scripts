import requests as r
import re
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

with open("cartas", "r") as f:
    linhas = f.readlines()
    cartas = [quote_plus(" ".join(linha.split()[1:])) for linha in linhas]

lojas_intersec = set()

for carta in cartas:
    lojas = set()
    res = r.get(f"https://www.ligamagic.com.br/?view=cards/card&card={carta}")
    print("Analisando", carta)
    soup = BeautifulSoup(res.content, 'lxml')
    lojas_linhas = soup.find_all("div", {"class": "estoque-linha ecom-marketplace ecom-aval-on"})
    for linha in lojas_linhas:
        for loja in linha.find_all("div", {"class": "e-col1"}):
            nome_loja = re.findall(r'title="(.*)"\/>', str(loja))[0]
            lojas.add(nome_loja)
    lojas_intersec = lojas if lojas_intersec == set() else lojas_intersec.intersection(lojas)
print()
print(lojas_intersec)