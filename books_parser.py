# Import Necessary Libraries
from flask import Flask, request, jsonify
import pandas as pd
from statistics import mode

# Create app using Flask
app = Flask(__name__)

# Create Route for the Homepage
@app.route('/')
def homepage():
    return(
        f"The Book Parser App is up and Running!</br>"
    )

# Route to View the Data from the books.csv file
@app.route('/api', methods=['GET'])
def api():
    # file = request.files['books.csv']
    data = pd.read_csv('books.csv')
    return jsonify(data.to_dict())

# Create Routes in the new app and set the HTTP function
@app.route('/upload', methods=['POST'])

# Create Method that takes books.csv and returns a JSON Object
def upload_file():
    # file = request.files['books.csv']
    data = pd.read_csv('books.csv')
    return jsonify(data.to_dict())

# Method that takes the data from the CSV and a list of Categories with keywords and returns data grouped by the categories given
def categorize_data(data, categories):
    # file = request.files['books.csv']
    data = pd.read_csv('books.csv')
    cat_data = {}
    for category, keywords in categories.items():
        cat_data[category] = data[data['description'].str.contains('|'.join(keywords), case=False, na=False)]
        return cat_data

# Dictionary of different Categories for the data to be grouped by
CATEGORIES = {
    'Murder Mystery': ['Suspicious','Unexpected', 'Courtroom', 'Murder', 'Psychopath']
    # 'Science Fiction': ['Aliens', 'Space', 'Cloning']
}

# Route that returns the Categorized Data
@app.route('/process', methods=['GET'])
def process_data():
    # file = request.files['books.csv']
    data = pd.read_csv('books.csv')
    cat_data = categorize_data(data, CATEGORIES)
    return jsonify({cat: data.to_dict() for cat, data in cat_data.items()})

# Method that Aggregates the Categorized Data to be used for Visulizations
def aggragate_data(cat_data):
    metrics = {}
    for cat, data in cat_data.items():
        metrics[cat] = {
            'total_titles': data['title'].count().astype('float'),
            'average_category_rating': data['average_rating'].mean(),
            'avg_category_pages': data['num_pages'].mean(),
            'most_frequent_author': mode(data['authors'])
        }
        return metrics
    
@app.route('/metrics', methods=['GET'])
def calculate_metrics():
    # file = request.files['books.csv']
    data = pd.read_csv('books.csv')
    cat_data = categorize_data(data, CATEGORIES)
    metrics = aggragate_data(cat_data)
    return jsonify(metrics)

# Runs the app
if __name__ == '__main__':
    app.run(port=8080, debug=True)