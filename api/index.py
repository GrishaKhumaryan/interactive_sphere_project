import download_libs  # սա կաշխատի import-ի պահին

from flask import Flask
app = Flask(__name__)

@app.get("/")
def home():
    return {"message": "Libraries downloaded automatically"}
