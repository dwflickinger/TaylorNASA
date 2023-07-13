from flask import Flask, render_template
import os
import requests
import openai
from openai import ChatCompletion

app = Flask(__name__)

openai.api_key = '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'
dnTzboPUdbpUYTeVgIVX0bd4nG2JkVzjuBmpby6X = 'your_openai_api_key_here'

def fetch_nasa_apod_data(api_key):
    response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key=dnTzboPUdbpUYTeVgIVX0bd4nG2JkVzjuBmpby6X')
    data = response.json()
    return data['url'], data['explanation']

def simplify_text_with_chatgpt(text):
    model = "gpt-4-0613" # or use "text-davinci-002"
    chat_model = ChatCompletion.create(
      model=model,
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Explain this picture description and all the associated scientific concepts to a 3rd grader. Explain all the scientific concepts in detail not matter how complex such that a 3rd grader could understand. : {text}"}
        ]
    )
    return chat_model.choices[0]['message']['content']

@app.route('/')
def main():
    nasa_api_key = os.getenv('NASA_API_KEY') # Set your NASA API Key here
    image_url, description = fetch_nasa_apod_data(nasa_api_key)
    simplified_text = simplify_text_with_chatgpt(description)
    
    return render_template('index.html', image_url=image_url, original_desc=description, simplified_desc=simplified_text)

if __name__ == "__main__":
    app.run(debug=True)

