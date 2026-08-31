from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from weather_mood_music import zip_info, get_music_suggestions, music_urls
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/get-weather", methods =["POST"])
def zip_code():
    info = request.get_json()
    res = zip_info(info["zip"])
    return jsonify(res)





if __name__ == "__main__":
    app.run(debug=True)