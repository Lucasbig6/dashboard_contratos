# 📊 Dashboard de Contratos e Pagamentos Públicos - Piauí (Dados Fictícios)

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30-orange)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Express-purple)](https://plotly.com/python/)


![Dashboard Interativo](assets/brave_H194MxmscB%20-%20Trim.gif)

## 🔹 Sobre o Projeto
Este Projeto consiste em um **Dashboard interativo** que analisa contratos, clientes e pagamentos de empresas fictícias no Estado do Piauí.
O objetivo é demonstrar habilidades em **Análise de dados, visualização interativa e storytelling com dados**, utilizando **Python** e bibliotecas modernas.

---

## 🔹 Tecnologias e Bibliotecas Utilizadas
- **Python 3.13.7**
- **Streamlit** → para criar o dashboard web interativo
- **Pandas** → manipulação e tratamento de dados
- **Plotly Express** → gráficos interativos, responsivos e formatados para valores monetários
- **Faker** → geração de dados fictícios realistas (clientes, contratos e pagamentos) 

---

## 🔹 Estrutura do Projeto

```shell
├── data/
│ ├── clientes.csv
│ ├── contratos.csv
│ └── pagamentos.csv
├── app.py # Script principal do Dashboard
├── README.md
└── requirements.txt
```

## 🔹 Funcionalidades e KPIs
O dashboard apresenta os principais indicadores financeiros e contratuais:

- 💰 **Receita Total**  
- 💵 **Ticket Médio** por contrato  
- 📑 **Contratos Ativos**  
- ⚠️ **Inadimplência (%)**  

Gráficos interativos:
- 📍 **Receita por cidade e por setor**  
- 💳 **Distribuição de formas de pagamento**  
- 📈 **Evolução da receita mensal**  

Todos os valores são exibidos em **R$ (Real brasileiro)** com separador de milhar e 2 casas decimais.

---
## 🔹 Técnicas e Aprendizados
- Integração de múltiplos datasets com `merge` do Pandas  
- Filtragem dinâmica usando widgets do Streamlit  
- Visualizações interativas e responsivas com Plotly Express  
- Formatação monetária avançada para dashboards  
- Criação de dados fictícios realistas para portfólio com Faker 

