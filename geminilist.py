import google.generativeai as genai
import config

# Configure a chave de API a partir do seu arquivo config.py
genai.configure(api_key=config.geminiKey)

print("Modelos Gemini disponíveis para chat (método 'generateContent'):")
print("-" * 60)

# Itera sobre todos os modelos disponíveis
for m in genai.list_models():
  # Verifica se o modelo suporta o método 'generateContent', que é usado para chat
  if 'generateContent' in m.supported_generation_methods:
    # Imprime o nome do modelo, que você pode copiar e colar no seu app.py
    print(m.name)

print("-" * 60)