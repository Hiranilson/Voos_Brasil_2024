import streamlit as st
import networkx as nx
import pandas as pd
import numpy as np
from pyvis.network import Network
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import community as community_louvain  # python-louvain

# Configuração da página
st.set_page_config(page_title="Rede de Voos 2024", layout="wide")
st.title("✈️ Análise Interativa da Rede de Voos no Brasil (2024)")

# === Carregamento da rede ===
G = nx.read_gpickle("rede_voos_brasil_2024.gpickle")
pos = nx.get_node_attributes(G, 'pos')

# === Comunidades Louvain ===
partition = community_louvain.best_partition(G)
nx.set_node_attributes(G, partition, 'comunidade')
lista_comunidades = sorted(set(partition.values()))

# === Sidebar com filtros ===
aba = st.sidebar.radio("Visualização:", [
    "🔗 Pyvis", 
    "🗽 Mapa Interativo", 
    "📊 Análise da Sub-Rede Filtrada"
])

tipo_voo_selecionado = st.sidebar.selectbox(
    "Tipo de Voo:",
    ["Todos", "Nacional", "Internacional"]
)

comunidade_selecionada = st.sidebar.selectbox(
    "Comunidade Louvain:",
    ["Todas"] + lista_comunidades
)

# === Gera sub-rede com base nos filtros ===
if comunidade_selecionada == "Todas":
    nos_filtrados = list(G.nodes)
else:
    nos_filtrados = [n for n, d in G.nodes(data=True) if d.get('comunidade') == comunidade_selecionada]

arestas_filtradas = []
for u, v, d in G.edges(data=True):
    if u in nos_filtrados and v in nos_filtrados:
        tipo = d.get('tipo', 'Nacional')
        if tipo_voo_selecionado == "Todos" or tipo == tipo_voo_selecionado:
            arestas_filtradas.append((u, v))

G_sub = G.edge_subgraph(arestas_filtradas).copy()

# === Aba Pyvis ===
if aba == "🔗 Pyvis":
    st.markdown("#### Visualização da Rede com Pyvis")
    net = Network(height="700px", width="100%", bgcolor="#ffffff", font_color="black")
    net.from_nx(G_sub)
    for node in net.nodes:
        cidade = node['id']
        com = G.nodes[cidade].get('comunidade', 'N/A')
        node['title'] = f"{cidade}<br>Comunidade: {com}"
        node['color'] = f"hsl({com * 35 % 360}, 70%, 65%)"
    net.save_graph("pyvis_rede_voos.html")
    with open("pyvis_rede_voos.html", "r", encoding="utf-8") as f:
        html = f.read()
        components.html(html, height=750, scrolling=True)

# === Aba Mapa Plotly ===
elif aba == "🗽 Mapa Interativo":
    st.markdown("#### Mapa Interativo com Plotly")
    edge_traces = []
    for u, v in G_sub.edges():
        if u in pos and v in pos:
            tipo = G.edges[u, v].get('tipo', 'Nacional')
            cor = 'blue' if tipo == 'Nacional' else 'green'
            lon1, lat1 = pos[u]
            lon2, lat2 = pos[v]
            edge_traces.append(go.Scattergeo(
                lon=[lon1, lon2, None],
                lat=[lat1, lat2, None],
                mode='lines',
                line=dict(width=1, color=cor),
                hoverinfo='text',
                text=f'{u} → {v} ({tipo})',
                showlegend=False
            ))
    edge_traces.append(go.Scattergeo(lon=[None], lat=[None], mode='lines', line=dict(width=2, color='blue'), name='Voo Nacional'))
    edge_traces.append(go.Scattergeo(lon=[None], lat=[None], mode='lines', line=dict(width=2, color='green'), name='Voo Internacional'))

    cidades = list(G_sub.nodes())
    graus = np.array([G_sub.degree(n) for n in cidades])
    if graus.ptp() == 0:
        graus_normalizados = np.full_like(graus, 10)
    else:
        graus_normalizados = 5 + 20 * (graus - graus.min()) / (graus.max() - graus.min())

    centrality = nx.degree_centrality(G_sub)
    centrality_values = [centrality.get(c, 0) for c in cidades]
    node_trace = go.Scattergeo(
        lon=[pos[c][0] for c in cidades],
        lat=[pos[c][1] for c in cidades],
        text=cidades,
        hovertext=[f"{c}<br>Degree: {G_sub.degree(c)}<br>Centralidade: {centrality.get(c):.3f}" for c in cidades],
        mode='markers+text',
        marker=dict(
            size=graus_normalizados.tolist(),
            color=centrality_values,
            colorscale='YlOrRd',
            colorbar=dict(title='Centralidade', x=0.92, len=0.5),
            line=dict(width=0.5, color='black')
        ),
        textposition='top center',
        hoverinfo='text',
        name='Cidades'
    )

    fig = go.Figure(data=edge_traces + [node_trace])
    fig.update_layout(
        title=dict(text='Rede de Voos do Brasil em 2024', x=0.5, font=dict(size=24)),
        geo=dict(projection_type='equirectangular', showland=True, landcolor='rgb(217, 217, 217)', oceancolor='rgb(150, 200, 255)', lakecolor='rgb(255, 255, 255)', showocean=True, showcountries=True, countrycolor="RebeccaPurple"),
        showlegend=True,
        height=800,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

# === Aba Análise Estrutural ===
elif aba == "📊 Análise da Sub-Rede Filtrada":
    st.header("📊 Métricas Estruturais da Sub-Rede Filtrada")

    col1, col2, col3 = st.columns(3)
    with col1:
        densidade = nx.density(G_sub)
        st.metric("Densidade", f"{densidade:.4f}")
    with col2:
        assort = nx.degree_assortativity_coefficient(G_sub)
        st.metric("Assortatividade", f"{assort:.4f}")
    with col3:
        clustering = nx.average_clustering(G_sub)
        st.metric("Clustering", f"{clustering:.4f}")

    col4, col5 = st.columns(2)
    with col4:
        scc = nx.number_strongly_connected_components(G_sub) if G_sub.is_directed() else "-"
        st.metric("Componentes Fortemente Conectados", scc)
    with col5:
        wcc = nx.number_connected_components(G_sub) if not G_sub.is_directed() else "-"
        st.metric("Componentes Fracamente Conectados", wcc)

    # Histograma de Grau
    st.subheader("🎯 Distribuição de Grau dos Nós")
    graus = [G_sub.degree(n) for n in G_sub.nodes()]
    fig_grau, ax = plt.subplots()
    ax.hist(graus, bins=20, color='skyblue', edgecolor='black')
    ax.set_title("Distribuição de Grau dos Nós")
    ax.set_xlabel("Grau")
    ax.set_ylabel("Frequência")
    st.pyplot(fig_grau)

    # Centralidade
    st.subheader("🏆 Centralidade dos Nós")
    metrica = st.selectbox("Selecione a Métrica de Centralidade", ["Degree", "Closeness", "Betweenness", "Eigenvector"])

    if metrica == "Degree":
        centralidade = nx.degree_centrality(G_sub)
    elif metrica == "Closeness":
        centralidade = nx.closeness_centrality(G_sub)
    elif metrica == "Betweenness":
        centralidade = nx.betweenness_centrality(G_sub)
    elif metrica == "Eigenvector":
        try:
            centralidade = nx.eigenvector_centrality(G_sub)
        except nx.NetworkXException:
            st.error("Erro: A sub-rede atual não permite cálculo de centralidade por autovetor.")
            centralidade = {}

    if centralidade:
        df_cent = pd.DataFrame(centralidade.items(), columns=["Nó", metrica])
        df_cent = df_cent.sort_values(by=metrica, ascending=False).reset_index(drop=True)
        st.dataframe(df_cent, height=300)

        fig_cent = go.Figure(go.Bar(
            x=df_cent["Nó"][:10],
            y=df_cent[metrica][:10],
            marker_color='royalblue'
        ))
        fig_cent.update_layout(title=f"Top 10 Nós por {metrica}", height=400)
        st.plotly_chart(fig_cent, use_container_width=True)