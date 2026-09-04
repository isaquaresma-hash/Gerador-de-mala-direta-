import streamlit as st
import pandas as pd
from io import BytesIO
import base64

st.set_page_config(page_title="Gerador de Mala Direta", layout="wide")

# Função para converter a imagem local/GitHub em Base64 para usar no CSS
def carregar_imagem_fundo(caminho_imagem):
    try:
        with open(caminho_imagem, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        css_fundo = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(css_fundo, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Não foi possível carregar a imagem de fundo: {e}")

# Aplica o fundo com a imagem 'fundo do maleiro.png'
carregar_imagem_fundo("fundo do maleiro.png")

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

        st.subheader("Pré-visualização dos Dados:")
        st.dataframe(df_filtrado.head(10), use_container_width=True)

        # 3. Prepara o arquivo Excel para download
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
