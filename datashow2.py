import os
import pandas as pd
import plotly.express as px

caminho_pasta = input("Digite o caminho da pasta com os arquivos: ").strip()

caminho_pasta = os.path.normpath(caminho_pasta)
lista_arquivos = os.listdir(caminho_pasta)
tabela_total = pd.DataFrame()

for arquivo in lista_arquivos:
    caminho_completo = os.path.join(caminho_pasta, arquivo)
    
    try:
        if arquivo.endswith('.csv'):
            df = pd.read_csv(caminho_completo)
        elif arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
            df = pd.read_excel(caminho_completo)
        elif arquivo.endswith('.json'):
            df = pd.read_json(caminho_completo)
        elif arquivo.endswith('.html'):
            df = pd.read_html(caminho_completo)[0]
        else:
            print(f"Ignorado (formato não suportado): {arquivo}")
            continue
        print(f"\nArquivo lido com sucesso: {arquivo}")
        print(df.head())

    except Exception as erro:
        print(f"Erro ao ler {arquivo}: {erro}")
        tabela_total =  pd.concat(tabela_total,df)
print(tabela_total)

