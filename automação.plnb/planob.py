import streamlit as st
import pandas as pd
import time
import os

from bot.whatsapp import iniciar_driver, abrir_conversa, enviar_imagem

# CONFIG
st.set_page_config(
    page_title="Disparador WhatsApp Pro",
    layout="wide",
    page_icon="📲"
)

# ESTILO VISUAL (CSS)
st.markdown("""
<style>
.main {
    background-color: #0f172a;
    color: white;
}
.stButton>button {
    background-color: #22c55e;
    color: white;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.title("📲 Disparador WhatsApp Profissional")
st.markdown("Sistema de envio automatizado com imagem e personalização")

# LAYOUT
col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Dados")
    arquivo = st.file_uploader("Lista de contatos", type=["xlsx"])
    imagem = st.file_uploader("Imagem do envio", type=["jpg", "png"])

with col2:
    st.subheader("💬 Mensagem")
    mensagem_modelo = st.text_area(
        "Use {nome} e {produto}",
        height=200,
        placeholder="Ex: Olá {nome}, vi que você busca {produto}..."
    )

    delay = st.slider("⏱️ Intervalo (segundos)", 5, 20, 8)

# BOTÕES
col3, col4 = st.columns(2)
with col3:
    iniciar = st.button("🚀 Iniciar envio")
with col4:
    parar = st.button("⛔ Parar envio")

# CONTROLE
if "rodando" not in st.session_state:
    st.session_state.rodando = False

if iniciar:
    st.session_state.rodando = True

if parar:
    st.session_state.rodando = False

# LOG E PROGRESSO
st.subheader("📊 Progresso")
progress = st.progress(0)
log_area = st.empty()

# EXECUÇÃO
if st.session_state.rodando:

    if arquivo is None or imagem is None or mensagem_modelo == "":
        st.error("Preencha todos os campos!")
    else:
        df = pd.read_excel(arquivo)

        caminho_img = "temp.jpg"
        with open(caminho_img, "wb") as f:
            f.write(imagem.read())

        driver = iniciar_driver()

        logs = []

        for i, row in df.iterrows():

            if not st.session_state.rodando:
                break

            nome = row["nome"]
            contato = row["telefone"]
            produto = row.get("produto", "")

            msg = mensagem_modelo.format(nome=nome, produto=produto)

            try:
                abrir_conversa(driver, contato)
                enviar_imagem(driver, os.path.abspath(caminho_img), msg)

                logs.append(f"✅ Enviado para {nome}")

            except Exception as e:
                logs.append(f"❌ Erro com {nome}: {e}")

            log_area.text("\n".join(logs))
            progress.progress((i + 1) / len(df))

            time.sleep(delay)

        st.success("🎉 Envio finalizado!")