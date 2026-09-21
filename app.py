import streamlit as st
import pandas as pd
import base64
import re

# Função mágica que decodifica offline (sem internet = impossível o Google bloquear!)
def decodificar_offline(url):
    try:
        # Pega a parte do link que tem o código criptografado "CBM..."
        match = re.search(r'articles/([a-zA-Z0-9-_]+)', url)
        if not match: return None
        
        codigo = match.group(1)
        # Ajusta o tamanho do texto para o Base64 conseguir ler
        codigo += "=" * ((4 - len(codigo) % 4) % 4)
        
        # Desfaz a criptografia
        decoded_bytes = base64.urlsafe_b64decode(codigo)
        text = decoded_bytes.decode('latin1', errors='ignore')
        
        # Puxa o link real de dentro do texto decifrado
        url_match = re.search(r'(https?://[a-zA-Z0-9-._~:/?#\[\]@!$&\'()*+,;=%]+)', text)
        if url_match:
            return url_match.group(1)
    except:
        pass
    return None

# ----- INTERFACE DO SITE -----
st.set_page_config(page_title="Decodificador de Links", page_icon="🔗", layout="centered")
st.title("🔗 Decodificador de Links (Modo Turbo)")
st.write("Cole os seus links (um por linha) e clique em **Decodificar**.")

texto_links = st.text_area("Cole os links aqui:", height=200)

if st.button("🚀 Decodificar Links", type="primary"):
    linhas = [l.strip().replace('"', '').replace("'", "") for l in texto_links.splitlines() if l.strip()]
    
    if not linhas:
        st.warning("Por favor, cole pelo menos um link válido.")
    else:
        st.info(f"Descriptografando {len(linhas)} links...")
        barra_progresso = st.progress(0)
        resultados = []
        
        # Importamos a biblioteca apenas como "Plano B"
        from googlenewsdecoder import gnewsdecoder 
        
        for idx, link in enumerate(linhas):
            # 1ª TENTATIVA: MODO OFFLINE (Garante que o Google não bloqueie)
            url_limpa = decodificar_offline(link)
            
            if url_limpa:
                resultados.append({"Link Original": link, "Link Decodificado": url_limpa})
            else:
                # 2ª TENTATIVA: Plano B (Usa a internet só se o link for num formato muito antigo)
                try:
                    res = gnewsdecoder(link, interval=1)
                    if res and res.get("status"):
                        resultados.append({"Link Original": link, "Link Decodificado": res["decoded_url"]})
                    else:
                        erro_msg = res.get('message') if res else 'Bloqueado pelo Google'
                        resultados.append({"Link Original": link, "Link Decodificado": f"Falha: {erro_msg}"})
                except Exception as e:
                    resultados.append({"Link Original": link, "Link Decodificado": f"Erro: {str(e)}"})
            
            # Atualiza barrinha
            barra_progresso.progress((idx + 1) / len(linhas))
            
        st.success("✅ Processamento concluído em tempo recorde!")
        
        # Mostra a tabela na tela
        df = pd.DataFrame(resultados)
        st.dataframe(df, use_container_width=True)
        
        # Botão de download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar Tabela em CSV", data=csv, file_name="links_decodificados.csv", mime="text/csv")
