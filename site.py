import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import gspread 

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(layout="wide", page_title="Dashboard Superstore")

# --- 2. CARREGAMENTO DOS DADOS  ---
@st.cache_data(ttl=10) 
def carregar_dados():
   
    try:

        gc = gspread.service_account_from_dict(st.secrets["connections"]["gsheets"])
        spreadsheet = gc.open(st.secrets["connections"]["gsheets"]["spreadsheet"])
        worksheet = spreadsheet.sheet1
        dados = worksheet.get_all_records()
        df = pd.DataFrame(dados)
        

        if 'Order Date' in df.columns:
            df['Order Date'] = pd.to_datetime(df['Order Date'])
        if 'Sales' in df.columns:
            df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
        if 'Profit' in df.columns:
            df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
        if 'Discount' in df.columns:
            df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce')
        if 'Shipping Cost' in df.columns: 
            df['Shipping Cost'] = pd.to_numeric(df['Shipping Cost'], errors='coerce')
        if 'Ship Date' in df.columns:
            df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')

        df.dropna(subset=['Sales', 'Profit'], inplace=True)

        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        st.stop()

dataset_superstore = carregar_dados()

# --- 3. FUNÇÕES AUXILIARES ---
def formatar_numero(valor, prefixo='R$'):
    return f"{prefixo} {valor:,.2f}"

def formatar_percentual(valor):
    return f"{valor:.2f}%"

def estilizar_dataframe(df, colunas_moeda, colunas_percentual):
    format_dict = {}
    for col in colunas_moeda:
        if col in df.columns: # Garante que a coluna existe no DataFrame
            format_dict[col] = lambda x: formatar_numero(x)
    for col in colunas_percentual:
        if col in df.columns: # Garante que a coluna existe no DataFrame
            format_dict[col] = lambda x: formatar_percentual(x)

    styled_df = df.style.format(format_dict)
    
    # Aplica formatação condicional para lucro e margem de lucro 
    if 'Lucro' in df.columns:
        styled_df = styled_df.applymap(lambda v: 'color: red' if v < 0 else 'color: green', subset=['Lucro'])
    if 'Margem Lucro' in df.columns: # Ajustado para o nome que você usará no DataFrame
        styled_df = styled_df.applymap(lambda v: 'color: red' if v < 0 else 'color: green', subset=['Margem Lucro'])

    return styled_df

# --- 4. TÍTULO E INTRODUÇÃO ---
st.title("Dashboard Interativo Superstore")
st.markdown("Uma análise visual dos principais insights do relatório, agora construída com Python, Streamlit e Plotly.")

# --- 5. ABAS DE NAVEGAÇÃO ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Visão Geral", "Produtos", "Geográfica", "Clientes", "Descontos", "Envio", "Recomendações"
])

# --- 6. ABA 1: VISÃO GERAL ---
with tab1:
    st.header("Visão Geral do Desempenho")
    st.markdown("""
    Esta seção apresenta os indicadores chave de desempenho (KPIs) da Superstore, incluindo vendas totais, 
    lucro total e margem de lucro geral. Além disso, exploramos as tendências de vendas e lucro ao longo dos anos.
    """)
    
    # KPIs Calculados a partir dos dados brutos
    total_sales = dataset_superstore['Sales'].sum()
    total_profit = dataset_superstore['Profit'].sum()
    overall_profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Vendas Totais", formatar_numero(total_sales))
    col2.metric("Lucro Total", formatar_numero(total_profit))
    col3.metric("Margem de Lucro Geral", formatar_percentual(overall_profit_margin))

    st.markdown("---")
    
    # Gráfico de Desempenho Anual
    st.subheader("Desempenho Anual")
    
    # Crie a coluna 'Ano' a partir da 'Order Date'
    if 'Order Date' in dataset_superstore.columns:
        yearly_df = dataset_superstore.groupby(dataset_superstore['Order Date'].dt.year).agg(
            Vendas=('Sales', 'sum'),
            Lucro=('Profit', 'sum')
        ).reset_index()
        yearly_df.rename(columns={'Order Date': 'Ano'}, inplace=True) # Renomeia a coluna gerada pelo groupby
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=yearly_df['Ano'], y=yearly_df['Vendas'], mode='lines+markers', name='Vendas'))
        fig.add_trace(go.Scatter(x=yearly_df['Ano'], y=yearly_df['Lucro'], mode='lines+markers', name='Lucro'))
        
        fig.update_layout(title="Vendas e Lucro por Ano", xaxis_title="Ano", yaxis_title="Valor (R$)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Coluna 'Order Date' não encontrada para calcular o desempenho anual.")


# --- 7. ABA 2: PRODUTOS ---
with tab2:
    st.header("Desempenho de Produtos")
    st.markdown("""
    Analisamos o desempenho de vendas e lucratividade por categoria e subcategoria de produtos. 
    O objetivo é identificar quais produtos são os mais rentáveis e quais podem estar impactando negativamente a lucratividade.
    """)
    
    # Desempenho por Categoria
    st.subheader("Desempenho por Categoria")
    if 'Category' in dataset_superstore.columns:
        category_df = dataset_superstore.groupby('Category').agg(
            sales=('Sales', 'sum'),
            profit=('Profit', 'sum')
        ).reset_index()
        category_df['profitMargin'] = (category_df['profit'] / category_df['sales']) * 100
        
        fig = px.bar(category_df, x='Category', y=['sales', 'profit'], barmode='group',
                     labels={'value': 'Valor (R$)', 'Category': 'Categoria'},
                     title="Vendas vs. Lucro por Categoria",
                     color_discrete_map={'sales': '#1f77b4', 'profit': '#2ca02c'})
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(estilizar_dataframe(category_df.rename(columns={
            'Category': 'Categoria', 'sales': 'Vendas', 'profit': 'Lucro', 'profitMargin': 'Margem Lucro'
        }), ['Vendas', 'Lucro'], ['Margem Lucro']), use_container_width=True)
    else:
        st.warning("Coluna 'Category' não encontrada para análise de produtos por categoria.")

    st.markdown("---")

    # Lucro por Subcategoria
    st.subheader("Lucro por Subcategoria (Destaques)")
    if 'Sub-Category' in dataset_superstore.columns:
        subcategory_profit_df = dataset_superstore.groupby('Sub-Category').agg(
            profit=('Profit', 'sum')
        ).reset_index()
        subcategory_profit_df['Cor'] = ['green' if x >= 0 else 'red' for x in subcategory_profit_df['profit']]
        
        fig = px.bar(subcategory_profit_df.sort_values('profit', ascending=True), 
                     x='profit', y='Sub-Category', orientation='h', 
                     title="Lucro por Subcategoria",
                     labels={'profit': 'Lucro (R$)', 'Sub-Category': 'Subcategoria'})
        fig.update_traces(marker_color=subcategory_profit_df.sort_values('profit', ascending=True)['Cor'])
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Subcategorias com Prejuízo")
        # Filtra subcategorias com lucro negativo e calcula o desempenho
        loss_subcategories_df = dataset_superstore[dataset_superstore['Profit'] < 0].groupby(['Category', 'Sub-Category']).agg(
            sales=('Sales', 'sum'),
            profit=('Profit', 'sum')
        ).reset_index()
        loss_subcategories_df['profitMargin'] = (loss_subcategories_df['profit'] / loss_subcategories_df['sales']) * 100 if not loss_subcategories_df.empty else 0 # Evita divisão por zero se vazio
        
        st.dataframe(estilizar_dataframe(loss_subcategories_df.rename(columns={
            'Category': 'Categoria', 'Sub-Category': 'Subcategoria', 'sales': 'Vendas', 'profit': 'Lucro', 'profitMargin': 'Margem Lucro'
        }), ['Vendas', 'Lucro'], ['Margem Lucro']), use_container_width=True)
    else:
        st.warning("Coluna 'Sub-Category' não encontrada para análise de produtos por subcategoria.")

# --- 8. ABA 3: GEOGRÁFICA ---
with tab3:
    st.header("Análise Geográfica")
    st.markdown("""
    Esta seção explora o desempenho da Superstore em diferentes regiões e estados, 
    identificando onde a empresa é mais forte e onde existem oportunidades de melhoria.
    """)

    # Desempenho por Região
    st.subheader("Desempenho por Região")
    if 'Region' in dataset_superstore.columns:
        region_df = dataset_superstore.groupby('Region').agg(
            sales=('Sales', 'sum'),
            profit=('Profit', 'sum')
        ).reset_index()
        region_df['profitMargin'] = (region_df['profit'] / region_df['sales']) * 100
        
        fig = px.bar(region_df, x='Region', y=['sales', 'profit'],
                     barmode='group', title="Vendas vs. Lucro por Região",
                     labels={'value': 'Valor (R$)', 'Region': 'Região'})
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(estilizar_dataframe(region_df.rename(columns={
            'Region': 'Região', 'sales': 'Vendas', 'profit': 'Lucro', 'profitMargin': 'Margem Lucro'
        }), ['Vendas', 'Lucro'], ['Margem Lucro']), use_container_width=True)
    else:
        st.warning("Coluna 'Region' não encontrada para análise geográfica.")

    st.markdown("---")

    # Estados com Prejuízo
    st.subheader("Estados com Prejuízo")
    if 'State' in dataset_superstore.columns:
        loss_states_df = dataset_superstore[dataset_superstore['Profit'] < 0].groupby('State').agg(
            sales=('Sales', 'sum'),
            profit=('Profit', 'sum')
        ).reset_index()
        loss_states_df['profitMargin'] = (loss_states_df['profit'] / loss_states_df['sales']) * 100 if not loss_states_df.empty else 0
        
        st.dataframe(estilizar_dataframe(loss_states_df.rename(columns={
            'State': 'Estado', 'sales': 'Vendas', 'profit': 'Lucro', 'profitMargin': 'Margem Lucro'
        }), ['Vendas', 'Lucro'], ['Margem Lucro']), use_container_width=True)
    else:
        st.warning("Coluna 'State' não encontrada para análise geográfica.")
        
# --- 9. ABA 4: CLIENTES ---
with tab4:
    st.header("Análise de Clientes")
    st.markdown("Análise do desempenho com base nos diferentes segmentos de clientes para direcionar estratégias de marketing e vendas.")
    
    if 'Segment' in dataset_superstore.columns:
        segment_df = dataset_superstore.groupby('Segment').agg(
            sales=('Sales', 'sum'),
            profit=('Profit', 'sum')
        ).reset_index()
        segment_df['profitMargin'] = (segment_df['profit'] / segment_df['sales']) * 100
        
        # Gráfico de Pizza (Doughnut)
        st.subheader("Distribuição do Lucro por Segmento")
        fig = px.pie(segment_df, names='Segment', values='profit', title="Lucro por Segmento de Cliente", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Desempenho Detalhado por Segmento")
        st.dataframe(estilizar_dataframe(segment_df.rename(columns={
            'Segment': 'Segmento', 'sales': 'Vendas', 'profit': 'Lucro', 'profitMargin': 'Margem Lucro'
        }), ['Vendas', 'Lucro'], ['Margem Lucro']), use_container_width=True)
    else:
        st.warning("Coluna 'Segment' não encontrada para análise de clientes.")
        
# --- 10. ABA 5: DESCONTOS ---
with tab5:
    st.header("Impacto dos Descontos")
    st.markdown("""
    Esta seção investiga a relação entre os descontos aplicados e a lucratividade, 
    revelando o impacto de diferentes faixas de desconto na margem de lucro.
    """)

    if 'Discount' in dataset_superstore.columns and 'Profit' in dataset_superstore.columns and 'Sales' in dataset_superstore.columns:
        # Matriz de Correlação (apenas para colunas numéricas relevantes)
        st.subheader("Matriz de Correlação")
        # Seleciona apenas as colunas numéricas de interesse
        corr_cols = ['Sales', 'Profit', 'Discount']
        numeric_df = dataset_superstore[corr_cols].dropna()
        
        if not numeric_df.empty:
            corr_matrix = numeric_df.corr()
            st.dataframe(corr_matrix.style.background_gradient(cmap='coolwarm', axis=None).format("{:.2f}"))
        else:
            st.warning("Não há dados numéricos suficientes para calcular a matriz de correlação.")
        
        st.markdown("---")

        # Lucratividade por Faixa de Desconto
        st.subheader("Lucratividade por Faixa de Desconto")
        
        # Cria faixas de desconto
        bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        labels = [f'{int(b*100)}% - {int((b+0.1)*100)}%' for b in bins[:-1]]
        # Último label para cobrir o máximo
        labels[-1] = '90% - 100%' 
        
        dataset_superstore['Discount_Range'] = pd.cut(dataset_superstore['Discount'], bins=bins, labels=labels, right=False)
        
        discount_impact_df = dataset_superstore.groupby('Discount_Range').agg(
            sales=('Sales', 'sum'),
            profit=('Profit', 'sum')
        ).reset_index()
        discount_impact_df['profitMargin'] = (discount_impact_df['profit'] / discount_impact_df['sales']) * 100
        
        discount_impact_df['Cor'] = ['green' if x >= 0 else 'red' for x in discount_impact_df['profitMargin']]
        
        fig = px.bar(discount_impact_df, x='Discount_Range', y='profitMargin', 
                     title="Margem de Lucro por Faixa de Desconto",
                     labels={'Discount_Range': 'Faixa de Desconto', 'profitMargin': 'Margem de Lucro (%)'})
        fig.update_traces(marker_color=discount_impact_df['Cor'])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Colunas 'Discount', 'Profit' ou 'Sales' não encontradas para análise de descontos.")

# --- 11. ABA 6: ENVIO ---
with tab6:
    st.header("Logística de Envio")
    st.markdown("Análise do desempenho dos diferentes modos de envio e o impacto do tempo de envio na operação.")
    
    if 'Ship Mode' in dataset_superstore.columns and 'Order Date' in dataset_superstore.columns and 'Ship Date' in dataset_superstore.columns:
        # Calcular tempo de envio (em dias)
        dataset_superstore['Shipping Time'] = (dataset_superstore['Ship Date'] - dataset_superstore['Order Date']).dt.days

        ship_mode_df = dataset_superstore.groupby('Ship Mode').agg(
            sales=('Sales', 'sum'),
            profit=('Profit', 'sum'),
            avgTime=('Shipping Time', 'mean')
        ).reset_index()
        ship_mode_df['profitMargin'] = (ship_mode_df['profit'] / ship_mode_df['sales']) * 100
        
        st.subheader("Desempenho por Modo de Envio")
        st.dataframe(estilizar_dataframe(ship_mode_df.rename(columns={
            'Ship Mode': 'Modo de Envio', 'sales': 'Vendas', 'profit': 'Lucro', 'profitMargin': 'Margem Lucro', 'avgTime': 'Tempo Médio (dias)'
        }), ['Vendas', 'Lucro'], ['Margem Lucro']), use_container_width=True)

        st.markdown("---")
        
        # KPIs de Tempo de Envio
        avg_shipping_time = dataset_superstore['Shipping Time'].mean()
        median_shipping_time = dataset_superstore['Shipping Time'].median()
        
        col1, col2 = st.columns(2)
        col1.metric("Tempo Médio de Envio Geral", f"{avg_shipping_time:.2f} dias")
        col2.metric("Mediana do Tempo de Envio", f"{median_shipping_time:.2f} dias")
    else:
        st.warning("Colunas 'Ship Mode', 'Order Date' ou 'Ship Date' não encontradas para análise de envio.")

# --- 12. ABA 7: RECOMENDAÇÕES ---
with tab7:
    st.header("Conclusões e Recomendações Estratégicas")
    st.markdown("""
    Com base na análise detalhada dos dados da Superstore, esta seção resume as principais conclusões e 
    sugere ações estratégicas para otimizar o desempenho e aumentar a lucratividade.
    """)
    
    recomendacoes = [
        "Foco em produtos de alta margem e categorias com bom desempenho.",
        "Reavaliar a estratégia de preços/descontos para subcategorias com prejuízo (ex: 'Tables', 'Bookcases').",
        "Investigar o motivo do baixo desempenho ou prejuízo em regiões/estados específicos.",
        "Otimizar a logística de envio para reduzir custos e melhorar a satisfação do cliente.",
        "Desenvolver campanhas de marketing direcionadas para segmentos de clientes com maior potencial de lucro."
    ]
    for rec in recomendacoes:
        st.markdown(f"- {rec}")
