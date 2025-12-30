from flask import Flask
from regions import regions_bp
from industries import industries_bp
from date_posted import dateposted_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(regions_bp)
app.register_blueprint(industries_bp)
app.register_blueprint(dateposted_bp)

if __name__ == "__main__":
    app.run(debug=True)
