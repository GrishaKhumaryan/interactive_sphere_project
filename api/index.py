from flask import Flask

import download_libs  # սա կկատարվի deploy-ի ժամանակ

app = Flask(__name__)

@app.get("/")
def home():
    return {"message": "Hello from Flask on Vercel!"}

# Vercel handler
def handler(request, context):
    return app(request, context)
