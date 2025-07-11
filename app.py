import streamlit as st
import networkx as nx
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pickle
import community as community_louvain

# --- Configuração da página ---
st.set_page_config(page_title="Rede de Voos 2024", layout="wide")
st.title("✈️ Mapa Interativo da Rede de Voos no Brasil (2024)")

# === Carregamento da rede ===
@st.cache_data
def carregar_grafo(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

G = carregar_grafo("rede_voos_brasil_2024.gpickle")
pos = nx.get_node_attributes(G, 'pos')

# === Comunidades Louvain ===
partition = community_louvain.best_partition(G.to_undirected())
nx.set_node_attributes(G, partition, 'comunidade')
lista_comunidades = sorted(set(partition.values()))

# === Sidebar ===
st.sidebar.markdown("### Filtros")
tipo_voo = st.sidebar.selectbox("Tipo de Voo:", ["Todos", "Nacional", "Internacional"])
comunidade = st.sidebar.selectbox("Comunidade Louvain:", ["Todas"] + lista_comunidades)

# === Filtragem de arestas ===
arestas_visiveis = []
for u, v, d in G.edges(data=True):
    tipo = d.get("tipo", "Nacional")
    mesma_comunidade = (partition.get(u) == partition.get(v))

    if tipo_voo != "Todos" and tipo != tipo_voo:
        continue
    if comunidade != "Todas" and not mesma_comunidade:
        continue
    if comunidade != "Todas" and partition.get(u) != comunidade:
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
if graus_arr.ptp() == 0:
    tamanhos = np.full_like(graus_arr, 10)
else:
    tamanhos = 5 + 20 * (graus_arr - graus_arr.min()) / (graus_arr.max() - graus_arr.min())

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
    title=dict(text='Rede de Voos do Brasil em 2024', x=0.5, font=dict(size=24)),
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