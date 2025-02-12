from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "secret_key"

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load initial dataset
df = pd.read_csv("cleaned_data_final_new.csv")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    global df
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files["file"]

        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Load new dataset
            new_data = pd.read_csv(filepath)

            # Ensure necessary columns exist
            required_columns = ["Name", "Age", "Gender", "Country", "Gotra", "Occupation", "Education", "Income"]
            if not all(col in new_data.columns for col in required_columns):
                flash("Invalid CSV format. Required columns: " + ", ".join(required_columns))
                return redirect(request.url)

            # Append new data to the existing DataFrame
            df = pd.concat([df, new_data], ignore_index=True)

            flash("File uploaded successfully and data merged!")

    # Get unique values for filters dynamically
    age_min = int(df["Age"].min())
    age_max = int(df["Age"].max())
    gender_options = df["Gender"].dropna().unique().tolist()
    country_options = df["Country"].dropna().unique().tolist()
    gotra_options = df["Gotra"].dropna().unique().tolist()

    return render_template(
        "index.html",
        age_min=age_min,
        age_max=age_max,
        gender_options=gender_options,
        country_options=country_options,
        gotra_options=gotra_options,
    )

@app.route("/results", methods=["POST"])
def results():
    global df
    filtered_df = df.copy()
    
    min_age = request.form.get("min_age")
    max_age = request.form.get("max_age")
    gender = request.form.get("gender")
    country = request.form.get("country")
    gotra = request.form.get("gotra")

    if min_age:
        filtered_df = filtered_df[filtered_df["Age"] >= int(min_age)]
    if max_age:
        filtered_df = filtered_df[filtered_df["Age"] <= int(max_age)]
    if gender:
        filtered_df = filtered_df[filtered_df["Gender"] == gender]
    if country:
        filtered_df = filtered_df[filtered_df["Country"] == country]
    if gotra:
        filtered_df = filtered_df[filtered_df["Gotra"] == gotra]
    
    return render_template("result.html", profiles=filtered_df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
