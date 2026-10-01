import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Calculadora Nutricional",
    page_icon="🧮",
    layout="wide"
)

st.title("🧮 Calculadora Nutricional")
st.write("Gerencie dados, alimentos e monte refeições personalizadas.")

# Inicialização do estado da sessão (banco de dados em memória)
if "dados_pessoa" not in st.session_state:
    st.session_state.dados_pessoa = {}

if "alimentos" not in st.session_state:
    st.session_state.alimentos = {}

if "refeicao" not in st.session_state:
    st.session_state.refeicao = []

# Criação das Abas
aba1, aba2, aba3, aba4 = st.tabs([
    "👤 Dados da Pessoa", 
    "🥗 Cadastrar Alimentos", 
    "🍽️ Montar Refeição", 
    "📊 Resultados"
])

# ============================================================
# ABA 1 - DADOS DA PESSOA
# ============================================================
with aba1:
    st.header("Dados da Pessoa")
    
    nome = st.text_input("Nome:", value=st.session_state.dados_pessoa.get("nome", ""))
    idade = st.number_input("Idade:", min_value=0, step=1, value=st.session_state.dados_pessoa.get("idade", 0))
    peso = st.number_input("Peso (kg):", min_value=0.0, step=0.1, value=st.session_state.dados_pessoa.get("peso", 0.0))
    altura = st.number_input("Altura (cm):", min_value=0.0, step=1.0, value=st.session_state.dados_pessoa.get("altura", 0.0))
    restricoes = st.text_area("Restrições alimentares:", value=st.session_state.dados_pessoa.get("restricoes", ""))

    if st.button("Salvar Dados da Pessoa", type="primary"):
        if not nome.strip():
            st.warning("⚠️ Informe o nome.")
        elif peso <= 0 or altura <= 0:
            st.warning("⚠️️ Informe peso e altura válidos.")
        else:
            st.session_state.dados_pessoa = {
                "nome": nome.strip(),
                "idade": idade,
                "peso": peso,
                "altura": altura,
                "restricoes": restricoes.strip()
            }
            st.success("✅ Dados salvos com sucesso!")

# ============================================================
# ABA 2 - CADASTRO DE ALIMENTOS
# ============================================================
with aba2:
    st.header("Cadastrar Alimento")
    st.caption("Informe os valores nutricionais referentes a **100 g** do alimento.")

    nome_alim = st.text_input("Nome do alimento:", placeholder="Ex.: Arroz")
    
    col1, col2 = st.columns(2)
    with col1:
        calorias = st.number_input("Kcal (por 100g):", min_value=0.0, step=1.0)
        carboidratos = st.number_input("Carboidratos (g):", min_value=0.0, step=0.1)
        fibras = st.number_input("Fibras (g):", min_value=0.0, step=0.1)
    with col2:
        proteinas = st.number_input("Proteínas (g):", min_value=0.0, step=0.1)
        gorduras = st.number_input("Gorduras (g):", min_value=0.0, step=0.1)
        restricao_alim = st.text_input("Restrição/Alergênico:", placeholder="Ex.: lactose")

    if st.button("Cadastrar Alimento", type="primary"):
        if not nome_alim.strip():
            st.warning("⚠️ Informe o nome do alimento.")
        else:
            chave = nome_alim.strip().lower()
            st.session_state.alimentos[chave] = {
                "nome": nome_alim.strip(),
                "calorias": calorias,
                "proteinas": proteinas,
                "carboidratos": carboidratos,
                "gorduras": gorduras,
                "fibras": fibras,
                "restricao": restricao_alim.strip()
            }
            st.success(f"✅ Alimento '{nome_alim}' cadastrado!")

    st.subheader("Alimentos Cadastrados")
    if st.session_state.alimentos:
        df_alimentos = pd.DataFrame(st.session_state.alimentos.values())
        st.dataframe(df_alimentos, use_container_width=True)
    else:
        st.info("Nenhum alimento cadastrado ainda.")

# ============================================================
# ABA 3 - REFEIÇÕES
# ============================================================
with aba3:
    st.header("Montar Refeição")

    if not st.session_state.alimentos:
        st.warning("⚠️ Cadastre alimentos na aba 'Cadastrar Alimentos' antes de montar a refeição.")
    else:
        opcoes = {v["nome"]: k for k, v in st.session_state.alimentos.items()}
        alimento_sel_nome = st.selectbox("Selecione o alimento:", options=list(opcoes.keys()))
        qtd = st.number_input("Quantidade (g):", min_value=1.0, value=100.0, step=10.0)

        col_add, col_rem, col_lim = st.columns(3)
        
        with col_add:
            if st.button("➕ Adicionar"):
                chave = opcoes[alimento_sel_nome]
                alimento = st.session_state.alimentos[chave]
                fator = qtd / 100.0
                
                st.session_state.refeicao.append({
                    "nome": alimento["nome"],
                    "quantidade": qtd,
                    "calorias": alimento["calorias"] * fator,
                    "proteinas": alimento["proteinas"] * fator,
                    "carboidratos": alimento["carboidratos"] * fator,
                    "gorduras": alimento["gorduras"] * fator,
                    "fibras": alimento["fibras"] * fator
                })
                st.success(f"Adicionado: {qtd}g de {alimento['nome']}")

        with col_rem:
            if st.button("🗑️ Remover Último"):
                if st.session_state.refeicao:
                    removido = st.session_state.refeicao.pop()
                    st.info(f"Removido: {removido['nome']}")

        with col_lim:
            if st.button("❌ Limpar Refeição"):
                st.session_state.refeicao.clear()
                st.info("Refeição limpa.")

        st.subheader("Alimentos na Refeição Atual")
        if st.session_state.refeicao:
            df_refeicao = pd.DataFrame(st.session_state.refeicao)
            st.dataframe(df_refeicao, use_container_width=True)
        else:
            st.info("Nenhum alimento adicionado à refeição.")

# ============================================================
# ABA 4 - RESULTADOS
# ============================================================
with aba4:
    st.header("Resultado Nutricional")

    if not st.session_state.refeicao:
        st.info("Adicione alimentos na aba 'Montar Refeição' para visualizar os resultados.")
    else:
        df_ref = pd.DataFrame(st.session_state.refeicao)
        
        totais = {
            "Calorias (kcal)": df_ref["calorias"].sum(),
            "Proteínas (g)": df_ref["proteinas"].sum(),
            "Carboidratos (g)": df_ref["carboidratos"].sum(),
            "Gorduras (g)": df_ref["gorduras"].sum(),
            "Fibras (g)": df_ref["fibras"].sum()
        }

        nome_pessoa = st.session_state.dados_pessoa.get("nome", "Não informado")
        st.subheader(f"Resumo para: {nome_pessoa}")

        # Exibição de métricas em cartões
        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
        col_m1.metric("Calorias", f"{totais['Calorias (kcal)']:.1f} kcal")
        col_m2.metric("Proteínas", f"{totais['Proteínas (g)']:.1f} g")
        col_m3.metric("Carboidratos", f"{totais['Carboidratos (g)']:.1f} g")
        col_m4.metric("Gorduras", f"{totais['Gorduras (g)']:.1f} g")
        col_m5.metric("Fibras", f"{totais['Fibras (g)']:.1f} g")

        if st.session_state.dados_pessoa.get("restricoes"):
            st.warning(f"⚠️️ Restrições da pessoa: {st.session_state.dados_pessoa['restricoes']}")
