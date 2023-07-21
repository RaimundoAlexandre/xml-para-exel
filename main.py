import xmltodict as xml
import os
import pandas as pd


def pegar_infos(nome_arquivo, valores):
    #print(f"Pegou as informações {nome_arquivo}")
    with open(f"nfs/{nome_arquivo}", "rb") as arquivo_xml:
        dic_arquivo = xml.parse(arquivo_xml)

        if "NFe" in dic_arquivo:
            infos_nf = dic_arquivo["NFe"]["infNFe"]
        else:
            infos_nf = dic_arquivo["nfeProc"]["NFe"]["infNFe"]

        numero_nota = infos_nf["@Id"]
        empre_emisora = infos_nf["emit"]["xNome"]
        nome_cliente = infos_nf["dest"]["xNome"]
        endereco = infos_nf["dest"]["enderDest"]

        if "vol" in infos_nf['transp']:
            peso = infos_nf["transp"]["vol"]["pesoB"]
        else:
            peso = 'Não informado'

        valores.append([numero_nota, empre_emisora, nome_cliente, endereco, peso])

list_arquivos = os.listdir('nfs')

colunas = ["numero_nota", "empre_emisora", "nome_cliente", "endereco", "peso"]
valores = []
for arquivo in list_arquivos:
    pegar_infos(arquivo, valores)

tabela = pd.DataFrame(columns=colunas, data=valores)
tabela.to_excel("Notas fiscais.xlsx", index=False)
