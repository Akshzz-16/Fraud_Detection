from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

# Load your trained fraud detection model
try:
    model = joblib.load("fraud_model.pkl")
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None

    if request.method == "POST":
        try:
            features = request.form["features"]
            print(f"🔹 Received input: {features}")

            feature_list = np.array([list(map(float, features.split(",")))])  # Convert to float array
            print(f"🔹 Converted input to array: {feature_list}")

            if feature_list.shape[1] != 30:  # Ensure correct number of features
                print(f"❌ Error: Expected 30 features, got {feature_list.shape[1]}")
                return render_template("index.html", prediction="Error: Incorrect feature count!")

            # Get probabilities instead of just class label
            probabilities = model.predict_proba(feature_list)[0]
            print(f"🔹 Prediction probabilities: {probabilities}")

            # Classify based on probability threshold (default 0.5)
            result = 1 if probabilities[1] > 0.7 else 0
            prediction = "Fraud" if result == 1 else "No Fraud"
            print(f"✅ Final Prediction: {prediction}")

        except Exception as e:
            print(f"❌ Error during prediction: {e}")
            prediction = f"Error: {e}"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
