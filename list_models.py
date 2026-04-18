import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
try:
    response = requests.get(url)
    data = response.json()
    if 'models' in data:
        for m in data['models']:
            if 'embedContent' in m.get('supportedGenerationMethods', []):
                print(m['name'])
    else:
        print("Error fetching models:", data)
except Exception as e:
    print("Error:", e)
