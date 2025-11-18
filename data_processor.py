# data_processor.py

import pandas as pd
import pandas.api.types as ptypes
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker 


def _iniciar_carregamento(grafico_frame):
    for widget in grafico_frame.winfo_children():
        widget.destroy()

    loading_container = ttk.Frame(grafico_frame)
    loading_container.pack(expand=True, padx=20, pady=20) 

    loading_label = ttk.Label(loading_container, text="⏳ Gerando Gráfico... Processando Dados...", font=('Arial', 12, 'bold'))
    loading_label.pack(pady=10)
    
    spinner = ttk.Progressbar(loading_container, mode='indeterminate', length=200)
    spinner.pack(pady=10)
    spinner.start()

    grafico_frame.update() 
    
    return loading_container

def _finalizar_carregamento(loading_container):
    if loading_container and loading_container.winfo_exists():
        for widget in loading_container.winfo_children():
            if isinstance(widget, ttk.Progressbar):
                widget.stop()
        loading_container.destroy()


def limpar_e_converter_colunas(df, colunas):
    df_temp = df.copy()
    colunas_numericas_validas = []
    
    for col in colunas:
        if df_temp[col].astype(str).str.strip().eq('').all():
            continue
            
        limpo = df_temp[col].astype(str).str.replace(r'[R$%\s]', '', regex=True)
        limpo = limpo.str.replace(',', '.', regex=False)
        
        df_temp[col] = pd.to_numeric(limpo, errors='coerce')
        
        if not df_temp[col].isna().all():
            colunas_numericas_validas.append(col)
        
    return df_temp, colunas_numericas_validas


def analisar_tipos_colunas(df):

    coluna_tipos = {}
    
    df_temp, colunas_numericas = limpar_e_converter_colunas(df, df.columns.tolist())

    for col in df.columns:
        if col in colunas_numericas:
            data = df_temp[col].dropna()
            
            if data.empty:
                 coluna_tipos[col] = "Valor (Vazio)" 
                 continue
                 
            unique_count = data.nunique()
            total_count = len(data)
            
            if unique_count / total_count > 0.9 and total_count > 50:
                coluna_tipos[col] = "ID/Cód"
                continue
    
            max_val = data.max()
            mean_val = data.mean()

            if mean_val < 100 and max_val < 1000:
                 coluna_tipos[col] = "Quantidade"
            
            else:
                if max_val < 5000 and mean_val < 500:
                    coluna_tipos[col] = "Monetário Unitário" 
                else:
                    coluna_tipos[col] = "Monetário Total" 
                
        else:
            coluna_tipos[col] = "Categoria" 

    return coluna_tipos


def gerar_grafico_matplotlib(df_calculo, colunas_numericas_validas, operacao, colunas_selecionadas, grafico_frame):
    
    try:
        y_col = 'Resultado_Operacao'
        x_col_plot = None 

        non_numeric_selected_cols = [
            col for col in colunas_selecionadas 
            if col not in colunas_numericas_validas 
        ]
        
        x_col_grouping = non_numeric_selected_cols[0] if non_numeric_selected_cols else None
        
        if x_col_grouping and x_col_grouping in df_calculo.columns and len(df_calculo[x_col_grouping].unique()) < 50: 
            df_agrupado = df_calculo.fillna({x_col_grouping: 'Desconhecido'}).groupby(x_col_grouping)[y_col].sum().reset_index()
            x_col_plot = x_col_grouping
            title = f"Total da {operacao.upper()} por {x_col_grouping}"
            
        elif len(colunas_numericas_validas) > 1:
            data = {
                'Coluna': colunas_numericas_validas,
                y_col: [df_calculo[col].sum() for col in colunas_numericas_validas]
            }
            df_agrupado = pd.DataFrame(data)
            x_col_plot = 'Coluna'
            title = f"Comparação de Totais das Colunas ({operacao.upper()})"
            
        else:
            df_agrupado = pd.DataFrame({
                'Total Geral': ['Total'],
                y_col: [df_calculo[y_col].sum()]
            })
            x_col_plot = 'Total Geral'
            title = f"Resultado Global da {operacao.upper()}"


        fig, ax = plt.subplots(figsize=(6, 5)) 

        ax.bar(df_agrupado[x_col_plot], df_agrupado[y_col], color='teal')
        
        ax.set_title(title, fontsize=12)
        ax.set_xlabel(x_col_plot, fontsize=10)
        ax.set_ylabel(f"Resultado ({operacao.upper()})", fontsize=10)
        
        # Função para formatar o valor monetário em R$
        def formatar_moeda(valor):
            return f"R$ {valor:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')

        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.yticks(fontsize=8)
        
        for index, row in df_agrupado.iterrows():
            ax.text(index, row[y_col], formatar_moeda(row[y_col]), ha='center', va='bottom', fontsize=7)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=grafico_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()
        
    except Exception as e:
        ttk.Label(grafico_frame, text=f"❌ Erro ao gerar gráfico: {e}", foreground='red').pack(padx=10, pady=10)
        messagebox.showerror("Erro ao Gerar Gráfico", f"Não foi possível gerar o gráfico. Erro: {e}")


def processar_dados(df, colunas_para_calcular, operacao, grafico_frame, colunas_selecionadas):
    
    loading_container = None
    
    try:
        loading_container = _iniciar_carregamento(grafico_frame)
        
        df_temp, colunas_numericas_validas = limpar_e_converter_colunas(df, colunas_para_calcular)
        
        if not colunas_numericas_validas:
            _finalizar_carregamento(loading_container)
            messagebox.showwarning("Aviso", "Nenhuma coluna numérica válida foi selecionada para o cálculo.")
            return

        df_calculo = df_temp.dropna(subset=colunas_numericas_validas)
        
        if operacao == 'soma':
            df_calculo['Resultado_Operacao'] = df_calculo[colunas_numericas_validas].sum(axis=1)
            resultado_final = df_calculo['Resultado_Operacao'].sum()
            texto_op = "Soma Total (de todas as colunas somadas):"
            
        elif operacao == 'multiplicacao':
            df_calculo['Resultado_Operacao'] = df_calculo[colunas_numericas_validas].prod(axis=1)
            resultado_final = df_calculo['Resultado_Operacao'].sum() 
            texto_op = "Soma do Produto Total (Faturamento GERAL):"
            
        else:
            return
        
        resultado_formatado = f"R$ {resultado_final:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

        messagebox.showinfo(
            "Resultado do Cálculo", 
            f"Operação: {operacao.upper()} nas colunas: {', '.join(colunas_numericas_validas)}\n"
            f"Calculado a partir de {len(df_calculo)} linhas válidas.\n"
            f"💰 {texto_op} {resultado_formatado}"
        )
        
        _finalizar_carregamento(loading_container) 
        gerar_grafico_matplotlib(df_calculo, colunas_numericas_validas, operacao, colunas_selecionadas, grafico_frame)

    except Exception as e:
        messagebox.showerror("Erro de Processamento", f"Ocorreu um erro durante o processamento de dados: {e}")
        _finalizar_carregamento(loading_container)
        ttk.Label(grafico_frame, text=f"❌ Erro: {e}", foreground='red').pack(padx=10, pady=10)
        
def analise_descritiva(df, colunas_para_analisar):
    if not colunas_para_analisar:
        messagebox.showwarning("Aviso", "Selecione pelo menos uma coluna para a análise.")
        return
    
    if df.empty:
        messagebox.showwarning("Aviso", "Nenhum dado carregado.")
        return

    resultado_texto = ["--- ANÁLISE DESCRITIVA DAS COLUNAS ---"]

    for col in colunas_para_analisar:
        df_temp, _ = limpar_e_converter_colunas(df, [col])
        coluna_limpa = df_temp[col]

        if ptypes.is_numeric_dtype(coluna_limpa):
            count = coluna_limpa.count() 
            if count > 0:
                soma = coluna_limpa.sum()
                media = coluna_limpa.mean()
                
                soma_f = f"R$ {soma:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                media_f = f"R$ {media:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

                resultado_texto.append(
                    f"\nColuna: {col} (Numérica)\n"
                    f"  Total de Itens: {count:,}\n"
                    f"  Soma Total: {soma_f}\n"
                    f"  Média: {media_f}"
                )
            else:
                 resultado_texto.append(f"\nColuna: {col} (Numérica)\n  Sem dados válidos para cálculo.")
        else:
            unique_count = coluna_limpa.nunique()
            total_count = coluna_limpa.count()
            top_value = coluna_limpa.mode().iloc[0] if not coluna_limpa.mode().empty else "N/A"
            
            resultado_texto.append(
                f"\nColuna: {col} (Categórica/Texto)\n"
                f"  Total de Registros: {total_count:,}\n"
                f"  Quantidade de Valores Únicos (Produtos, IDs, etc): {unique_count:,}\n"
                f"  Valor Mais Comum: {top_value}"
            )
    
    messagebox.showinfo("Análise Descritiva", "\n".join(resultado_texto))