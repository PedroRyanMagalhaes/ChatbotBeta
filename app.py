import streamlit as st
import google.generativeai as genai
import os
import config

# --- CONFIGURAÇÃO DA PÁGINA E DA API ---

st.set_page_config(page_title="Meu Chatbot Gemini", page_icon="🤖")

# Título principal da aplicação
st.title("🤖 Meu Chatbot com Gemini")
st.caption("Um chatbot simples usando a API do Google Gemini e Streamlit")

try:
    genai.configure(api_key=config.geminiKey)
except AttributeError:
    st.error("A variável 'GEMINI_API_KEY' não foi encontrada no seu arquivo config.py!")
    st.stop() 
except ImportError:
    st.error("Não foi possível encontrar o arquivo config.py. Verifique se ele está na mesma pasta do app.py.")
    st.stop() 

# --- INICIALIZAÇÃO DO MODELO E DO CHAT ---

# Função para inicializar o modelo. O cache evita recriar o modelo a cada execução.
@st.cache_resource
def load_model():
    return genai.GenerativeModel('gemini-1.5-flash-latest') # Usando um modelo mais recente

model = load_model()

# Inicializa a sessão de chat no st.session_state se ela não existir
if "chat_session" not in st.session_state:
    instrucao_inicial = {
        "role": "user",
        "parts": [
            "Você é um chatbot assistente criado por Pedro Magalhães. "
            "Se alguém perguntar quem te criou ou quem é seu criador, "
            "você deve responder que foi criado por Pedro Magalhães e fornecer o link do LinkedIn dele: "
            "https://www.linkedin.com/in/pedro-ryan-magalh%C3%A3es-/ "
            "Responda a todas as outras perguntas normalmente."
        ]
    }
    
    resposta_confirmacao = {
        "role": "model",
        "parts": ["Entendido! Eu sou um chatbot criado por Pedro Magalhães. Responderei às perguntas sobre meu criador conforme instruído."]
    }

    st.session_state.chat_session = model.start_chat(history=[instrucao_inicial, resposta_confirmacao])

# Inicializa o histórico de mensagens no st.session_state se ele não existir
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- EXIBIÇÃO DO HISTÓRICO DE CHAT ---

# Mostra as mensagens antigas na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LÓGICA DE INTERAÇÃO DO CHAT ---

# Captura a entrada do usuário no campo de chat
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adiciona e exibe a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Envia a mensagem para o Gemini e obtém a resposta
    try:
        with st.chat_message("assistant"):
            # Mostra um "spinner" enquanto a resposta está sendo gerada
            with st.spinner("Pensando..."):
                response = st.session_state.chat_session.send_message(prompt)
                
            # Exibe a resposta do assistente
            st.markdown(response.text)
        
        # Adiciona a resposta do assistente ao histórico
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")