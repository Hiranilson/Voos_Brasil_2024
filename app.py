import streamlit as st
import networkx as nx
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pickle
import community.community_louvain as community_louvain

# --- Configuração da página ---
st.set_page_config(page_title="Rede de Voos 2024", layout="wide")
st.markdown("<h1 style='text-align: center;'>✈️ Rede de Voos no Brasil (2024)</h1>", unsafe_allow_html=True)

# === Carregamento da rede ===
@st.cache_data
def carregar_grafo(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

G = carregar_grafo("rede_voos_brasil_2024.gpickle")
pos = nx.get_node_attributes(G, 'pos')

# === Comunidades Louvain ===
with open("comunidades_louvain.pkl", "rb") as f:
    partition = pickle.load(f)

nx.set_node_attributes(G, partition, 'comunidade')

# === Sidebar ===
st.sidebar.markdown("### Filtros")
tipo_voo = st.sidebar.selectbox("Tipo de Voo:", ["Todos", "Nacional", "Internacional"])
comunidades_disponiveis = sorted(set(partition.values()))  # garante ordem
comunidade_opcoes = ["Todas"] + [str(c) for c in comunidades_disponiveis]  # todos como string
comunidade = st.sidebar.selectbox("Comunidade Louvain:", comunidade_opcoes)

# Converte a comunidade selecionada para inteiro, se aplicável
if comunidade != "Todas":
    comunidade = int(comunidade)

# === Filtragem de arestas ===
arestas_visiveis = []
for u, v, d in G.edges(data=True):
    tipo = d.get("tipo", "Nacional")
    com_u = partition.get(u)
    com_v = partition.get(v)

    # Aplica o filtro de tipo de voo
    if tipo_voo != "Todos" and tipo != tipo_voo:
        continue

    # Aplica o filtro de comunidade (somente nós da comunidade selecionada)
    if comunidade != "Todas":
        if com_u != comunidade or com_v != comunidade:
            continue

    arestas_visiveis.append((u, v))

# === Construção das linhas das arestas ===
edge_traces = []
for u, v in arestas_visiveis:
    if u in pos and v in pos:
        lon1, lat1 = pos[u]
        lon2, lat2 = pos[v]
        tipo = G.edges[u, v].get('tipo', 'Nacional')
        cor = 'blue' if tipo == 'Nacional' else 'green'
        edge_traces.append(go.Scattergeo(
            lon=[lon1, lon2, None],
            lat=[lat1, lat2, None],
            mode='lines',
            line=dict(width=1, color=cor),
            hoverinfo='text',
            text=f'{u} → {v} ({tipo})',
            showlegend=False
        ))

# Legenda manual
edge_traces += [
    go.Scattergeo(lon=[None], lat=[None], mode='lines', line=dict(width=2, color='blue'), name='Voo Nacional'),
    go.Scattergeo(lon=[None], lat=[None], mode='lines', line=dict(width=2, color='green'), name='Voo Internacional'),
]

# === Nós ===
cidades_visiveis = set([n for u, v in arestas_visiveis for n in (u, v)])
graus = dict(G.degree())
centralidade = nx.degree_centrality(G)

graus_arr = np.array([graus.get(n, 0) for n in cidades_visiveis])
if np.ptp(graus_arr) == 0:
    tamanhos = np.full_like(graus_arr, 10)
else:
    tamanhos = 5 + 20 * (graus_arr - graus_arr.min()) / np.ptp(graus_arr)

trace_nodes = go.Scattergeo(
    lon=[pos[n][0] for n in cidades_visiveis],
    lat=[pos[n][1] for n in cidades_visiveis],
    text=[n for n in cidades_visiveis],
    hovertext=[
        f"{n}<br>Degree: {graus.get(n)}<br>Centralidade: {centralidade.get(n):.3f}<br>Comunidade: {partition.get(n)}"
        for n in cidades_visiveis
    ],
    mode='markers+text',
    marker=dict(
        size=tamanhos.tolist(),
        color=[centralidade[n] for n in cidades_visiveis],
        colorscale='YlOrRd',
        colorbar=dict(title='Centralidade', x=0.92, len=0.5),
        line=dict(width=0.5, color='black')
    ),
    textposition='top center',
    hoverinfo='text',
    name='Cidades'
)

# === Layout ===
fig = go.Figure(data=edge_traces + [trace_nodes])
fig.update_layout(
    geo=dict(
        projection_type='equirectangular',
        showland=True,
        landcolor='rgb(217, 217, 217)',
        oceancolor='rgb(150, 200, 255)',
        lakecolor='rgb(255, 255, 255)',
        showocean=True,
        showcountries=True,
        countrycolor="RebeccaPurple"
    ),
    showlegend=True,
    height=800,
    margin=dict(l=0, r=0, t=50, b=0)
)

# === Exibe no app ===
st.plotly_chart(fig, use_container_width=True)