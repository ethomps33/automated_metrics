# Import Necessary Libraries
from flask import Flask, request, jsonify
import pandas as pd

# Create app using Flask
app = Flask(__name__)

# Create a Route in the new app and set the HTTP function
@app.route('/upload', methods=['POST'])

# Create Method that takes books.csv and returns a JSON Object
def upload_file():
    file = request.file['books']
    data = pd.read_csv(file)
    return jsonify(data.to_dict())

# Runs the app
if __name__ == '__main__':
    app.run(debug=True)