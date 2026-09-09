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
            padding-top: 8rem !important;
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

        /* Estilo das Tags do MultiSelect (Verde) */
        span[data-baseweb="tag"],
        div[data-baseweb="tag"],
        span[class*="st-"] {{
            background-color: #2a4e36 !important;
            border: 1px solid #386646 !important;
            border-radius: 4px !important;
        }}
        
        /* Cor do texto interno das tags */
        span[data-baseweb="tag"] span,
        div[data-baseweb="tag"] span {{
            color: #ffffff !important;
        }}

        /* Ícone 'x' para remover a tag */
        span[data-baseweb="tag"] svg,
        div[data-baseweb="tag"] svg {{
            fill: #ffffff !important;
            color: #ffffff !important;
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

    # --- SELEÇÃO DE COLUNAS PARA EXPORTAÇÃO ---
    st.markdown('<div class="filter-header-badge">📋 Seleção de Colunas para Compor o Excel</div>', unsafe_allow_html=True)
    
    # Lista das colunas que devem ser removidas da seleção
    colunas_remover = ["Situação do Município", "Tipo", "UF", "Muncípio", "Ranking"]
    
    # Filtra as colunas disponíveis ignorando as colunas especificadas
    colunas_disponiveis = [col for col in df_original.columns if col.strip() not in colunas_remover and col != "_ranking_tratado"]

    if "cols_selected" not in st.session_state:
        st.session_state["cols_selected"] = colunas_disponiveis

    # Botões de marcação rápida
    btn_col1, btn_col2, _ = st.columns([1.5, 1.5, 5])

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
        df_exportar = df_original[colunas_selecionadas]

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_exportar.to_excel(writer, index=False, sheet_name='Mala Direta')
        
        st.write(f"📊 Linhas que serão exportadas: **{len(df_exportar)}** | Colunas selecionadas: **{len(colunas_selecionadas)}**")
        
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
