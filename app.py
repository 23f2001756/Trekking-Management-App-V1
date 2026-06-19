from flask import Flask
app = Flask(__name__)

@app.route("/")
def mad1_project():
    return "<h1>This is mad1 project</h1>"

if __name__ == "__main__":
    app.run(debug=True)
