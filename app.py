import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Gerador de Mala Direta", layout="wide")

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
