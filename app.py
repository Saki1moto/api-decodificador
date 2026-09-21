import streamlit as st
from googlenewsdecoder import gnewsdecoder
import time
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Decodificador de Links", page_icon="🔗", layout="centered")

st.title("🔗 Decodificador de Links do Google News")
st.write("Cole os seus links do Google News no campo abaixo (um por linha) e clique em **Decodificar**.")

# Caixa de texto para colar os links
texto_links = st.text_area("Cole os links aqui:", height=200, placeholder="https://news.google.com/rss/articles/...\nhttps://news.google.com/rss/articles/...")

if st.button("🚀 Decodificar Links", type="primary"):
    # Limpa linhas vazias e aspas
    linhas = [l.strip().replace('"', '').replace("'", "") for l in texto_links.splitlines() if l.strip()]
    
    if not linhas:
        st.warning("Por favor, cole pelo menos um link válido.")
    else:
        st.info(f"Iniciando a decodificação de {len(linhas)} links...")
        
        barra_progresso = st.progress(0)
        status_texto = st.empty()
        resultados = []
        
        for idx, link in enumerate(linhas):
            status_texto.text(f"Decodificando link {idx + 1} de {len(linhas)}...")
            
            try:
                res = gnewsdecoder(link, interval=1)
                if res.get("status"):
                    resultados.append({"Link Original": link, "Link Decodificado": res["decoded_url"]})
                else:
                    resultados.append({"Link Original": link, "Link Decodificado": f"Falha: {res.get('message')}"})
            except Exception as e:
                resultados.append({"Link Original": link, "Link Decodificado": f"Erro: {str(e)}"})
            
            # Atualiza barra de progresso
            barra_progresso.progress((idx + 1) / len(linhas))
            time.sleep(0.3)
        
        status_texto.empty()
        st.success("✅ Processamento concluído!")
        
        # Converte para DataFrame do Pandas
        df = pd.DataFrame(resultados)
        
        # Exibe a tabela interativa na tela
        st.dataframe(df, use_container_width=True)
        
        # Botão para baixar como arquivo Excel/CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Tabela em CSV / Excel",
            data=csv,
            file_name="links_decodificados.csv",
            mime="text/csv",
        )
