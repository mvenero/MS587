# Flask Framework, and jsonify module
# https://flask.palletsprojects.com/en/3.0.x/api/
from flask import Flask, request, jsonify, render_template, send_file

# Hugging Face's open source library for NLP
from transformers import pipeline

app = Flask(__name__)

# Text generator using Hugging Face's pipeline
text_generator = pipeline("text-generation")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_story', methods=['POST'])
def generate_story():
    # Prompt from form
    prompt = request.form['prompt']

    # pass promt from user to text_generator function
    # limit prompt length to 100 chars
    generated_story = text_generator(prompt, max_length=100, num_return_sequences=1)

    # Create an array containin the story text
    #Python autmatically handles the type casting  
    story_text = generated_story[0]['generated_text']

    # Output to a text file
    # use write mode ',w' so the file will be created it if doesn't exist -- took forever to figure out
    with open('generated_story.txt', 'w') as file:
        file.write(story_text)

    # Download txt tile with generated story
    return send_file('generated_story.txt', as_attachment=True)

# Function to generate text based on user input
# POST method to send data to the server, data is returned in JSON format
@app.route('/generate_text', methods=['POST'])
def generate_text():
    # Prompt the user for text and pass to text generator
    prompt = request.json.get('prompt', '')

    # Generate text from the prompt
    generated_text = text_generator(prompt, max_length=100)[0]['generated_text']

    # Return the generated text as JSON response
    # Create the JSON OBJ using JSONIFY
    return jsonify({'generated_text': generated_text})

if __name__ == '__main__':
    app.run(debug=True)
