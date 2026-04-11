import os
import requests
import json

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-8b-8192"

    def _post(self, prompt):
        if not self.api_key:
            return "Error: GROQ_API_KEY no configurada."
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error en la conexión con IA: {str(e)}"

    def generar_marketing(self, nombre, material):
        prompt = f"Genera una descripción corta y atractiva para marketing de una joya llamada '{nombre}' hecha de '{material}'."
        return self._post(prompt)

    def sugerir_precio(self, nombre, material, costo):
        prompt = (f"Sugiere un precio de venta para una joya '{nombre}' de '{material}' "
                  f"con un costo de producción de {costo}. Responde solo con el número sugerido y una breve justificación.")
        return self._post(prompt)

    def analizar_riesgo(self, nombre, deuda, limite):
        prompt = (f"Analiza el riesgo crediticio del cliente '{nombre}' que tiene una deuda de {deuda} "
                  f"y un límite de crédito de {limite}. Responde si es seguro seguir vendiendo a crédito y por qué.")
        return self._post(prompt)
