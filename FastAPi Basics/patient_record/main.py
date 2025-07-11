## About the project
# Here we are creating a medical data record system using FastAPI.
# The system will allows to record the basic details such as id, name, age, city, gender, height, weight, blood group, verdict. 

"""

/create_endpoint
This is the endpoint to create a new patient record.
It accepts a JSON object with the following fields:
- id: int
- name: str
- age: int
- city: str
- gender: str
- height: float
- weight: float
- blood_group: str
- verdict: str

/view_endpoint
This is the endpoint to view all patient records.
It returns a JSON object with all the fields

/view/patient_id
This is the endpoint to view a specific patient record.
It accepts a path parameter `patient_id` and returns the record for that patient.

/update/patient_id
This is the endpoint to update a specific patient record.
It accepts a path parameter `patient_id` and a JSON object with the fields to update.

/delete/patient_id
This is the endpoint to delete a specific patient record.

"""
import json
from pydantic import BaseModel
from fastapi import FastAPI, Path

app = FastAPI()

def load_patient_records():
    """Load patient records from a file or database."""
    with open("patient_record.json", "r") as file:
        data = json.load(file)
    return data


@app.get("/")
def read_root():
    return {"message": "Welcome to the Patient Record System!"}


@app.get("/view")
def view_all_records():
    """View all patient records."""
    records = load_patient_records()
    return {"records": records}

@app.get("/view/{patient_id}")
def view_patient(patient_id:int = Path(..., description="The ID of the patient to view", example= 2 )):
    records = load_patient_records()
    for pat in records:
        if pat["id"] == patient_id:
            return {"record": pat}
    return {"message": "Patient not found."}    

class PatientUpdate(BaseModel):
    """We can only update the following fields."""
    age: int
    weight: float
    verdict: str

class PatientCreate(BaseModel):
    name: str
    age: int
    city: str
    gender: str
    height: float
    weight: float
    blood_group: str
    verdict: str

@app.post("/Add/")
def create_patient(patient_data: PatientUpdate):
    """Create a new patient record."""
    records = load_patient_records()
    new_id = max(pat["id"] for pat in records) + 1 if records else 1
    new_patient = {
        "id": new_id,
        "name": patient_data.name,
        "age": patient_data.age,
        "city": patient_data.city,
        "gender": patient_data.gender,
        "height": patient_data.height,
        "weight": patient_data.weight,
        "blood_group": patient_data.blood_group,
        "verdict": patient_data.verdict
    }
    # Add and save to file
    records.append(new_patient)
    with open("patient_record.json", "w") as file:
        json.dump(records, file, indent=4)

    return {"message": "New patient added successfully", "patient_id": new_id}

@app.post("/update/{patient_id}")
def update_patient(patient_id: int, patient_data: PatientUpdate):
    """Update a specific patient record."""
    records = load_patient_records()
    for pat in records:
        if pat["id"] == patient_id:
            pat.update(patient_data)
            with open("patient_record.json", "w") as file:
                json.dump(records, file, indent=4)
            return {"message": "Patient record updated successfully."}
    return {"message": "Patient not found."}

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: int):
    """Delete a specific patient record."""
    records = load_patient_records()
    for pat in records:
        if pat["id"] == patient_id:
            records.remove(pat)
            with open("patient_record.json", "w") as file:
                json.dump(records, file, indent=4)
            return {"message": "Patient record deleted successfully."}
    return {"message": "Patient not found."}