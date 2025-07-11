# ✈️ Análise Interativa da Rede de Voos no Brasil (2024)

Este projeto implementa uma aplicação interativa para **análise da malha aérea brasileira em 2024**, utilizando grafos para representar as conexões entre cidades por voos nacionais e internacionais.

A rede foi construída a partir de dados de voos realizados, com nós representando cidades e arestas representando rotas aéreas. O aplicativo permite visualização, filtragem por tipo de voo e comunidade Louvain, além da análise de métricas estruturais da sub-rede selecionada.

A interface foi desenvolvida com **Streamlit**, utilizando visualização geográfica em **Plotly**.

---

## 🔗 Repositório

[GitHub - Hiranilson/Voos_Brasil_2024](https://github.com/Hiranilson/Voos_Brasil_2024)

## 🌍 Aplicação Online (Streamlit Cloud)

✅ Acesse aqui:  
[App](https://voosbrasil2024-m4xvzmdkaepgwukvnljy2d.streamlit.app/)

---

## 🚀 Funcionalidades

- 🗺️ **Mapa Interativo com Plotly**
  - Visualização geográfica dos voos realizados no Brasil
  - Nós proporcionais ao grau e coloridos pela centralidade
  - Filtros por tipo de voo (Nacional/Internacional) e comunidade Louvain

- 📊 **Análise Estrutural**
  - Densidade da rede
  - Coeficiente de assortatividade
  - Clustering médio
  - Componentes conectados

---

## 🧠 Tecnologias utilizadas

- Python 3
- Streamlit
- Networkx
- Plotly
- Pandas
- Numpy
- Python-louvain (community)

---

## 📁 Estrutura do Projeto

```
📦 Voos_Brasil_2024
┣ 📜 Analise_de_Redes_AV3.ipynb       ← Notebook com uma análise exploratória e estrutural da rede
┣ 📜 app.py                           ← Código principal da aplicação Streamlit
┣ 📜 comunidades_louvain.pkl          ← Partição Louvain pré-calculada
┣ 📜 rede_voos_brasil_2024.gpickle    ← Grafo serializado com atributos e coordenadas
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

python -m venv venv
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
Projeto integrante da 3ª Avaliação da disciplina de **Análise de Redes**.
