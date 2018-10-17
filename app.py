import json
from flask import Flask, request, jsonify
import os
from Dao import Dao
from DiagnosisClient import DiagnosisClient
from WebScrapper import WebScrapper
import config



app = Flask(__name__)
diagnosisClient = DiagnosisClient(config.username, config.password, config.priaid_authservice_url, config.language, config.priaid_healthservice_url)
web_scrapper = WebScrapper()
dao = Dao(config)


# i have taken the help of publicly available code on priaid
# fetch all the symptoms present in medic records
@app.route("/fetch_all_symptoms", methods=["GET"])
def fetch_all_symptoms():
    return jsonify(diagnosisClient.loadSymptoms())

@app.route("/fetch_proposed_symptom", methods=["POST"])
def fetch_proposed_symptom():
    payload_data = json.loads(request.data)
    symptom_name = payload_data.get("symptom")
    gender = payload_data.get("gender")
    year = payload_data.get("birth_year")
    return json.dumps(diagnosisClient.loadProposedSymptoms(symptom_name, gender, year))

@app.route("/fetch_medical_condition_by_symptom_ids", methods=["POST"])
def fetch_symptoms_by_params():
    payload_data = json.loads(request.data)
    symptom_ids = payload_data.get("symptom_ids")
    gender = payload_data.get("gender")
    year = payload_data.get("birth_year")
    return json.dumps(diagnosisClient.loadMedicalIssues(symptom_ids, gender, year))

@app.route("/fetch_treatement_option_by_medical_condition", methods=["GET"])
def fetch_treatment_option_by_medical_condition():
    medical_condition = str(request.args.get("medical_condition"))
    metadata = dao.fetch_metadata_by_medical_condition(medical_condition)
    treatment_options = None
    if(metadata is None):
        treatment_options = json.dumps(web_scrapper.find_treatment_options_for_medical_condition(medical_condition))
        dao.persist_medical_metadata(medical_condition, treatment_options)
    else:
        metadata = json.loads(metadata.get("metadata"))
        treatment_options = json.dumps({"treatment_options": metadata.get("treatment_options")})
    if (treatment_options is None):
        return ValueError({"error" : "unable to find treatment options"})
    return treatment_options








if __name__ == '__main__':
    app.run(debug=True)