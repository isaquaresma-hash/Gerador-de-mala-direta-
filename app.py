import streamlit as st
import pandas as pd
from io import BytesIO
import base64
import re
from openpyxl.styles import PatternFill, Font

# Configuração da página do Streamlit em largura total
st.set_page_config(page_title="Gerador de Mala Direta", layout="wide")

# ==============================================================================
# 🔒 SISTEMA DE AUTENTICAÇÃO E CONTROLE DE ACESSO
# ==============================================================================
USUARIOS_AUTORIZADOS = {
    "sueli.rodrigues@fnp.org.br": "SenhaForte",
    "joao.oliveira@fnp.org.br": "SenhaForte",
    "isa.quaresma@fnp.org.br": "SenhaForte",
    "jailma.sousa@fnp.org.br": "SenhaForte"
}

def validar_login():
    """Valida o e-mail e a senha digitados."""
    usuario = st.session_state.get("input_email", "").strip().lower()
    senha = st.session_state.get("input_password", "")

    if usuario in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[usuario] == senha:
        st.session_state["autenticado"] = True
        st.session_state["usuario_logado"] = usuario
        del st.session_state["input_password"]  # Limpa a senha da memória por segurança
    else:
        st.session_state["autenticado"] = False
        st.error("⚠️ E-mail ou senha incorretos. Acesso negado.")

def tela_login():
    """Desenha o formulário de login centralizado."""
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div style="background-color: #143621; padding: 25px; border-radius: 10px; border: 1px solid #386646; margin-top: 50px;">
            <h2 style="color: white; text-align: center; margin-bottom: 15px;">🔒 Acesso Restrito</h2>
            <p style="color: white; text-align: center; font-size: 14px;">Esta aplicação contém dados sensíveis. Por favor, identifique-se para continuar.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_input("E-mail corporativo:", key="input_email")
        st.text_input("Senha:", type="password", key="input_password")
        st.button("Entrar no Sistema", on_click=validar_login, use_container_width=True)

# Controle de sessão do usuário
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

# Se o usuário não estiver autenticado, encerra a execução aqui
if not st.session_state["autenticado"]:
    tela_login()
    st.stop()

# ==============================================================================
# 🎨 ESTILIZAÇÃO E APLICAÇÃO PRINCIPAL (SÓ CARREGA APÓS LOGIN)
# ==============================================================================

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
            padding-top: 6rem !important;
            padding-bottom: 2rem !important;
        }}

        /* Customização do Título Principal */
        .titulo-personalizado {{
            font-size: 1.8rem !important;
            font-weight: bold;
            color: white !important;
            margin-top: 140px !important;
            margin-bottom: 15px !important;
        }}

        /* Customização para alinhar a área do usuário logado */
        .user-header-box {{
            margin-top: 140px !important;
        }}

        /* Fundo customizado com a LOGO REDUZIDA (background-size: 70% auto) */
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: 70% auto; /* Reduzido de 100% para 70% */
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

        /* Textos e Rótulos gerais */
        .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp label {{
            color: white !important;
        }}

        /* --- CORREÇÃO DO TEXTO DO EXPANDER --- */
        div[data-testid="stExpander"] {{
            background-color: #143621 !important;
            border: 1px solid #386646 !important;
            border-radius: 6px !important;
            color: #ffffff !important;
        }}
        
        div[data-testid="stExpander"] * {{
            color: #ffffff !important;
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

        /* Customização das tags verde escuro */
        span[data-baseweb="tag"],
        div[data-baseweb="tag"],
        span[class*="st-"] {{
            background-color: #2a4e36 !important;
            border: 1px solid #386646 !important;
            border-radius: 4px !important;
        }}
        
        span[data-baseweb="tag"] span,
        div[data-baseweb="tag"] span {{
            color: #ffffff !important;
        }}

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

# Barra Superior com o título ajustado e usuário logado
col_head1, col_head2 = st.columns([8, 2])
with col_head1:
    st.markdown('<div class="titulo-personalizado">📊 Gerador de Mala Direta</div>', unsafe_allow_html=True)
with col_head2:
    st.markdown('<div class="user-header-box">', unsafe_allow_html=True)
    st.write(f"👤 **{st.session_state.get('usuario_logado', '')}**")
    if st.button("🚪 Sair"):
        st.session_state["autenticado"] = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Carregamento do arquivo Excel
@st.cache_data
def carregar_dados():
    return pd.read_excel("sua_planilha.xlsx")

try:
    df_original = carregar_dados()
    df_filtrado = df_original.copy()

    # Mapeamento exato pelo nome das colunas na planilha original
    coluna_situacao = "Situação do Município" if "Situação do Município" in df_original.columns else (df_original.columns[2] if len(df_original.columns) > 2 else None)
    coluna_porte = "Tipo" if "Tipo" in df_original.columns else (df_original.columns[1] if len(df_original.columns) > 1 else None)
    coluna_ranking = "Ranking" if "Ranking" in df_original.columns else (df_original.columns[19] if len(df_original.columns) > 19 else None)
    coluna_uf = "UF" if "UF" in df_original.columns else (df_original.columns[6] if len(df_original.columns) > 6 else None)
    coluna_municipio = "Muncípio" if "Muncípio" in df_original.columns else ("Município" if "Município" in df_original.columns else (df_original.columns[7] if len(df_original.columns) > 7 else None))

    # Tratamento consistente da Coluna Ranking
    def tratar_item_ranking(valor):
        if pd.isna(valor):
            return None
        val_str = str(valor).strip()
        try:
            val_float = float(val_str.replace(',', '.'))
            if 0 < val_float <= 1:
                return f"{int(round(val_float * 100))}%"
            elif val_float > 1:
                return f"{int(round(val_float))}%"
        except ValueError:
            pass
        return val_str.strip()

    def chave_ordenacao_ranking(item):
        m = re.match(r"^(\d+)%$", str(item))
        if m:
            return (0, int(m.group(1)))
        return (1, str(item))

    if coluna_ranking and coluna_ranking in df_original.columns:
        df_original[coluna_ranking] = df_original[coluna_ranking].apply(tratar_item_ranking)
        df_filtrado[coluna_ranking] = df_filtrado[coluna_ranking].apply(tratar_item_ranking)

    # Elimina duplicidades formatando em Title Case
    def obter_opcoes_unicas(df, coluna):
        if not coluna or coluna not in df.columns:
            return ["Selecionar Todos"]
        valores_brutos = df[coluna].dropna().astype(str).str.strip().tolist()
        valores_formatados = sorted(list(set(v.title() for v in valores_brutos if v)))
        return ["Selecionar Todos"] + valores_formatados

    # --- BARRA DE FILTROS (5 COLUNAS SEPARADAS) ---
    st.markdown('<div class="filter-header-badge">🔍 Consulta e Filtros</div>', unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1.2])

    # 1. Situação (Filiação)
    with c1:
        st.markdown('<div class="filter-label-card">1. Situação (Filiação)</div>', unsafe_allow_html=True)
        if coluna_situacao and coluna_situacao in df_original.columns:
            opcoes_sit = obter_opcoes_unicas(df_original, coluna_situacao)
            sel_sit = st.selectbox("Selecione a Situação:", options=opcoes_sit, key="sb_sit")
            if sel_sit != "Selecionar Todos":
                df_filtrado = df_filtrado[df_filtrado[coluna_situacao].astype(str).str.strip().str.upper() == str(sel_sit).strip().upper()]

    # 2. Porte / Tipo (Capitais, etc.)
    with c2:
        st.markdown('<div class="filter-label-card">2. Porte</div>', unsafe_allow_html=True)
        if coluna_porte and coluna_porte in df_original.columns:
            opcoes_porte = obter_opcoes_unicas(df_original, coluna_porte)
            sel_porte = st.selectbox("Selecione o Porte:", options=opcoes_porte, key="sb_porte")
            if sel_porte != "Selecionar Todos":
                df_filtrado = df_filtrado[df_filtrado[coluna_porte].astype(str).str.strip().str.upper() == str(sel_porte).strip().upper()]

    # 3. Ranking
    with c3:
        st.markdown('<div class="filter-label-card">3. Ranking</div>', unsafe_allow_html=True)
        if coluna_ranking and coluna_ranking in df_original.columns:
            valores_ranking = df_original[coluna_ranking].dropna().unique().tolist()
            valores_ordenados = sorted(valores_ranking, key=chave_ordenacao_ranking)
            opcoes_rank = ["Selecionar Todos"] + valores_ordenados
            
            sel_rank = st.selectbox("Selecione o Ranking:", options=opcoes_rank, key="sb_rank")
            if sel_rank != "Selecionar Todos":
                df_filtrado = df_filtrado[df_filtrado[coluna_ranking] == sel_rank]

    # 4. Estado (UF)
    with c4:
        st.markdown('<div class="filter-label-card">4. Estado (UF)</div>', unsafe_allow_html=True)
        if coluna_uf and coluna_uf in df_original.columns:
            opcoes_uf = ["Selecionar Todos"] + sorted(df_original[coluna_uf].dropna().astype(str).str.strip().str.upper().unique().tolist())
            sel_uf = st.selectbox("Selecione a UF:", options=opcoes_uf, key="sb_uf")
            if sel_uf != "Selecionar Todos":
                df_filtrado = df_filtrado[df_filtrado[coluna_uf].astype(str).str.strip().str.upper() == str(sel_uf).strip().upper()]

    # 5. Município
    with c5:
        st.markdown('<div class="filter-label-card">5. Município(s)</div>', unsafe_allow_html=True)
        if coluna_municipio and coluna_municipio in df_original.columns:
            opcoes_mun = ["Selecionar Todos"] + sorted(df_filtrado[coluna_municipio].dropna().astype(str).str.strip().unique().tolist())
            sel_mun = st.selectbox("Escolha o Município:", options=opcoes_mun, key="sb_mun")
            if sel_mun != "Selecionar Todos":
                df_filtrado = df_filtrado[df_filtrado[coluna_municipio].astype(str).str.strip().str.upper() == str(sel_mun).strip().upper()]

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SELEÇÃO DE COLUNAS PARA EXPORTAÇÃO ---
    st.markdown('<div class="filter-header-badge">📋 Seleção de Colunas para Exportação</div>', unsafe_allow_html=True)
    
    # Bloco Informativo dos Tratamentos com texto em branco de alto contraste
    with st.expander("ℹ️ Entenda as colunas de Tratamento (Clique para expandir)"):
        st.markdown("""
        * **Tratamento 1**: Forma de vocativo formal direcionado à autoridade (ex: *Exmo(a). Sr(a).*).
        * **Tratamento 2**: Nome do cargo ou título oficial completo (ex: *Prefeito(a) Municipal*).
        * **Tratamento 3**: Formato de pronome direto/saudação personalizada usada para correspondência da Mala Direta (ex: *Prefeito(a)* / *Senhor(a) Prefeito(a)*).
        """)

    colunas_dos_filtros = [c for c in [coluna_porte, coluna_situacao, coluna_uf, coluna_municipio, coluna_ranking] if c is not None]
    colunas_exportaveis = [col for col in df_original.columns if col not in colunas_dos_filtros]

    if "ms_cols" not in st.session_state:
        st.session_state["ms_cols"] = colunas_exportaveis

    btn_col1, btn_col2, _ = st.columns([1.5, 1.5, 5])

    with btn_col1:
        if st.button("Marcar Todas"):
            st.session_state["ms_cols"] = colunas_exportaveis
            st.rerun()

    with btn_col2:
        if st.button("Desmarcar Todas"):
            st.session_state["ms_cols"] = []
            st.rerun()

    colunas_selecionadas = st.multiselect(
        "Escolha as colunas desejadas para compor o Excel:",
        options=colunas_exportaveis,
        key="ms_cols"
    )

    colunas_identificacao = [c for c in [coluna_porte, coluna_situacao, coluna_uf, coluna_municipio, coluna_ranking] if c in df_original.columns]
    colunas_finais_ordenadas = [col for col in df_original.columns if (col in colunas_identificacao or col in colunas_selecionadas)]

    if colunas_finais_ordenadas:
        df_exportar = df_filtrado[colunas_finais_ordenadas]

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_exportar.to_excel(writer, index=False, sheet_name='Mala Direta')
            
            # Formatação visual do Excel gerado
            workbook = writer.book
            worksheet = writer.sheets['Mala Direta']
            
            header_fill = PatternFill(start_color="143621", end_color="143621", fill_type="solid")
            header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
            
            for col_num, col_name in enumerate(colunas_finais_ordenadas, 1):
                cell = worksheet.cell(row=1, column=col_num)
                cell.fill = header_fill
                cell.font = header_font
        
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
    st.error(f"Erro ao processar a planilha. Verifique o arquivo Excel enviado. Detalhes: {e}")
