from openai import OpenAI
import tkinter as tk
from tkinter import messagebox

client = None

def configurar_api_key(api_key_entry, api_status_label):
    global client
    key = api_key_entry.get().strip()
    
    if not key:
        api_status_label.config(text="Status da API: ❓ Insira uma chave válida.", foreground="orange")
        messagebox.showwarning("Aviso", "Por favor, insira uma chave de API válida.")
        return False
        
    try:
        client = OpenAI(api_key=key)
        
        api_status_label.config(text="Status da API: ✅ Chave configurada com sucesso.", foreground="green")
        messagebox.showinfo("Sucesso", "Chave de API da OpenAI configurada com sucesso!")
        
        api_key_entry.delete(0, tk.END) 
        return True
        
    except Exception as e:
        client = None
        api_status_label.config(text=f"Status da API: ❌ Erro de Configuração. {e}", foreground="red")
        messagebox.showerror("Erro de Configuração", "Não foi possível configurar o cliente OpenAI. Verifique o formato da chave. (Erro 401)")
        return False

def analisar_colunas_com_ia(df):
    if client is None:
        return None

    colunas_info = df.dtypes.to_frame(name='Tipo de Dado').reset_index().to_string(index=False)
    
    prompt = f"""
    Eu tenho um DataFrame pandas... A estrutura das colunas é: {colunas_info}.
    Identifique **SOMENTE O NOME DA COLUNA** que tem a maior probabilidade de representar o **faturamento ou valor total da transação**. Responda "NENHUMA" se não for óbvio.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        sugestao = response.choices[0].message.content.strip()
        return sugestao.replace("'", "").replace('"', '') if sugestao != "NENHUMA" else None
        
    except Exception as e:
        messagebox.showerror("Erro de IA", f"Falha na comunicação com a OpenAI. Erro: {e}")
        return None