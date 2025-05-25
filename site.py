import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(layout="wide", page_title="Dashboard de Análise Superstore")

# --- DADOS ---
# Os dados são os mesmos do projeto original, agora em estruturas de dados do Python/Pandas
superstore_data = {
    'visaoGeral': {
        'totalSales': 2297200.86,
        'totalProfit': 286397.02,
        'overallProfitMargin': 12.47,
        'yearlyPerformance': pd.DataFrame({
            "Ano": ["2014", "2015", "2016", "2017"],
            "Vendas": [484247, 470532, 609205, 733215],
            "Lucro": [49543, 48795, 62026, 93439]
        }),
    },
    'produtos': {
        'categoryPerformance': pd.DataFrame([
            { 'category': "Technology", 'sales': 836154, 'profit': 145454, 'profitMargin': 17.39 },
            { 'category': "Office Supplies", 'sales': 719047, 'profit': 122490, 'profitMargin': 17.03 },
            { 'category': "Furniture", 'sales': 741999, 'profit': 18451, 'profitMargin': 2.49 }
        ]),
        'subCategoryProfit': pd.DataFrame([
            { 'subCategory': "Copiers", 'profit': 55617 },
            { 'subCategory': "Phones", 'profit': 44515 },
            { 'subCategory': "Paper", 'profit': 34053 },
            { 'subCategory': "Accessories", 'profit': 41936 },
            { 'subCategory': "Binders", 'profit': 30221 },
            { 'subCategory': "Tables", 'profit': -17725 },
            { 'subCategory': "Bookcases", 'profit': -3472 },
            { 'subCategory': "Supplies", 'profit': -1189 }
        ]),
        'lossSubCategoryTable': pd.DataFrame([
             { 'category': "Furniture", 'subCategory': "Tables", 'sales': 206965, 'profit': -17725, 'profitMargin': -8.56 },
             { 'category': "Furniture", 'subCategory': "Bookcases", 'sales': 114879, 'profit': -3472, 'profitMargin': -3.02 },
             { 'category': "Office Supplies", 'subCategory': "Supplies", 'sales': 46673, 'profit': -1189, 'profitMargin': -2.55 }
        ]),
    },
    'geografica': {
        'regionPerformance': pd.DataFrame([
            { 'region': "West", 'sales': 725457, 'profit': 108418, 'profitMargin': 14.94 },
            { 'region': "East", 'sales': 678781, 'profit': 91522, 'profitMargin': 13.48 },
            { 'region': "Central", 'sales': 501239, 'profit': 39706, 'profitMargin': 7.92 },
            { 'region': "South", 'sales': 391721, 'profit': 46749, 'profitMargin': 11.93 }
        ]),
        'lossStates': pd.DataFrame([
            { 'state': "Texas", 'sales': 170188, 'profit': -25729, 'profitMargin': -15.12 },
            { 'state': "Pennsylvania", 'sales': 116511, 'profit': -15559, 'profitMargin': -13.35 },
            { 'state': "Illinois", 'sales': 80166, 'profit': -12607, 'profitMargin': -15.72 }
        ])
    },
    'clientes': {
        'segmentPerformance': pd.DataFrame([
            { 'segment': "Consumer", 'sales': 1161401, 'profit': 134119, 'profitMargin': 11.55 },
            { 'segment': "Corporate", 'sales': 706146, 'profit': 91979, 'profitMargin': 13.03 },
            { 'segment': "Home Office", 'sales': 429653, 'profit': 60298, 'profitMargin': 14.03 }
        ])
    },
    'descontos': {
        'correlationMatrix': pd.DataFrame([
            { 'Métrica': "Sales", 'Sales': 1.00, 'Quantity': 0.20, 'Discount': 0.00, 'Profit': 0.48 },
            { 'Métrica': "Quantity", 'Sales': 0.20, 'Quantity': 1.00, 'Discount': 0.01, 'Profit': 0.07 },
            { 'Métrica': "Discount", 'Sales': 0.00, 'Quantity': 0.01, 'Discount': 1.00, 'Profit': -0.22 },
            { 'Métrica': "Profit", 'Sales': 0.48, 'Quantity': 0.07, 'Discount': -0.22, 'Profit': 1.00 }
        ]).set_index('Métrica'),
        'discountImpact': pd.DataFrame([
            { 'range': "0%", 'profitMargin': 20.00 },
            { 'range': "1-20%", 'profitMargin': 12.50 },
            { 'range': "21-40%", 'profitMargin': -3.33 },
            { 'range': "41-60%", 'profitMargin': -33.33 },
            { 'range': "61-80%", 'profitMargin': -80.00 }
        ])
    },
    'envio': {
        'shipModePerformance': pd.DataFrame([
            { 'mode': "Standard Class", 'sales': 1358216, 'profit': 164088, 'profitMargin': 12.08, 'avgTime': 4.96},
            { 'mode': "Second Class", 'sales': 459193, 'profit': 57446, 'profitMargin': 12.51, 'avgTime': 3.83},
            { 'mode': "First Class", 'sales': 351428, 'profit': 48969, 'profitMargin': 13.93, 'avgTime': 2.60},
            { 'mode': "Same Day", 'sales': 128363, 'profit': 15893, 'profitMargin': 12.38, 'avgTime': 0.94}
        ])
    },
    'recomendacoes': [
        "**Foco na Lucratividade, Não Apenas Vendas:** Priorizar estratégias que aumentem a margem de lucro. Revisar precificação, custos e política de descontos para itens/áreas problemáticas.",
        "**Gestão Estratégica de Descontos:** Implementar uma política de descontos mais inteligente. Evitar descontos agressivos generalizados e focar em promoções direcionadas que não comprometam a margem.",
        "**Otimização Geográfica:** Investigar a fundo as causas do baixo desempenho em regiões/estados específicos. Adaptar estratégias de marketing e vendas regionalmente.",
        "**Entender e Engajar Segmentos de Clientes:** Desenvolver personas para cada segmento e personalizar as estratégias de marketing, comunicação e oferta de produtos.",
        "**Eficiência Logística e de Envio:** Monitorar continuamente os tempos de envio. Otimizar processos logísticos para reduzir prazos e custos.",
        "**Monitoramento Contínuo:** Implementar dashboards e relatórios regulares para acompanhar os KPIs identificados."
    ]
}

# --- FUNÇÕES AUXILIARES ---
def formatar_numero(valor, prefixo='R$'):
    return f"{prefixo} {valor:,.2f}"

def formatar_percentual(valor):
    return f"{valor:.2f}%"

# Função para estilizar DataFrames
def estilizar_dataframe(df, colunas_moeda, colunas_percentual):
    format_dict = {}
    for col in colunas_moeda:
        format_dict[col] = lambda x: formatar_numero(x)
    for col in colunas_percentual:
        format_dict[col] = lambda x: formatar_percentual(x)

    styled_df = df.style.format(format_dict)
    
    if 'profit' in df.columns:
        styled_df = styled_df.applymap(lambda v: 'color: red' if v < 0 else 'color: green', subset=['profit'])
    if 'profitMargin' in df.columns:
         styled_df = styled_df.applymap(lambda v: 'color: red' if v < 0 else 'color: green', subset=['profitMargin'])

    return styled_df

# --- TÍTULO ---
st.title("Dashboard Interativo da Superstore")
st.markdown("Uma análise visual dos principais insights do relatório, agora construída com Python, Streamlit e Plotly.")

# --- ABAS DE NAVEGAÇÃO ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Visão Geral", "Produtos", "Geográfica", "Clientes", "Descontos", "Envio", "Recomendações"
])

# --- ABA 1: VISÃO GERAL ---
with tab1:
    st.header("Visão Geral do Desempenho")
    st.markdown("""
    Esta seção apresenta os indicadores chave de desempenho (KPIs) da Superstore, incluindo vendas totais, 
    lucro total e margem de lucro geral. Além disso, exploramos as tendências de vendas e lucro ao longo dos anos.
    """)
    
    # KPIs
    kpi_data = superstore_data['visaoGeral']
    col1, col2, col3 = st.columns(3)
    col1.metric("Vendas Totais", formatar_numero(kpi_data['totalSales']))
    col2.metric("Lucro Total", formatar_numero(kpi_data['totalProfit']))
    col3.metric("Margem de Lucro Geral", formatar_percentual(kpi_data['overallProfitMargin']))

    st.markdown("---")
    
    # Gráfico de Desempenho Anual
    st.subheader("Desempenho Anual")
    yearly_df = kpi_data['yearlyPerformance']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=yearly_df['Ano'], y=yearly_df['Vendas'], mode='lines+markers', name='Vendas'))
    fig.add_trace(go.Scatter(x=yearly_df['Ano'], y=yearly_df['Lucro'], mode='lines+markers', name='Lucro'))
    
    fig.update_layout(title="Vendas e Lucro por Ano", xaxis_title="Ano", yaxis_title="Valor (R$)")
    st.plotly_chart(fig, use_container_width=True)


# --- ABA 2: PRODUTOS ---
with tab2:
    st.header("Desempenho de Produtos")
    st.markdown("""
    Analisamos o desempenho de vendas e lucratividade por categoria e subcategoria de produtos. 
    O objetivo é identificar quais produtos são os mais rentáveis e quais podem estar impactando negativamente a lucratividade.
    """)
    
    produtos_data = superstore_data['produtos']
    
    # Gráfico de Desempenho por Categoria
    st.subheader("Desempenho por Categoria")
    category_df = produtos_data['categoryPerformance']
    fig = px.bar(category_df, x='category', y=['sales', 'profit'], barmode='group',
                 labels={'value': 'Valor (R$)', 'category': 'Categoria'},
                 title="Vendas vs. Lucro por Categoria",
                 color_discrete_map={'sales': '#1f77b4', 'profit': '#2ca02c'})
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(estilizar_dataframe(category_df.rename(columns={
        'category': 'Categoria', 'sales': 'Vendas', 'profit': 'Lucro', 'profitMargin': 'Margem Lucro'
    }), ['Vendas', 'Lucro'], ['Margem Lucro']), use_container_width=True)

    st.markdown("---")

    # Gráfico de Lucro por Subcategoria
    st.subheader("Lucro por Subcategoria (Destaques)")
    subcategory_df = produtos_data['subCategoryProfit']
    subcategory_df['Cor'] = ['green' if x > 0 else 'red' for x in subcategory_df['profit']]
    
    fig = px.bar(subcategory_df.sort_values('profit', ascending=True), 
                 x='profit', y='subCategory', orientation='h', 
                 title="Lucro por Subcategoria",
                 labels={'profit': 'Lucro (R$)', 'subCategory': 'Subcategoria'})
    fig.update_traces(marker_color=subcategory_df.sort_values('profit', ascending=True)['Cor'])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Subcategorias com Prejuízo")
    loss_df = produtos_data['lossSubCategoryTable']
    st.dataframe(estilizar_dataframe(loss_df.rename(columns={
        'category': 'Categoria', 'subCategory': 'Subcategoria', 'sales': 'Vendas', 'profit': 'Lucro', 'profitMargin': 'Margem Lucro'
    }), ['Vendas', 'Lucro'], ['Margem Lucro']), use_container_width=True)


# --- ABA 3: GEOGRÁFICA ---
with tab3:
    st.header("Análise Geográfica")
    st.markdown("""
    Esta seção explora o desempenho da Superstore em diferentes regiões e estados, 
    identificando onde a empresa é mais forte e onde existem oportunidades de melhoria.
    """)

    geo_data = superstore_data['geografica']

    # Desempenho por Região
    st.subheader("Desempenho por Região")
    region_df = geo_data['regionPerformance']
    fig = px.bar(region_df, x='region', y=['sales', 'profit'],
                 barmode='group', title="Vendas vs. Lucro por Região",
                 labels={'value': 'Valor (R$)', 'region': 'Região'})
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(estilizar_dataframe(region_df.rename(columns={
        'region': 'Região', 'sales': 'Vendas', 'profit': 'Lucro', 'profitMargin': 'Margem Lucro'
    }), ['Vendas', 'Lucro'], ['Margem Lucro']), use_container_width=True)

    st.markdown("---")

    # Estados com Prejuízo
    st.subheader("Estados com Prejuízo")
    loss_states_df = geo_data['lossStates']
    st.dataframe(estilizar_dataframe(loss_states_df.rename(columns={
        'state': 'Estado', 'sales': 'Vendas', 'profit': 'Lucro', 'profitMargin': 'Margem Lucro'
    }), ['Vendas', 'Lucro'], ['Margem Lucro']), use_container_width=True)
    
# --- ABA 4: CLIENTES ---
with tab4:
    st.header("Análise de Clientes")
    st.markdown("Análise do desempenho com base nos diferentes segmentos de clientes para direcionar estratégias de marketing e vendas.")
    
    clientes_data = superstore_data['clientes']
    segment_df = clientes_data['segmentPerformance']

    # Gráfico de Pizza (Doughnut)
    st.subheader("Distribuição do Lucro por Segmento")
    fig = px.pie(segment_df, names='segment', values='profit', title="Lucro por Segmento de Cliente", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Desempenho Detalhado por Segmento")
    st.dataframe(estilizar_dataframe(segment_df.rename(columns={
        'segment': 'Segmento', 'sales': 'Vendas', 'profit': 'Lucro', 'profitMargin': 'Margem Lucro'
    }), ['Vendas', 'Lucro'], ['Margem Lucro']), use_container_width=True)
    
# --- ABA 5: DESCONTOS ---
with tab5:
    st.header("Impacto dos Descontos")
    st.markdown("""
    Esta seção investiga a relação entre os descontos aplicados e a lucratividade, 
    revelando o impacto de diferentes faixas de desconto na margem de lucro.
    """)

    descontos_data = superstore_data['descontos']
    
    # Matriz de Correlação
    st.subheader("Matriz de Correlação")
    corr_df = descontos_data['correlationMatrix']
    st.dataframe(corr_df.style.background_gradient(cmap='coolwarm', axis=None).format("{:.2f}"))
    
    st.markdown("---")

    # Lucratividade por Faixa de Desconto
    st.subheader("Lucratividade por Faixa de Desconto")
    discount_df = descontos_data['discountImpact']
    discount_df['Cor'] = ['green' if x >= 0 else 'red' for x in discount_df['profitMargin']]
    
    fig = px.bar(discount_df, x='range', y='profitMargin', 
                 title="Margem de Lucro por Faixa de Desconto",
                 labels={'range': 'Faixa de Desconto', 'profitMargin': 'Margem de Lucro (%)'})
    fig.update_traces(marker_color=discount_df['Cor'])
    st.plotly_chart(fig, use_container_width=True)


# --- ABA 6: ENVIO ---
with tab6:
    st.header("Logística de Envio")
    st.markdown("Análise do desempenho dos diferentes modos de envio e o impacto do tempo de envio na operação.")
    
    envio_data = superstore_data['envio']
    ship_mode_df = envio_data['shipModePerformance']

    st.subheader("Desempenho por Modo de Envio")
    st.dataframe(estilizar_dataframe(ship_mode_df.rename(columns={
        'mode': 'Modo de Envio', 'sales': 'Vendas', 'profit': 'Lucro', 'profitMargin': 'Margem Lucro', 'avgTime': 'Tempo Médio (dias)'
    }), ['Vendas', 'Lucro'], ['Margem Lucro']), use_container_width=True)

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    col1.metric("Tempo Médio de Envio Geral", "3.96 dias")
    col2.metric("Mediana do Tempo de Envio", "4.00 dias")


# --- ABA 7: RECOMENDAÇÕES ---
with tab7:
    st.header("Conclusões e Recomendações Estratégicas")
    st.markdown("""
    Com base na análise detalhada dos dados da Superstore, esta seção resume as principais conclusões e 
    sugere ações estratégicas para otimizar o desempenho e aumentar a lucratividade.
    """)
    
    recomendacoes = superstore_data['recomendacoes']
    for rec in recomendacoes:
        st.markdown(f"- {rec}")