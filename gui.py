# gui.py

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import pandas as pd
import openIA
import data_processor


class AppGUI:
    def __init__(self, master):
        self.master = master
        master.title("📊 DataShow 2.0 - Análise de Dados GUI")
        master.geometry("1200x700")
        self.tabela_total = pd.DataFrame()
        self.colunas_disponiveis = []
        self.coluna_sugerida = None
        self.colunas_selecionadas_gui = {} 
        self.coluna_classificacao = {}
        self._setup_frames()
        self.atualizar_lista_colunas()


    def _setup_frames(self):
        # 0. CONFIGURAÇÃO DA API KEY
        api_frame = ttk.LabelFrame(self.master, text="0. Configuração da OpenAI API Key (Para Sugestão da IA)")
        api_frame.pack(padx=10, pady=10, fill='x')

        self.api_key_entry = ttk.Entry(api_frame, show="*", width=50) 
        self.api_key_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=(10, 5), pady=5)
        self.api_key_entry.insert(0, "Insira sua chave 'sk-...' aqui")

        api_button = ttk.Button(api_frame, text="✅ Configurar Chave", command=self._configurar_api_key_wrapper)
        api_button.pack(side=tk.LEFT, padx=(0, 10), pady=5)

        self.api_status_label = ttk.Label(api_frame, text="Status da API: ❓ Não configurada.", foreground="red")
        self.api_status_label.pack(pady=(0, 5))

        arquivos_frame = ttk.LabelFrame(self.master, text="1. Carregamento de Arquivos")
        arquivos_frame.pack(padx=10, pady=10, fill='x')

        select_button = ttk.Button(arquivos_frame, text="📂 Selecionar Arquivos de Tabela", command=self.selecionar_e_processar_arquivos)
        select_button.pack(pady=10, padx=10, fill='x')

        self.status_label = ttk.Label(arquivos_frame, text="Status: Aguardando seleção de arquivos.")
        self.status_label.pack(pady=(0, 10))
        
        main_content_frame = ttk.Frame(self.master)
        main_content_frame.pack(padx=10, pady=0, fill='both', expand=True)

        controls_frame = ttk.Frame(main_content_frame, width=450)
        controls_frame.pack(side=tk.LEFT, fill='y', padx=(0, 10)) 
        controls_frame.pack_propagate(False) 

        colunas_group_frame = ttk.LabelFrame(controls_frame, text="2. Seleção de Colunas (Etiquetas de Valor/Categoria)")
        colunas_group_frame.pack(padx=0, pady=0, fill='both', expand=True)

        canvas = tk.Canvas(colunas_group_frame)
        scrollbar = ttk.Scrollbar(colunas_group_frame, orient="vertical", command=canvas.yview)
        self.colunas_frame = ttk.Frame(canvas)

        self.colunas_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.colunas_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        operacoes_frame = ttk.LabelFrame(controls_frame, text="3. Executar Análise e Gráfico")
        operacoes_frame.pack(padx=0, pady=10, fill='x')

        descritiva_button = ttk.Button(operacoes_frame, text="🔢 Análise Descritiva (Contagem/Soma/Média)", command=lambda: self.executar_calculo_ou_analise('descritiva'))
        descritiva_button.pack(fill='x', padx=5, pady=5)

        calc_frame = ttk.Frame(operacoes_frame)
        calc_frame.pack(fill='x', pady=(0, 10))

        soma_button = ttk.Button(calc_frame, text="➕ Calcular SOMA Total", command=lambda: self.executar_calculo_ou_analise('soma'))
        soma_button.pack(side=tk.LEFT, expand=True, fill='x', padx=5)

        mult_button = ttk.Button(calc_frame, text="✖️ Calcular FATURAMENTO TOTAL", command=lambda: self.executar_calculo_ou_analise('multiplicacao'))
        mult_button.pack(side=tk.LEFT, expand=True, fill='x', padx=5)

        # COLUNA DA DIREITA (Gráfico)
        self.grafico_frame = ttk.LabelFrame(main_content_frame, text="4. Visualização do Gráfico de Resultados")
        self.grafico_frame.pack(side=tk.RIGHT, fill='both', expand=True)
        ttk.Label(self.grafico_frame, text="O gráfico aparecerá aqui após você executar a Soma ou Multiplicação.").pack(padx=10, pady=10)

    def _configurar_api_key_wrapper(self):
        openIA.configurar_api_key(self.api_key_entry, self.api_status_label)

    def selecionar_e_processar_arquivos(self):
        
        caminhos_arquivos_selecionados = filedialog.askopenfilenames(
            title="Selecione os arquivos de dados (CSV, Excel, etc.)",
            filetypes=[
                ("Arquivos de Dados de Tabela", "*.csv *.xlsx *.xls"),
                ("Todos os Arquivos", "*.*")
            ]
        )

        if not caminhos_arquivos_selecionados:
            self.status_label.config(text="Status: Seleção cancelada.")
            return

        self.tabela_total = pd.DataFrame()
        arquivos_lidos = 0
        
        for caminho_completo in caminhos_arquivos_selecionados:
            arquivo = os.path.basename(caminho_completo) 
            
            try:
                df = None
                if arquivo.lower().endswith('.csv'):
                    try:
                        df = pd.read_csv(caminho_completo, on_bad_lines='skip')
                    except UnicodeDecodeError:
                        df = pd.read_csv(caminho_completo, on_bad_lines='skip', encoding='latin1') 
                elif arquivo.lower().endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(caminho_completo) 
                else:
                    continue
                
                df.columns = df.columns.astype(str)
                self.tabela_total = pd.concat([self.tabela_total, df], ignore_index=True)
                arquivos_lidos += 1
                
            except Exception as erro:
                messagebox.showerror("Erro de Leitura", f"Erro fatal ao ler ou concatenar o arquivo {arquivo}: {erro}")

        if self.tabela_total.empty:
            self.status_label.config(text="Status: Nenhum dado válido foi lido.")
            self.colunas_disponiveis = []
            self.coluna_sugerida = None
            self.coluna_classificacao = {} 
        else:
            self.colunas_disponiveis = self.tabela_total.columns.tolist()
            self.status_label.config(text=f"Status: ✅ {arquivos_lidos} arquivos lidos. {len(self.tabela_total)} linhas.")
            
            self.coluna_classificacao = data_processor.analisar_tipos_colunas(self.tabela_total)
            
            self.coluna_sugerida = openIA.analisar_colunas_com_ia(self.tabela_total)
            
        self.atualizar_lista_colunas()
        
    def atualizar_lista_colunas(self):
        for widget in self.colunas_frame.winfo_children():
            widget.destroy()

        self.colunas_selecionadas_gui.clear()
        
        if not self.colunas_disponiveis:
            ttk.Label(self.colunas_frame, text="Nenhum arquivo carregado ou colunas encontradas.").pack(padx=10, pady=10)
            return

        for col in self.colunas_disponiveis:
            var = tk.BooleanVar()
            self.colunas_selecionadas_gui[col] = var
            
            classificacao = self.coluna_classificacao.get(col, 'Desconhecido')
            tag = f"[{classificacao}]"
            
            text_label = f"{col} {tag}"
            
            if self.coluna_sugerida and col.strip().lower() == self.coluna_sugerida.strip().lower():
                var.set(True)
                text_label += " (SUGESTÃO IA)"
            
            cb = ttk.Checkbutton(self.colunas_frame, text=text_label, variable=var)
            cb.pack(anchor='w', padx=5, pady=2)
            
    def executar_calculo_ou_analise(self, tipo):
        colunas_para_processar = [col for col, var in self.colunas_selecionadas_gui.items() if var.get()]
        
        if not colunas_para_processar:
            messagebox.showwarning("Aviso", "Selecione pelo menos uma coluna.")
            return

        if self.tabela_total.empty:
            messagebox.showwarning("Aviso", "Nenhum dado carregado. Carregue os arquivos primeiro.")
            return
        
        if tipo in ['soma', 'multiplicacao']:
            data_processor.processar_dados(
                self.tabela_total, 
                colunas_para_processar, 
                tipo, 
                self.grafico_frame, 
                colunas_para_processar
            )
        elif tipo == 'descritiva':
            data_processor.analise_descritiva(self.tabela_total, colunas_para_processar)

def iniciar_gui():
    root = tk.Tk()
    AppGUI(root)
    root.mainloop()