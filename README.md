# **Dashboard Dinâmico de Análise da Superstore** 

---

### **Autor:** [Rafael Fabiano do Nascimento]
### **Link para a Aplicação:** [https://dashboard-vendas-superstore.streamlit.app/]

---

## **1. Visão Geral do Projeto**

Este projeto é uma aplicação web interativa para análise de dados de vendas da "Superstore". Diferente de um relatório estático, este dashboard foi desenvolvido para ser uma ferramenta dinâmica, conectada diretamente a uma fonte de dados externa (Google Sheets), permitindo que as visualizações e KPIs reflitam atualizações nos dados em tempo quase real.

O objetivo é fornecer uma visão clara e acionável do desempenho do negócio, explorando métricas de vendas, lucratividade e logística através de uma interface intuitiva e responsiva.

---

## **2. Arquitetura da Solução**

A solução foi projetada com uma arquitetura moderna para aplicações de dados, separando a fonte de dados da lógica da aplicação e da interface do usuário.

* **Fonte de Dados (Data Layer):** Os dados brutos da Superstore são hospedados em uma planilha do **Google Sheets**. Essa abordagem permite que os dados sejam atualizados por qualquer pessoa com permissão, sem a necessidade de modificar o código da aplicação ou realizar um novo deploy.

* **Aplicação Web (Application Layer):** O coração do projeto, desenvolvido em **Python** e rodando na **Streamlit Community Cloud**. Esta camada é responsável por conectar-se de forma segura à fonte de dados, buscar, processar e agregar os dados em tempo quase real, implementando um sistema de cache inteligente para otimizar a performance.

* **Interface do Usuário (Presentation Layer):** A interface com a qual o usuário interage, construída com **Streamlit**. Ela apresenta os dados processados através de gráficos interativos (Plotly), tabelas e métricas.

---

## **3. Metodologia e Ferramentas**

### **Fonte de Dados**
O dataset "Sample - Superstore" foi carregado em uma planilha do Google Sheets, servindo como uma base de dados centralizada e de fácil atualização. Vale ressaltar que são dados fictícios e nenhum dado sensível foi utilizado.

### **Processamento e Análise**
A aplicação não utiliza dados fixos. Em vez disso, a cada sessão, ela executa as seguintes etapas:
1.  **Conexão Segura:** Utiliza a biblioteca `st-gsheets-connection` para estabelecer uma conexão segura e autorizada com la API do Google Sheets.
2.  **Extração de Dados:** Lê a planilha e a carrega em um DataFrame do Pandas.
3.  **Análise Dinâmica:** Todos os cálculos de KPIs e agregações são performados em tempo de execução.
4.  **Otimização de Performance:** A função de carregamento de dados é otimizada com `@st.cache_data`, que armazena o resultado da consulta por 10 minutos para garantir que o dashboard permaneça rápido e responsivo.

### **Tecnologias Utilizadas**
* **Linguagem:** Python 3.11
* **Framework Web:** Streamlit
* **Manipulação de Dados:** Pandas
* **Visualização de Dados:** Plotly, Matplotlib
* **Conexão de Dados:** `st-gsheets-connection`
* **Base de Dados:** Google Sheets
* **Versionamento:** Git & GitHub

---

## **4. Principais Análises e Recomendações**

A análise dos dados aponta para insights estratégicos cruciais:
* **Rentabilidade por Produto:** A categoria **Tecnologia** se mantém como a mais lucrativa, enquanto **Móveis**, especificamente as subcategorias **Mesas** e **Estantes**, geram prejuízo e exigem uma revisão estratégica.
* **Impacto dos Descontos:** Descontos agressivos (acima de 20%) estão diretamente correlacionados com margens de lucro negativas, indicando a necessidade de uma política de precificação mais inteligente.
* **Desempenho Geográfico:** As regiões **Oeste** e **Leste** lideram em lucratividade, enquanto a região **Central** necessita de intervenção para reverter as perdas em estados-chave.

---
