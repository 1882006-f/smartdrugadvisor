from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load the database
with open('data.json', 'r') as f:
    database = json.load(f)

drugs = database["drugs"]
commercial_names = database["commercial_names"]
symptoms = database["symptoms"]

def find_drug_info(drug_name):
    normalized_name = commercial_names.get(drug_name.lower(), drug_name.lower())
    for drug in drugs:
        if drug["name"] == normalized_name:
            return drug
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        symptom = request.form['symptom'].lower()
        drug_input = request.form['drug'].lower()
        expected_category = symptoms.get(symptom)

        drug_info = find_drug_info(drug_input)
        if not drug_info:
            result = {"error": "Medication not found. Please try another name."}
        else:
            correct_category = (drug_info['category'] == expected_category)
            result = {
                "correct_category": correct_category,
                "drug_info": drug_info
            }
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)