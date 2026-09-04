import streamlit as st
import pandas as pd
from io import BytesIO
import base64

# Configuração da página do Streamlit
st.set_page_config(page_title="Gerador de Mala Direta", layout="wide")

# Função para aplicar a imagem de fundo sem cortar o topo e ajustar cores dos textos
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
        
        /* Ajusta o espaçamento do topo para o conteúdo subir */
        .block-container {{
            padding-top: 2rem !important;
        }}

        /* Fixa a imagem no topo sem cortar a logo */
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: 100% auto;
            background-position: top center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-color: #1a3323; /* Cor de fundo complementar caso role a página */
        }}

        /* Força a cor branca nos textos principais para dar contraste */
        .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp label {{
            color: white !important;
        }}

        /* Mantém o texto das opções de seleção visível/escuro */
        .stApp .stMultiSelect {{
            color: initial !important;
        }}
        </style>
        """
        st.markdown(css_fundo_e_texto, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Não foi possível carregar o estilo de fundo: {e}")

# Aplica a imagem de fundo do seu repositório
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
    st.error(f"Erro ao carregar a planilha. Certifique-se de que o arquivo Excel enviado para o GitHub tem o mesmo nome configurado na linha 53 do código. Detalhes: {e}")
