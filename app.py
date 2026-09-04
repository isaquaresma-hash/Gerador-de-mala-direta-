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
        .stApp .stMultiSelect {{
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
    # Substitua pelo nome exato do seu arquivo Excel no GitHub
    return pd.read_excel("sua_planilha.xlsx")

try:
    df = carregar_dados()
    st.success("Banco de dados carregado com sucesso!")

    # 2. Transforma as colunas da planilha em opções de seleção
    colunas_disponiveis = df.columns.tolist()
    
    st.subheader("Selecione as informações desejadas:")
    colunas_selecionadas = st.multiselect(
        "Escolha as colunas para compor a nova planilha:",
        options=colunas_disponiveis,
        default=colunas_disponiveis
    )

    if colunas_selecionadas:
        # Filtra a planilha base com as colunas escolhidas
        df_filtrado = df[colunas_selecionadas]

        # 3. Prepara o arquivo Excel para download direto (sem pré-visualização)
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_filtrado.to_excel(writer, index=False, sheet_name='Mala Direta')
        
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
