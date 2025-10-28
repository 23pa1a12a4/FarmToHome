from flask import Flask

app = Flask(_name_)

@app.route('/')
def home():
    return "<h1>Welcome to FarmToHome 🌾</h1><p>Connecting farmers directly to customers.</p>"

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)
