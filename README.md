# ✈️ Análise de Rede dos Voos Realizados no Brasil em 2024

Este projeto implementa uma aplicação interativa para **análise da malha aérea brasileira em 2024**, utilizando grafos para representar as conexões entre cidades por voos nacionais e internacionais. O repositório combina uma aplicação interativa em Streamlit com um notebook de análise exploratória e visualização de rede, ambos baseados em dados reais da ANAC, OpenFlights e GeoNames.

A rede foi construída a partir de dados de voos realizados, com nós representando cidades e arestas representando rotas aéreas. O aplicativo permite visualização, filtragem por tipo de voo e comunidade Louvain, além da análise de métricas estruturais da sub-rede selecionada.

A interface foi desenvolvida com **Streamlit**, utilizando visualização geográfica em **Plotly**.

---

## 🌍 Aplicação Interativa

A aplicação foi desenvolvida com Streamlit e permite explorar a rede de voos por meio de um mapa geográfico interativo (Plotly) com filtros por tipo de voo e por comunidades detectadas com Louvain.

✅  [Acesse a aplicação online](https://voosbrasil2024-m4xvzmdkaepgwukvnljy2d.streamlit.app/)

---

## 📓 Análise Exploratória no Notebook

O notebook `Analise_de_Redes_AV3.ipynb` contém uma análise técnica detalhada da rede, dividida em:

### 1. 📥 Importação e Processamento de Dados
- Concatenação de arquivos da ANAC com voos realizados em 2024.
- Enriquecimento com informações geográficas (OurAirports + GeoNames).
- Correções manuais em ICAOs e coordenadas não reconhecidas.

### 2. 🌐 Construção do Grafo
- Grafo direcionado com NetworkX.
- Nós: cidades; Arestas: rotas aéreas; Peso: quantidade de voos.
- Inclusão de atributos geográficos e tipo de voo (nacional/internacional).

### 3. 📊 Análise Estrutural
- Número de nós e arestas.
- Matriz de adjacência.
- Densidade e esparsidade.
- Diâmetro e periferia da rede.
- Componentes fortemente e fracamente conectados.
- Coeficiente de assortatividade.
- Clustering global e local.

### 4. 🧠 Centralidades
- Grau (Degree)
- Proximidade (Closeness)
- Intermediação (Betweenness)
- Autovetor (Eigenvector)
- Visualização com histograma de graus.

### 5. 🧩 Detecção de Comunidades
- Algoritmo de Louvain aplicado à versão não-direcionada da rede.
- Atribuição de cores às comunidades detectadas.
- Salvamento em `comunidades_louvain.pkl`.

### 6. 🌍 Visualizações
- **Pyvis**: grafo interativo com painel de física e métricas nos nós.
- **Cartopy**: rede plotada sobre mapa global com long/lat.
- **Plotly (ScatterGeo)**:
  - Diferenciação visual de voos nacionais e internacionais por cor.
  - Tamanho proporcional ao grau.
  - Cor relacionada à centralidade.
  - Hover com grau e centralidade por cidade.

---

## 🧪 Tecnologias Utilizadas

- Python 3
- Pandas, Numpy
- NetworkX, Python-Louvain
- Matplotlib, Seaborn
- Plotly, Pyvis, Cartopy
- GeoNames, OurAirports

---

## 📁 Estrutura do Projeto

```
📦 Voos_Brasil_2024
┣ 📜 Analise_de_Redes_AV3.ipynb       ← Notebook com uma análise exploratória e estrutural da rede
┣ 📜 app.py                           ← Aplicação interativa com Streamlit
┣ 📜 comunidades_louvain.pkl          ← Partições Louvain serializadas
┣ 📜 rede_voos_brasil_2024.gpickle    ← Grafo direcionado com atributos geográficos
┣ 📜 requirements.txt                 ← Dependências do projeto
┗ 📜 README.md                        ← Este documento
```

---

## 💻 Como executar localmente

1. Clone o repositório:

```bash
git clone https://github.com/Hiranilson/Voos_Brasil_2024.git
cd rede-voos-2024
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   
```
python3 -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

3. Instale as dependências:
   
```
pip install -r requirements.txt
```

4. Execute a aplicação:
   
```
streamlit run app.py
```

5. Acesse no navegador:
   
```
http://localhost:8501
```

---

## 👨‍🏫 Sobre o Projeto

Este projeto foi desenvolvido por Hiranilson Andrade como parte da 3ª Avaliação da disciplina de Análise de Redes. Ele integra aspectos computacionais, geográficos e teóricos da Análise de Redes Complexas aplicados à malha aérea brasileira de 2024.
