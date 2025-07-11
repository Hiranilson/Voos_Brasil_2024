# ✈️ Análise Interativa da Rede de Voos no Brasil (2024)

Este projeto implementa uma aplicação interativa para **análise da malha aérea brasileira em 2024**, utilizando grafos para representar as conexões entre cidades por voos nacionais e internacionais.

A rede foi construída a partir de dados de voos realizados, com nós representando cidades e arestas representando rotas aéreas. O aplicativo permite visualização, filtragem por tipo de voo e comunidade Louvain, além da análise de métricas estruturais da sub-rede selecionada.

A interface foi desenvolvida com **Streamlit**, com visualização geográfica em **Plotly** e topológica com **Pyvis**.

---

## 🔗 Repositório

[GitHub - Hiranilson/rede-voos-2024](https://github.com/Hiranilson/Voos_Brasil_2024)

## 🌍 Aplicação Online (Streamlit Cloud)

✅ Acesse aqui:  
[https://rede-voos-2024.streamlit.app](https://rede-voos-2024.streamlit.app)

---

## 🚀 Funcionalidades

- 🗺️ **Mapa Interativo com Plotly**
  - Visualização geográfica dos voos realizados
  - Nós proporcionais ao grau e coloridos pela centralidade
  - Filtros por tipo de voo e comunidade Louvain

- 🔗 **Visualização com Pyvis**
  - Grafo interativo com física e zoom
  - Tooltip com informações por cidade
  - Cores por comunidade detectada

- 📊 **Análise Estrutural**
  - Densidade da rede
  - Coeficiente de assortatividade
  - Clustering médio
  - Componentes conectados

- 🎯 **Distribuição de Grau**
  - Histograma interativo com `matplotlib`

- 🏆 **Centralidade dos Nós**
  - Degree
  - Closeness
  - Betweenness
  - Eigenvector

---

## 🧠 Tecnologias utilizadas

- Python 3
- Streamlit
- NetworkX
- Plotly
- Pyvis
- Matplotlib
- Pandas
- Python-Louvain

---

## 📁 Estrutura do Projeto

```
📦 rede-voos-2024
┣ 📜 Analise_de_Redes_AV3.ipynb       ← Notebook com uma análise exploratória e estrutural da rede
┣ 📜 app.py                           ← Código principal da aplicação
┣ 📜 rede_voos_brasil_2024.gpickle    ← Grafo salvo com coordenadas e atributos
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
python -m venv venv
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

## ✨ Autor

Desenvolvido por **Hiranilson Andrade**  
Este projeto faz parte da Avaliação 3 da disciplina de **Análise de Redes**.
