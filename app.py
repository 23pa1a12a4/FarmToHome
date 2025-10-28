from flask import Flask

app = Flask(_name_)

@app.route('/')
def home():
    return """
    <html>
      <head>
        <title>FarmToHome 🌾</title>
        <style>
          body {
            background-color: #e6ffe6;
            font-family: Arial, sans-serif;
            text-align: center;
            padding-top: 100px;
          }
          h1 {
            color: green;
          }
          p {
            font-size: 20px;
            color: #333;
          }
        </style>
      </head>
      <body>
        <h1>🌾 Welcome to FarmToHome 🌾</h1>
        <p>Connecting farmers directly to your home with natural, fresh produce!</p>
      </body>
    </html>
    """

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)
