from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    text = "ALRIGHT"
    return text



if __name__ == "__main__":
    app.run(debug=True)
