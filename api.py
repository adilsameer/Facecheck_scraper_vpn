import os
import uuid
import csv
from flask import Flask, request, jsonify
from scraper import Scraper

app = Flask(__name__)

results_file = 'results.csv'
uploads_dir = "uploads"
os.makedirs(uploads_dir, exist_ok=True)

# Ensure the results CSV file exists
if not os.path.exists(results_file):
    with open(results_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "urls"])

def add_results_to_csv(image_id, urls):
    with open(results_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([image_id, ','.join(urls)])

def get_results_from_csv(image_id):
    results = {}
    with open(results_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            results[row['id']] = row['urls'].split(',')
    return results.get(image_id, None)

def remove_results_from_csv(image_id):
    rows = []
    with open(results_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        rows = [row for row in reader if row[0] != image_id]

    with open(results_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400

    image_id = str(uuid.uuid4())
    image_path = os.path.join(uploads_dir, image_id + ".jpg")
    image.save(image_path)

    # Start the scraping process only if the image is successfully saved
    if os.path.exists(image_path):
        scraper = Scraper()
        scraper.main(fr"path{image_path}")

        # Store the results in the CSV file
        add_results_to_csv(image_id, scraper.extracted_urls)

        return jsonify({"id": image_id})
    else:
        return jsonify({"error": "Failed to save the uploaded image"}), 500

@app.route('/results/<image_id>', methods=['GET'])
def get_results(image_id):
    urls = get_results_from_csv(image_id)
    if not urls:
        return jsonify({"error": "Invalid ID"}), 404

    # Delete the image and remove the result from CSV after accessing
    image_path = os.path.join(uploads_dir, image_id + ".jpg")
    if os.path.exists(image_path):
        os.remove(image_path)
    remove_results_from_csv(image_id)

    return jsonify({"urls": urls})

if __name__ == '__main__':
    app.run(debug=False)
