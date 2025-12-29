<h1 align = "center">DataShow 2.0 - Análise Inteligente de Dados</h1>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-009688?style=for-the-badge&logo=python&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=plotly&logoColor=white)

[![Status](https://img.shields.io/badge/Status-Ativo-success?style=flat-square)](https://github.com)
[![Licença](https://img.shields.io/badge/Licença-MIT-blue?style=flat-square)](LICENSE)
[![Versão](https://img.shields.io/badge/Versão-2.0-orange?style=flat-square)](https://github.com)

</div>

---

## Sobre o Projeto

**DataShow 2.0** é uma aplicação desktop inteligente para análise de dados comerciais e financeiros. Desenvolvida em Python com interface gráfica Tkinter, a ferramenta permite processar múltiplos arquivos de dados (CSV, Excel) e realizar análises descritivas, cálculos de faturamento e visualizações gráficas de forma simples e intuitiva.


### Diferenciais

- **Integração com IA da OpenAI** para sugestão automática de colunas relevantes
- **Geração automática de gráficos** com Matplotlib
- **Processamento de múltiplos arquivos** simultaneamente
- **Análises estatísticas** completas (soma, média, contagem, faturamento)
- **Classificação inteligente** de colunas (Unitário, Total, Categoria, ID)

---

<div align="left">
    <img height="500" src="https://github.com/user-attachments/assets/b896a426-4e2a-4c01-8305-4807df6f191f" alt="Screenshot 1 do DataShow 2.0"/>
</div>

---

###  1. Carregamento de Dados

- Suporte para arquivos **CSV** e **Excel** (XLSX, XLS)
- Processamento simultâneo de múltiplos arquivos
- Concatenação automática de datasets
- Tratamento de erros e encoding (Latin1 para compatibilidade)

---

<div align="left">
    <img height="500" src="https://github.com/user-attachments/assets/cc88b4f4-e16f-4e61-a9a0-2efedddf2517" alt="Screenshot 2 do DataShow 2.0"/>
</div>

### 2. Inteligência Artificial (OpenAI)

A integração com a API da OpenAI é o coração inteligente do DataShow 2.0:

Como Funciona:

# O sistema envia a estrutura das colunas para o GPT-3.5-turbo

<div align="left">
    <img height="500" src="https://github.com/user-attachments/assets/6b459138-8328-43e7-8f2b-90455976d221"/>
</div>


#### Benefícios da IA:

- **Sugestão Automática**: Identifica automaticamente qual coluna representa valores monetários
- **Economia de Tempo**: Elimina a necessidade de análise manual de colunas
- **Precisão**: Utiliza GPT-3.5-turbo para reconhecimento de padrões
- **Feedback Visual**: Marca a coluna sugerida com tag "(SUGESTÃO IA)"

#### Configuração:

1. Insira sua chave API da OpenAI (formato: `sk-...`)
2. Clique em " Configurar Chave"
3. A IA estará pronta para auxiliar nas análises

<div align="left">
    <img height="500" src="https://github.com/user-attachments/assets/ff07ceef-696b-41e4-8b2b-1de92cc57350"/>
</div>

> **Nota**: A funcionalidade de IA é opcional. O sistema funciona normalmente sem ela, mas a sugestão inteligente não estará disponível.

### 3. Classificação Automática de Colunas

<div align="left">
    <img height="600" src="https://github.com/user-attachments/assets/4303100b-f523-4878-bb7e-fa0b099f3366"/>
</div>

---

O sistema analisa e classifica automaticamente cada coluna:

| Classificação | Descrição                   | Exemplo                 |
| ------------- | --------------------------- | ----------------------- |
| **Unitario** | Valores baixos (< R$ 5.000) | Preço por unidade       |
| **Total**     | Valores altos (> R$ 5.000)  | Faturamento total       |
| **Categoria** | Dados textuais              | Nome do produto, região |
| **ID/Código** | Identificadores únicos      | Código do pedido        |




### 4. Análises Disponíveis

#### Análise Descritiva

Para cada coluna selecionada:

- **Colunas Numéricas**: Total de itens, Soma total, Média
- **Colunas Categóricas**: Total de registros, Valores únicos, Valor mais comum

#### ➕ Cálculo de SOMA Total

- Soma valores de múltiplas colunas
- Gera gráfico de barras comparativo
- Exibe resultado formatado em R$

#### ✖️ Cálculo de FATURAMENTO

- Multiplica valores (Ex: Quantidade × Preço Unitário)
- Calcula faturamento total global
- Visualização gráfica por categoria

### 5. Visualizações Gráficas

<div align="left">
    <img height="600" src="https://github.com/user-attachments/assets/6129b02b-ccd6-418a-92d0-3f0b2d038885"/>
</div>

---

- Gráficos de barras automáticos
- Agrupamento inteligente por categorias
- Formatação monetária (R$)
- Rotação de labels para melhor legibilidade
- Exibição de valores sobre as barras

---

### IA & APIs

- **OpenAI API (GPT-3.5-turbo)** - Sugestões inteligentes de colunas

### Bibliotecas Auxiliares

- **ttk** - Widgets modernos para Tkinter
- **os** - Manipulação de arquivos
- **matplotlib.backends.backend_tkagg** - Integração Matplotlib + Tkinter

### 2️ Configurar a IA (Opcional)

1. Obtenha sua chave API em [OpenAI Platform](https://platform.openai.com/api-keys)
2. Cole a chave no campo "ConfiguraÃ§Ã£o da OpenAI API Key"
3. Clique em " Configurar Chave"



