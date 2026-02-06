import streamlit as st
import requests
import pandas as pd

# --- CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="StockFlow Pro", layout="wide")

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
BASE_URL = "http://127.0.0.1:8000/api/v1"

# --- GERENCIAMENTO DE ESTADO (AUTH) ---
if 'token' not in st.session_state:
    st.session_state['token'] = None

def get_headers():
    if st.session_state['token']:
        return {"Authorization": f"Bearer {st.session_state['token']}"}
    return {}

def api_put(endpoint, data):
    return requests.put(f"{BASE_URL}/{endpoint}", json=data, headers=get_headers())

def api_delete(endpoint):
    return requests.delete(f"{BASE_URL}/{endpoint}", headers=get_headers())

# --- FUNÇÕES DE COMUNICAÇÃO ---
def login(email, password):
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
    st.stop()
else:
    if st.sidebar.button("Log out"):
        st.session_state['token'] = None
        st.rerun()

menu = st.sidebar.radio("Navegação", ["Dashboard", "Produtos", "Categorias", "Fornecedores"])

# --- PÁGINA: DASHBOARD ---
if menu == "Dashboard":
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

# --- PÁGINA: CATEGORIAS ---
elif menu == "Categorias":
    st.title("🏷️ Gestão de Categorias")
    tab1, tab2, tab3 = st.tabs(["📋 Listar", "➕ Cadastrar", "⚙️ Gerenciar"])

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
                    st.success("Categoria cadastrada!"); st.rerun()
                else:
                    st.error(f"Erro {res.status_code}: {res.text}")

    with tab3:
        st.subheader("Editar ou Excluir Categoria")
        cats = api_get("categories")
        if cats:
            cat_map = {c['name']: c for c in cats}
            sel_cat_name = st.selectbox("Selecione a Categoria", list(cat_map.keys()))
            cat_to_edit = cat_map[sel_cat_name]

            with st.form("edit_cat"):
                n_name = st.text_input("Novo Nome", value=cat_to_edit['name'])
                n_desc = st.text_area("Nova Descrição", value=cat_to_edit.get('description', ''))
                c1, c2 = st.columns(2)
                if c1.form_submit_button("💾 Atualizar"):
                    res = api_put(f"categories/{cat_to_edit['id']}", {"name": n_name, "description": n_desc})
                    if res.status_code == 200: st.success("Atualizada!"); st.rerun()
                if c2.form_submit_button("🗑️ Deletar", type="primary"):
                    res = api_delete(f"categories/{cat_to_edit['id']}")
                    if res.status_code == 204: st.success("Deletada!"); st.rerun()

# --- PÁGINA: PRODUTOS ---
elif menu == "Produtos":
    st.title("📦 Gestão de Produtos")
    tab1, tab2, tab3 = st.tabs(["📋 Listar", "➕ Cadastrar", "⚙️ Gerenciar"])
    
    cats = api_get("categories")
    sups = api_get("suppliers")
    
    with tab1:
        produtos = api_get("products")
        if produtos: st.dataframe(pd.DataFrame(produtos), use_container_width=True)
        else: st.info("Nenhum produto cadastrado.")

    with tab2:
        if not cats or not sups:
            st.warning("Cadastre categorias e fornecedores antes de criar produtos.")
        else:
            with st.form("form_prod"):
                name = st.text_input("Nome")
                price = st.number_input("Preço", min_value=0.0)
                qtd = st.number_input("Qtd", min_value=0)
                cat_name = st.selectbox("Categoria", [c['name'] for c in cats])
                sup_name = st.selectbox("Fornecedor", [s['name'] for s in sups])
                cat_id = next(c['id'] for c in cats if c['name'] == cat_name)
                sup_id = next(s['id'] for s in sups if s['name'] == sup_name)

                if st.form_submit_button("Cadastrar"):
                    payload = {"name": name, "price": price, "qtd": qtd, "category_id": cat_id, "supplier_id": sup_id}
                    res = api_post("products", payload)
                    if res.status_code == 201: st.success("Cadastrado!"); st.rerun()

    with tab3:
        produtos = api_get("products")
        if produtos:
            prod_map = {p['name']: p for p in produtos}
            sel_prod_name = st.selectbox("Selecione o Produto", list(prod_map.keys()))
            p_edit = prod_map[sel_prod_name]
            with st.form("edit_prod"):
                en_name = st.text_input("Nome", value=p_edit['name'])
                en_price = st.number_input("Preço", value=float(p_edit['price']))
                en_qtd = st.number_input("Quantidade", value=int(p_edit['qtd']))
                b1, b2 = st.columns(2)
                if b1.form_submit_button("💾 Atualizar"):
                    payload = {"name": en_name, "price": en_price, "qtd": en_qtd, "category_id": p_edit['category_id'], "supplier_id": p_edit['supplier_id']}
                    res = api_put(f"products/{p_edit['id']}", payload)
                    if res.status_code == 200: st.success("Atualizado!"); st.rerun()
                if b2.form_submit_button("🗑️ Deletar", type="primary"):
                    res = api_delete(f"products/{p_edit['id']}")
                    if res.status_code == 204: st.success("Removido!"); st.rerun()

# --- PÁGINA: FORNECEDORES ---
elif menu == "Fornecedores":
    st.title("🚚 Gestão de Fornecedores")
    tab1, tab2, tab3 = st.tabs(["📋 Listar", "➕ Cadastrar", "⚙️ Gerenciar"])

    with tab1:
        fornecedores = api_get("suppliers")
        if fornecedores:
            df_sup = pd.DataFrame(fornecedores)
            cols = [c for c in ['id', 'name', 'cnpj', 'address'] if c in df_sup.columns]
            st.dataframe(df_sup[cols], use_container_width=True)
        else: st.info("Nenhum fornecedor cadastrado.")

    with tab2:
        with st.form("form_supplier"):
            name = st.text_input("Nome da Empresa")
            cnpj = st.text_input("CNPJ")
            address = st.text_input("Endereço Completo")
            if st.form_submit_button("💾 Salvar Fornecedor"):
                res = api_post("suppliers", {"name": name, "cnpj": cnpj, "address": address})
                if res.status_code in [200, 201]: st.success("Cadastrado!"); st.rerun()

    with tab3:
        sups = api_get("suppliers")
        if sups:
            sup_map = {s['name']: s for s in sups}
            sel_sup = st.selectbox("Fornecedor", list(sup_map.keys()))
            s_edit = sup_map[sel_sup]
            with st.form("edit_sup"):
                es_name = st.text_input("Nome", value=s_edit['name'])
                es_cnpj = st.text_input("CNPJ", value=s_edit['cnpj'])
                es_addr = st.text_input("Endereço", value=s_edit['address'])
                s1, s2 = st.columns(2)
                if s1.form_submit_button("💾 Atualizar"):
                    res = api_put(f"suppliers/{s_edit['id']}", {"name": es_name, "cnpj": es_cnpj, "address": es_addr})
                    if res.status_code == 200: st.success("Atualizado!"); st.rerun()
                if s2.form_submit_button("🗑️ Deletar", type="primary"):
                    res = api_delete(f"suppliers/{s_edit['id']}")
                    if res.status_code == 204: st.success("Deletado!"); st.rerun()