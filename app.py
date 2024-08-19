from flask import Flask, render_template, request
import re

app = Flask(__name__)

def check_password_strength(password):
    length_criteria = len(password) >= 8
    lowercase_criteria = re.search(r"[a-z]", password) is not None
    uppercase_criteria = re.search(r"[A-Z]", password) is not None
    digit_criteria = re.search(r"[0-9]", password) is not None
    symbol_criteria = re.search(r"[@#$%^&+=]", password) is not None
    
    score = sum([length_criteria, lowercase_criteria, uppercase_criteria, digit_criteria, symbol_criteria])
    
    if score == 5:
        strength = "Sangat Kuat"
    elif score == 4:
        strength = "Kuat"
    elif score == 3:
        strength = "Sedang"
    else:
        strength = "Lemah"
    
    return strength, score

def recommend_improvements(password):
    recommendations = []
    if len(password) < 8:
        recommendations.append("Tambahkan lebih banyak karakter (minimal 8 karakter).")
    if re.search(r"[a-z]", password) is None:
        recommendations.append("Tambahkan huruf kecil.")
    if re.search(r"[A-Z]", password) is None:
        recommendations.append("Tambahkan huruf besar.")
    if re.search(r"[0-9]", password) is None:
        recommendations.append("Tambahkan angka.")
    if re.search(r"[@#$%^&+=]", password) is None:
        recommendations.append("Tambahkan simbol (@, #, $, %, ^, &, +, =).")
    
    return recommendations

@app.route("/", methods=["GET", "POST"])
def index():
    strength = None
    score = None
    recommendations = None
    
    if request.method == "POST":
        password = request.form["password"]
        strength, score = check_password_strength(password)
        if strength != "Sangat Kuat":
            recommendations = recommend_improvements(password)
    
    return render_template("index.html", strength=strength, score=score, recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
