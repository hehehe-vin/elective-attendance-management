from flask import Flask, render_template
from flask_cors import CORS

# blueprints will be registered later
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'replace-with-secure-key'
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
