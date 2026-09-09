import streamlit as st
import pandas as pd
from io import BytesIO
import base64

# Configuração da página do Streamlit em largura total
st.set_page_config(page_title="Gerador de Mala Direta", layout="wide")

# Função para aplicar a imagem de fundo e ajustar os espaçamentos/estilos compactos
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
        
        /* Ajusta o topo do contêiner principal mantendo a largura total */
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

        /* Força a cor branca nos textos principais */
        .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp label {{
            color: white !important;
        }}

        /* Compacta fontes e espaçamentos das seções */
        .stApp h3 {{
            font-size: 1.2rem !important;
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }}

        /* Compacta as caixas de aviso/sucesso */
        div[data-testid="stAlert"] {{
            padding: 0.5rem 1rem !important;
            font-size: 0.9rem !important;
        }}

        /* Mantém o texto dentro do campo de seleção visível/escuro */
        .stApp .stMultiSelect, .stApp .stSelectbox {{
            color: initial !important;
        }}
        
        /* Estilização e espaçamento do botão de download */
        div.stDownloadButton > button {{
            margin-top: 1rem;
            padding: 0.4rem 1rem !important;
            font-size: 0.95rem !important;
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
    # Certifique-se de que o nome da planilha corresponde ao arquivo no seu repositório
    return pd.read_excel("sua_planilha.xlsx")

try:
    df_original = carregar_dados()
    st.success("Banco de dados carregado com sucesso!")

    df_filtrado = df_original.copy()

    # --- BLOCO DE FILTROS ---
    st.subheader("🎯 Filtros de Seleção de Dados")
    col1, col2, col3 = st.columns(3)

    # 1. Filtro de Filiação (ajuste os nomes das colunas conforme sua planilha)
    # Supondo que exista uma coluna 'Filiado' ou 'Situação' (ex: Sim/Não ou Filiado/Não Filiado)
    coluna_filiacao = next((col for col in df_original.columns if "filiad" in col.lower() or "situa" in col.lower()), None)
    
    with col1:
        if coluna_filiacao:
            opcao_filiacao = st.radio(
                "Status de Filiação:",
                options=["Todos", "Filiados", "Não Filiados"]
            )
            if opcao_filiacao == "Filiados":
                # Aceita valores como 'Sim', 'Filiado', True, etc.
                df_filtrado = df_filtrado[df_filtrado[coluna_filiacao].astype(str).str.lower().str.contains("sim|filiado|true|1")]
            elif opcao_filiacao == "Não Filiados":
                df_filtrado = df_filtrado[df_filtrado[coluna_filiacao].astype(str).str.lower().str.contains("não|nao|não filiado|nao filiado|false|0")]
        else:
            st.info("Coluna de filiação não identificada automaticamente.")

    # 2. Filtro de UF (Estado)
    coluna_uf = next((col for col in df_original.columns if col.lower() in ["uf", "estado", "sigla_uf"]), None)
    
    with col2:
        if coluna_uf:
            ufs_disponiveis = sorted(df_filtrado[coluna_uf].dropna().astype(str).unique().tolist())
            ufs_selecionadas = st.multiselect("Selecione a(s) UF(s):", options=ufs_disponiveis)
            if ufs_selecionadas:
                df_filtrado = df_filtrado[df_filtrado[coluna_uf].astype(str).isin(ufs_selecionadas)]

    # 3. Filtro de Município
    coluna_municipio = next((col for col in df_original.columns if "municip" in col.lower() or "cidade" in col.lower()), None)
    
    with col3:
        if coluna_municipio:
            muns_disponiveis = sorted(df_filtrado[coluna_municipio].dropna().astype(str).unique().tolist())
            muns_selecionados = st.multiselect("Selecione o(s) Município(s):", options=muns_disponiveis)
            if muns_selecionados:
                df_filtrado = df_filtrado[df_filtrado[coluna_municipio].astype(str).isin(muns_selecionados)]

    st.markdown("---")

    # --- SELEÇÃO DE COLUNAS ---
    st.subheader("📋 Seleção de Colunas para a Mala Direta")
    colunas_disponiveis = df_original.columns.tolist()
    
    colunas_selecionadas = st.multiselect(
        "Escolha as colunas para compor a nova planilha:",
        options=colunas_disponiveis,
        default=colunas_disponiveis
    )

    if colunas_selecionadas:
        df_exportar = df_filtrado[colunas_selecionadas]

        # 3. Prepara o arquivo Excel para download direto
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
