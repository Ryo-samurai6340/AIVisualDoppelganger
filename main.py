from flask import Flask, render_template, request
from PIL import Image
import os
import io
import base64
import numpy as np
from genetic_algorithm import GeneticAlgorithm

app = Flask(__name__)  # create Flask web app

# Set the upload folder for imgs
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure that the 'uploads' folder actually exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# define function to process the uploaded img
def process_image(file_path, generations, mutation_rate):
    img = Image.open(file_path)  # open the image using Pillow
    image_array = np.array(img)  # convert the img to a binary array.
    
    # set up the genetic algo w population size and chromosome length
    population_size = 50
    chromosome_length = image_array.size
    genetic_algorithm = GeneticAlgorithm(population_size, chromosome_length)

    # evolve the population to find the best individual
    best_individual = genetic_algorithm.evolve(image_array, generations, mutation_rate)

    # Decode the best individual to get the replicated image.
    decoded_best_individual = genetic_algorithm.decode_individual(best_individual, image_array)

    # convert the decoded array back to an img
    replicated_img = Image.fromarray(decoded_best_individual.astype(np.uint8))

    return replicated_img

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle form submission and process the img
@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        return "No file part"

    # Get the uploaded file from teh form 
    file = request.files['image']
    print("Uploaded file:", file.filename)

    if file.filename == '':
        return "No selected file"

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    print("File saved to:", file_path)

    # Define original_image is a binary array that shows the desired camouflage pattern
    # original_image = np.array([0, 1, 0, 1, 0, 1, 0, 1])

    # Set the number of generations and mutation rate
    generations = 1
    mutation_rate = 0.5
    img = Image.open(file_path)  # Open the uploaded img using Pillow

    # Process the uploaded image using the genetic algo
    replicated_image = process_image(file_path, generations, mutation_rate)

    # Display the original and replicated imgs in the browser
    with io.BytesIO() as output_original, io.BytesIO() as output_replicated:
        img.save(output_original, format="PNG")
        replicated_image.save(output_replicated, format="PNG")

        # convert img data to base64 for rendering in HTML 
        original_image_data = base64.b64encode(output_original.getvalue()).decode('utf-8')
        replicated_image_data = base64.b64encode(output_replicated.getvalue()).decode('utf-8')

    return render_template('index.html', original_image=original_image_data, replicated_image=replicated_image_data, generations=generations, mutation_rate=mutation_rate)

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
    