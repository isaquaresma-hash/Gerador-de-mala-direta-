import streamlit as st
import pandas as pd
from io import BytesIO
import base64

# Configuração da página do Streamlit em largura total
st.set_page_config(page_title="Gerador de Mala Direta", layout="wide")

# Função para aplicar a imagem de fundo e estilizar os blocos no padrão de cores verdes
def carregar_configuracao_estilo(caminho_imagem):
    try:
        with open(caminho_imagem, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        css_fundo_e_texto = f"""
        <style>
        /* Deixa o cabeçalho nativo transparente */
        header[data-testid="stHeader"] {{
            background-color: transparent !important;
            z-index: 1;
        }}
        
        /* Ajusta o topo do contêiner principal para dar espaço à logo */
        .block-container {{
            padding-top: 10rem !important;
            padding-bottom: 2rem !important;
        }}

        /* Fixa a imagem no topo */
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: 100% auto;
            background-position: top center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-color: #1a3323;
        }}

        /* Badge principal: 🔍 Consulta e Filtros (Verde Escuro) */
        .filter-header-badge {{
            background-color: #143621;
            color: #ffffff !important;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 15px;
            display: inline-block;
            margin-bottom: 12px;
            border: 1px solid #235234;
        }}

        /* Etiqueta/Cartão acima de cada filtro (Verde Médio/Militar) */
        .filter-label-card {{
            background-color: #2a4e36;
            color: #ffffff !important;
            padding: 6px 12px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            font-weight: bold;
            font-size: 14px;
            margin-bottom: -1px;
            border: 1px solid #386646;
            border-bottom: none;
        }}

        /* Esconde o label nativo do Streamlit */
        .stApp label {{
            display: none !important;
        }}

        /* Estilização dos seletores acoplados à etiqueta */
        div[data-baseweb="select"] > div {{
            border-top-left-radius: 0px !important;
            border-top-right-radius: 0px !important;
            border-bottom-left-radius: 6px !important;
            border-bottom-right-radius: 6px !important;
            background-color: #f4f6f4 !important;
            border-color: #386646 !important;
        }}

        /* Força textos principais a ficarem brancos */
        .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4 {{
            color: white !important;
        }}

        /* Estilização do botão de download em Verde */
        div.stDownloadButton > button {{
            margin-top: 1.5rem;
            padding: 0.5rem 1.2rem !important;
            font-size: 1rem !important;
            background-color: #2a4e36 !important;
            color: white !important;
            border: 1px solid #386646 !important;
            border-radius: 6px !important;
            transition: all 0.3s ease;
        }}

        div.stDownloadButton > button:hover {{
            background-color: #143621 !important;
            border-color: #ffffff !important;
        }}
        </style>
        """
        st.markdown(css_fundo_e_texto, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Não foi possível carregar o estilo de fundo: {e}")

# Aplica a imagem de fundo do repositório
carregar_configuracao_estilo("fundo do maleiro.png")

# Título da aplicação
st.title("📊 Gerador de Mala Direta")

# 1. Carrega o banco de dados diretamente do repositório
@st.cache_data
def carregar_dados():
    # Substitua pelo nome exato do seu arquivo Excel no GitHub se for diferente
    return pd.read_excel("sua_planilha.xlsx")

try:
    df_original = carregar_dados()
    df_filtrado = df_original.copy()

    # --- BARRA DE CONSULTA E FILTROS EM PALETA VERDE ---
    st.markdown('<div class="filter-header-badge">🔍 Consulta e Filtros</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    # Identificação automática de colunas
    coluna_filiacao = next((col for col in df_original.columns if "filiad" in col.lower() or "situa" in col.lower() or "classific" in col.lower()), None)
    coluna_uf = next((col for col in df_original.columns if col.lower() in ["uf", "estado", "sigla_uf"]), None)
    coluna_municipio = next((col for col in df_original.columns if "municip" in col.lower() or "cidade" in col.lower()), None)
    coluna_porte = next((col for col in df_original.columns if "porte" in col.lower()), None)

    # Bloco 1: Porte (ou Filiação)
    with c1:
        titulo_b1 = "Porte" if coluna_porte else "Filiação"
        st.markdown(f'<div class="filter-label-card">{titulo_b1}</div>', unsafe_allow_html=True)
        col_ref = coluna_porte if coluna_porte else coluna_filiacao
        if col_ref:
            opcoes_b1 = ["-"] + sorted(df_original[col_ref].dropna().astype(str).unique().tolist())
            sel_b1 = st.selectbox("label_b1", options=opcoes_b1, key="sb1")
            if sel_b1 != "-":
                df_filtrado = df_filtrado[df_filtrado[col_ref].astype(str) == sel_b1]

    # Bloco 2: UF
    with c2:
        st.markdown('<div class="filter-label-card">UF</div>', unsafe_allow_html=True)
        if coluna_uf:
            opcoes_uf = ["-"] + sorted(df_filtrado[coluna_uf].dropna().astype(str).unique().tolist())
            sel_uf = st.selectbox("label_uf", options=opcoes_uf, key="sb_uf")
            if sel_uf != "-":
                df_filtrado = df_filtrado[df_filtrado[coluna_uf].astype(str) == sel_uf]

    # Bloco 3: Município
    with c3:
        st.markdown('<div class="filter-label-card">Município</div>', unsafe_allow_html=True)
        if coluna_municipio:
            opcoes_mun = ["-"] + sorted(df_filtrado[coluna_municipio].dropna().astype(str).unique().tolist())
            sel_mun = st.selectbox("label_mun", options=opcoes_mun, key="sb_mun")
            if sel_mun != "-":
                df_filtrado = df_filtrado[df_filtrado[coluna_municipio].astype(str) == sel_mun]

    # Bloco 4: Classificação (ou Filiação)
    with c4:
        st.markdown('<div class="filter-label-card">Classificação</div>', unsafe_allow_html=True)
        if coluna_filiacao and coluna_filiacao != col_ref:
            opcoes_class = ["-"] + sorted(df_filtrado[coluna_filiacao].dropna().astype(str).unique().tolist())
            sel_class = st.selectbox("label_class", options=opcoes_class, key="sb_class")
            if sel_class != "-":
                df_filtrado = df_filtrado[df_filtrado[coluna_filiacao].astype(str) == sel_class]
        else:
            st.selectbox("label_empty", options=["-"], key="sb_empty")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SELEÇÃO DE COLUNAS PARA EXPORTAÇÃO ---
    st.markdown('<div class="filter-label-card" style="border-radius: 6px; display: inline-block;">📋 Seleção de Colunas para a Mala Direta</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    colunas_disponiveis = df_original.columns.tolist()
    colunas_selecionadas = st.multiselect(
        "Escolha as colunas para compor a nova planilha:",
        options=colunas_disponiveis,
        default=colunas_disponiveis
    )

    if colunas_selecionadas:
        df_exportar = df_filtrado[colunas_selecionadas]

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_exportar.to_excel(writer, index=False, sheet_name='Mala Direta')
        
        st.write(f"Total de registros encontrados: **{len(df_exportar)}**")
        st.download_button(
            label="📥 Baixar Mala Direta (.xlsx)",
            data=buffer.getvalue(),
            file_name="mala_direta_personalizada.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("Selecione pelo menos uma coluna para exportar.")

except Exception as e:
    st.error(f"Erro ao carregar a planilha. Certifique-se de que o arquivo Excel enviado para o GitHub tem o mesmo nome configurado no código. Detalhes: {e}")
