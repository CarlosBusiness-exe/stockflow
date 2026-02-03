import streamlit as st
import requests
import pandas as pd

# --- CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="StockFlow Pro", layout="wide")

# Corrigindo o contraste das métricas e boxes
st.markdown("""
<style>
    [data-testid="stMetricValue"] {
        background-color: #1E1E1E;
        color: #00FF41; /* Verde Matrix/Tech */
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #333;
    }
    [data-testid="stMetricLabel"] {
        color: #FFFFFF !important;
        font-weight: bold;
    }
    .stTable { background-color: #0E1117; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÕES DE API ---
# Baseado no seu configs.py e api.py
BASE_URL = "http://127.0.0.1:8000/api/v1"

# --- GERENCIAMENTO DE ESTADO (AUTH) ---
if 'token' not in st.session_state:
    st.session_state['token'] = None

def get_headers():
    if st.session_state['token']:
        return {"Authorization": f"Bearer {st.session_state['token']}"}
    return {}

# --- FUNÇÕES DE COMUNICAÇÃO ---
def login(email, password):
    # OAuth2PasswordBearer geralmente espera form-data, não JSON
    payload = {'username': email, 'password': password}
    try:
        response = requests.post(f"{BASE_URL}/users/login", data=payload)
        if response.status_code == 200:
            token = response.json().get("access_token")
            st.session_state['token'] = token
            return True
        return False
    except:
        return False

def api_get(endpoint):
    res = requests.get(f"{BASE_URL}/{endpoint}", headers=get_headers())
    return res.json() if res.status_code == 200 else []

def api_post(endpoint, data):
    return requests.post(f"{BASE_URL}/{endpoint}", json=data, headers=get_headers())

# --- INTERFACE ---
st.sidebar.title("📦 StockFlow")

# Bloco de Login
if not st.session_state['token']:
    st.sidebar.subheader("🔒 Autenticação")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Entrar"):
        if login(email, password):
            st.sidebar.success("Conectado!")
            st.rerun()
        else:
            st.sidebar.error("Falha no login.")
    st.stop() # Interrompe o app se não estiver logado
else:
    if st.sidebar.button("Log out"):
        st.session_state['token'] = None
        st.rerun()

menu = st.sidebar.radio("Navegação", ["Dashboard", "Produtos", "Categorias", "Fornecedores"])

# --- PÁGINA: CATEGORIAS ---
if menu == "Categorias":
    st.title("🏷️ Gestão de Categorias")
    tab1, tab2 = st.tabs(["Listar", "Cadastrar"])

    with tab1:
        categorias = api_get("categories")
        if categorias:
            st.table(categorias)
        else:
            st.info("Nenhuma categoria encontrada.")

    with tab2:
        with st.form("form_cat"):
            name = st.text_input("Nome da Categoria")
            description = st.text_area("Descrição")
            if st.form_submit_button("Salvar Categoria"):
                payload = {"name": name, "description": description}
                res = api_post("categories", payload)
                if res.status_code in [200, 201]:
                    st.success("Categoria cadastrada com sucesso!")
                else:
                    st.error(f"Erro {res.status_code}: {res.text}")

# --- PÁGINA: DASHBOARD ---
elif menu == "Dashboard":
    st.title("📊 Visão Geral")
    produtos = api_get("products")
    
    if produtos:
        df = pd.DataFrame(produtos)
        c1, c2 = st.columns(2)
        c1.metric("Produtos Totais", len(df))
        c2.metric("Valor Total", f"R$ {(df['price'] * df['qtd']).sum():,.2f}")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Sem dados para exibir. Realize o login ou verifique a conexão.")

# --- PÁGINA: PRODUTOS ---
elif menu == "Produtos":
    st.title("📦 Cadastro de Produtos")
    
    # Carregando dependências para os selects
    cats = api_get("categories")
    sups = api_get("suppliers")
    
    if not cats or not sups:
        st.warning("Cadastre categorias e fornecedores antes de criar produtos.")
    else:
        with st.form("form_prod"):
            name = st.text_input("Nome")
            price = st.number_input("Preço", min_value=0.0)
            qtd = st.number_input("Qtd", min_value=0)
            
            # Mapeamento para facilitar a vida do usuário
            cat_name = st.selectbox("Categoria", [c['name'] for c in cats])
            sup_name = st.selectbox("Fornecedor", [s['name'] for s in sups])
            
            cat_id = next(c['id'] for c in cats if c['name'] == cat_name)
            sup_id = next(s['id'] for s in sups if s['name'] == sup_name)

            if st.form_submit_button("Cadastrar"):
                payload = {
                    "name": name, "price": price, "qtd": qtd,
                    "category_id": cat_id, "supplier_id": sup_id
                }
                res = api_post("products", payload)
                if res.status_code == 201:
                    st.success("Produto cadastrado!")
                else:
                    st.error("Erro ao cadastrar.")

# --- PÁGINA: FORNECEDORES ---
elif menu == "Fornecedores":
    st.title("🚚 Gestão de Fornecedores")
    tab1, tab2 = st.tabs(["📋 Listar Fornecedores", "➕ Cadastrar Novo"])

    with tab1:
        st.subheader("Fornecedores Parceiros")
        fornecedores = api_get("suppliers")
        
        if fornecedores:
            df_sup = pd.DataFrame(fornecedores)
            
            # Colunas desejadas sem o campo email
            cols_desejadas = ['id', 'name', 'cnpj', 'address']
            
            # Filtro defensivo: exibe apenas o que existe no banco
            cols_existentes = [c for c in cols_desejadas if c in df_sup.columns]
            
            st.dataframe(df_sup[cols_existentes], use_container_width=True)
        else:
            st.info("Nenhum fornecedor cadastrado no sistema.")

    with tab2:
        st.subheader("Cadastrar Novo Fornecedor")
        with st.form("form_supplier"):
            col_a, col_b = st.columns(2)
            name = col_a.text_input("Nome da Empresa / Razão Social")
            cnpj = col_b.text_input("CNPJ")
            
            # Endereço ocupando a linha inteira para melhor UX de design
            address = st.text_input("Endereço Completo")

            submitted = st.form_submit_button("💾 Salvar Fornecedor")

            if submitted:
                if not name or not cnpj:
                    st.warning("Nome e CNPJ são obrigatórios.")
                else:
                    # Payload enviado para o seu router de suppliers sem o campo email
                    payload = {
                        "name": name,
                        "cnpj": cnpj,
                        "address": address
                    }
                    res = api_post("suppliers", payload)
                    if res.status_code in [200, 201]:
                        st.success(f"Fornecedor '{name}' cadastrado!")
                        st.rerun() # Atualiza a lista automaticamente
                    else:
                        st.error(f"Erro ao cadastrar: {res.text}")