# Import Necessary Libraries
from flask import Flask, request, jsonify
import pandas as pd


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
    # file = request.file['books.csv']
    data = pd.read_csv('books.csv')
    return jsonify(data.to_dict())

# Create Routes in the new app and set the HTTP function
@app.route('/upload', methods=['POST'])

# Create Method that takes books.csv and returns a JSON Object
def upload_file():
    data = pd.read_csv('books.csv')
    return jsonify(data.to_dict())

def categorize_data(data, categories):
    data = pd.read_csv('books.csv')
    cat_data = {}
    for category, keywords in categories.items():
        cat_data[category] = data[data['description'].str.contains('|'.join(keywords), case=False, na=False)]
        return cat_data

CATEGORIES = {
    'Murder Mystery': ['Suspicious','Unexpected', 'Courtroom', 'Murder', 'Psychopath']
}

@app.route('/process', methods=['GET'])
def process_data():
    data = pd.read_csv('books.csv')
    cat_data = categorize_data(data, CATEGORIES)
    return jsonify({cat: data.to_dict() for cat, data in cat_data.items()})


# Runs the app
if __name__ == '__main__':
    app.run(port=8080, debug=True)