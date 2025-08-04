import config
import google.generativeai as genai


genai.configure(api_key=config.geminiKey) 

model = genai.GenerativeModel('gemini-2.0-flash')

chat = model.start_chat(history=[])

def send_message(message, chat_session):
    resposta = chat_session.send_message(message)
    return resposta

print("Chatbot Gemini iniciado! Digite 'sair' para terminar.")

while True:
    texto = input("Você: ")

    if texto.lower() == "sair":
        print("Até mais!")
        break
    
    if not texto.strip():
        print("Por favor, digite uma mensagem.")
        continue

    resposta_gemini = send_message(texto, chat)
    
    print(f"Chatbot: {resposta_gemini.text}")
