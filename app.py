import streamlit as st
import pandas as pd
from io import BytesIO
import base64

# Configuração da página do Streamlit em largura total
st.set_page_config(page_title="Gerador de Mala Direta", layout="wide")

# Função para aplicar a imagem de fundo e estilizar a interface
def carregar_configuracao_estilo(caminho_imagem):
    try:
        with open(caminho_imagem, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        css_fundo_e_texto = f"""
        <style>
        /* Header transparente */
        header[data-testid="stHeader"] {{
            background-color: transparent !important;
            z-index: 1;
        }}
        
        /* Espaçamento do topo */
        .block-container {{
            padding-top: 10rem !important;
            padding-bottom: 2rem !important;
        }}

        /* Fundo customizado */
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: 100% auto;
            background-position: top center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-color: #1a3323;
        }}

        /* Badges de Título */
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

        /* Etiqueta dos Filtros */
        .filter-label-card {{
            background-color: #2a4e36;
            color: #ffffff !important;
            padding: 6px 12px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 0px;
            border: 1px solid #386646;
        }}

        /* Textos e Rótulos */
        .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp label {{
            color: white !important;
        }}

        /* Botões com texto visível */
        .stButton > button {{
            background-color: #2a4e36 !important;
            color: #ffffff !important;
            border: 1px solid #386646 !important;
            border-radius: 6px !important;
            font-weight: bold !important;
            padding: 0.4rem 1rem !important;
        }}
        
        .stButton > button:hover {{
            background-color: #143621 !important;
            color: #ffffff !important;
            border-color: #ffffff !important;
        }}

        /* Força texto escuro e legível dentro das caixas de seleção */
        .stMultiSelect, .stSelectbox {{
            color: #000000 !important;
        }}
        
        div[data-baseweb="select"] span {{
            color: #000000 !important;
        }}

        /* Botão de Download */
        div.stDownloadButton > button {{
            margin-top: 1rem;
            padding: 0.6rem 1.5rem !important;
            font-size: 1rem !important;
            font-weight: bold !important;
            background-color: #2a4e36 !important;
            color: #ffffff !important;
            border: 1px solid #386646 !important;
            border-radius: 6px !important;
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

# Aplica o estilo e fundo
carregar_configuracao_estilo("fundo do maleiro.png")

st.title("📊 Gerador de Mala Direta")

# Carregamento do arquivo Excel
@st.cache_data
def carregar_dados():
    return pd.read_excel("sua_planilha.xlsx")

try:
    df_original = carregar_dados()
    df_filtrado = df_original.copy()

    # Mapeamento pelas Posições Exatas das Colunas na Planilha (A=0, B=1, C=2, G=6, H=7)
    coluna_porte = df_original.columns[1] if len(df_original.columns) > 1 else None       # Coluna B: Tipo / Porte
    coluna_situacao = df_original.columns[2] if len(df_original.columns) > 2 else None    # Coluna C: Situação / Filiação
    coluna_uf = df_original.columns[6] if len(df_original.columns) > 6 else None          # Coluna G: UF / Estado
    coluna_municipio = df_original.columns[7] if len(df_original.columns) > 7 else None   # Coluna H: Município

    # --- BARRA DE FILTROS (4 COLUNAS SEPARADAS) ---
    st.markdown('<div class="filter-header-badge">🔍 Consulta e Filtros</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([1, 1, 1, 1.5])

    # 1. Situação / Filiação (Coluna C)
    with c1:
        st.markdown('<div class="filter-label-card">1. Situação (Filiação)</div>', unsafe_allow_html=True)
        if coluna_situacao:
            opcoes_sit = ["Selecionar Todos"] + sorted(df_original[coluna_situacao].dropna().astype(str).unique().tolist())
            sel_sit = st.selectbox("Selecione a Situação:", options=opcoes_sit, key="sb_sit")
            if sel_sit != "Selecionar Todos":
                df_filtrado = df_filtrado[df_filtrado[coluna_situacao].astype(str) == sel_sit]

    # 2. Porte (Coluna B)
    with c2:
        st.markdown('<div class="filter-label-card">2. Porte</div>', unsafe_allow_html=True)
        if coluna_porte:
            opcoes_porte = ["Selecionar Todos"] + sorted(df_filtrado[coluna_porte].dropna().astype(str).unique().tolist())
            sel_porte = st.selectbox("Selecione o Porte:", options=opcoes_porte, key="sb_porte")
            if sel_porte != "Selecionar Todos":
                df_filtrado = df_filtrado[df_filtrado[coluna_porte].astype(str) == sel_porte]

    # 3. Estado / UF (Coluna G)
    with c3:
        st.markdown('<div class="filter-label-card">3. Estado (UF)</div>', unsafe_allow_html=True)
        if coluna_uf:
            opcoes_uf = ["Selecionar Todos"] + sorted(df_filtrado[coluna_uf].dropna().astype(str).unique().tolist())
            sel_uf = st.selectbox("Selecione a UF:", options=opcoes_uf, key="sb_uf")
            if sel_uf != "Selecionar Todos":
                df_filtrado = df_filtrado[df_filtrado[coluna_uf].astype(str) == sel_uf]

    # 4. Município(s) (Coluna H)
    with c4:
        st.markdown('<div class="filter-label-card">4. Município(s)</div>', unsafe_allow_html=True)
        if coluna_municipio:
            opcoes_mun = ["Selecionar Todos"] + sorted(df_filtrado[coluna_municipio].dropna().astype(str).unique().tolist())
            sel_mun = st.selectbox("Escolha o Município:", options=opcoes_mun, key="sb_mun")
            if sel_mun != "Selecionar Todos":
                df_filtrado = df_filtrado[df_filtrado[coluna_municipio].astype(str) == sel_mun]

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SELEÇÃO DE COLUNAS PARA EXPORTAÇÃO ---
    st.markdown('<div class="filter-header-badge">📋 Seleção de Colunas para Exportação</div>', unsafe_allow_html=True)
    
    colunas_disponiveis = df_original.columns.tolist()

    # Botões de marcação rápida
    btn_col1, btn_col2, _ = st.columns([1.5, 1.5, 5])
    
    if "cols_selected" not in st.session_state:
        st.session_state["cols_selected"] = colunas_disponiveis

    with btn_col1:
        if st.button("Marcar Todas"):
            st.session_state["cols_selected"] = colunas_disponiveis
            st.rerun()

    with btn_col2:
        if st.button("Desmarcar Todas"):
            st.session_state["cols_selected"] = []
            st.rerun()

    colunas_selecionadas = st.multiselect(
        "Escolha as colunas desejadas para compor o Excel:",
        options=colunas_disponiveis,
        default=st.session_state["cols_selected"],
        key="ms_cols"
    )

    if colunas_selecionadas:
        df_exportar = df_filtrado[colunas_selecionadas]

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_exportar.to_excel(writer, index=False, sheet_name='Mala Direta')
        
        st.write(f"📊 Registros encontrados com os filtros atuais: **{len(df_exportar)}**")
        
        st.download_button(
            label="📥 Baixar Mala Direta (.xlsx)",
            data=buffer.getvalue(),
            file_name="mala_direta_personalizada.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("Selecione ao menos uma coluna no campo acima para habilitar o download.")

except Exception as e:
    st.error(f"Erro ao carregar a planilha. Certifique-se de que o arquivo Excel enviado para o GitHub tem o mesmo nome configurado no código. Detalhes: {e}")
