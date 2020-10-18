from flask import Flask, request, jsonify
from text_analysis_sytem import Text_Analysis_System

app =Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():

    input_text = request.json["text"]

    tas = Text_Analysis_System()
    result = tas.analyze_text(input_text)

    return jsonify(result)


if __name__ == "__main__":

    app.run(debug=False)