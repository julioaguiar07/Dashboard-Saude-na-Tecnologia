import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração do Streamlit (DEVE SER O PRIMEIRO COMANDO)
st.set_page_config(page_title="Saúde Mental na Tecnologia", layout="wide")

# Configuração da paleta de cores
colors = ["#b76435", "#799191", "#f3be72", "#af502b"]

# Carregar os dados (substitua pelo caminho do seu arquivo)
@st.cache_data
def load_data():
    return pd.read_csv("dados_corrigidos (1).csv")

data = load_data()

# Sidebar para filtros
st.sidebar.title("Filtros")

# Filtro de País (permite selecionar um ou todos)
pais_options = ["Todos"] + list(data['Pais'].unique())
pais_selecionado = st.sidebar.selectbox("Selecione o país", options=pais_options)

# Filtro de Idade
idade_min, idade_max = st.sidebar.slider("Selecione a faixa de idade", min_value=int(data['Idade'].min()), max_value=int(data['Idade'].max()), value=(int(data['Idade'].min()), int(data['Idade'].max())))

# Aplicar filtros
if pais_selecionado == "Todos":
    filtered_data = data[data['Idade'].between(idade_min, idade_max)]
else:
    filtered_data = data[(data['Pais'] == pais_selecionado) & (data['Idade'].between(idade_min, idade_max))]

# Página Inicial
st.title("Dashboard de Saúde Mental no Local de Trabalho")
st.write("Explore insights sobre saúde mental no local de trabalho. Use os filtros ao lado para personalizar a análise.")

# Métricas-chave
st.subheader("Métricas-Chave")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de Respostas", len(filtered_data))
with col2:
    st.metric("Buscaram Tratamento", filtered_data['Tratamento'].value_counts().get('Sim', 0))
with col3:
    st.metric("Histórico Familiar", filtered_data['Historico_familiar'].value_counts().get('Sim', 0))
with col4:
    st.metric("Trabalha Remotamente", filtered_data['Trabalho_remoto'].value_counts().get('Sim', 0))

# Gráfico 1: Busca por Tratamento por Gênero
st.subheader("Busca por Tratamento por Gênero")
tratamento_genero = filtered_data.groupby(['Genero', 'Tratamento']).size().unstack().fillna(0)
fig = px.bar(tratamento_genero, x=tratamento_genero.index, y=['Sim', 'Não'], title="Busca por Tratamento por Gênero", barmode='group', color_discrete_sequence=[colors[0], colors[1]])
st.plotly_chart(fig, use_container_width=True)



# Gráfico 3: Interferência no Trabalho
st.subheader("Interferência da Saúde Mental no Trabalho")
interfere_counts = filtered_data['Interfere_no_trabalho'].value_counts()
fig = px.bar(interfere_counts, x=interfere_counts.index, y=interfere_counts.values, title="Interferência no Trabalho", color=interfere_counts.index, color_discrete_sequence=colors)
st.plotly_chart(fig, use_container_width=True)



# Gráfico 5: Consequências de Discutir Saúde Mental
st.subheader("Consequências de Discutir Saúde Mental")
consequencias = filtered_data['Consequencia_saude_mental'].value_counts()
fig = px.bar(consequencias, x=consequencias.index, y=consequencias.values, title="Consequências de Discutir Saúde Mental", color=consequencias.index, color_discrete_sequence=colors)
st.plotly_chart(fig, use_container_width=True)

# Gráfico 6: Saúde Mental vs. Saúde Física
st.subheader("Saúde Mental vs. Saúde Física")
mental_vs_fisica = filtered_data['Mental_vs_fisica'].value_counts()
fig = px.pie(mental_vs_fisica, values=mental_vs_fisica.values, names=mental_vs_fisica.index, title="Saúde Mental vs. Saúde Física", color_discrete_sequence=colors)
st.plotly_chart(fig, use_container_width=True)

# Gráfico 7: Fala sobre Saúde Mental com Colegas e Supervisores por Idade
st.subheader("Fala sobre Saúde Mental com Colegas e Supervisores por Idade")

# Criar faixas etárias
filtered_data['Faixa_Etaria'] = pd.cut(filtered_data['Idade'], bins=range(20, 70, 10), right=False)

# Agrupar dados por faixa etária e contar as respostas para 'Colegas_de_trabalho' e 'Supervisor'
fala_saude_mental = filtered_data.groupby(['Faixa_Etaria', 'Colegas_de_trabalho', 'Supervisor']).size().unstack().fillna(0)

# Resetar o índice para facilitar a manipulação
fala_saude_mental = fala_saude_mental.reset_index()

# Criar o gráfico de barras agrupadas
fig = go.Figure()

# Adicionar barras para 'Colegas_de_trabalho'
fig.add_trace(go.Bar(
    x=fala_saude_mental['Faixa_Etaria'].astype(str),
    y=fala_saude_mental['Sim'],  # Supondo que 'Sim' seja o valor para "Fala com Colegas"
    name='Fala com Colegas'
))

# Adicionar barras para 'Supervisor'
fig.add_trace(go.Bar(
    x=fala_saude_mental['Faixa_Etaria'].astype(str),
    y=fala_saude_mental['Sim'],  # Supondo que 'Sim' seja o valor para "Fala com Supervisor"
    name='Fala com Supervisor'
))

# Atualizar layout do gráfico
fig.update_layout(
    barmode='group',
    title="Fala sobre Saúde Mental com Colegas e Supervisores por Idade",
    xaxis_title="Faixa Etária",
    yaxis_title="Quantidade de Pessoas",
    legend_title="Fala com",
    colorway=colors
)

# Exibir o gráfico
st.plotly_chart(fig, use_container_width=True)

# Estatísticas Descritivas
st.subheader("Estatísticas Descritivas")
st.write(filtered_data[['Idade', 'Genero', 'Pais', 'Tratamento', 'Historico_familiar', 'Interfere_no_trabalho']].describe())


# Rodapé
st.sidebar.markdown("---")
st.sidebar.markdown("Universidade Federal do Ceará")
