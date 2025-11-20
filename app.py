from flask import Flask, render_template, request, jsonify
import os
import logging
from logging.handlers import RotatingFileHandler


# Configure logging
def setup_logging(app):
    """Set up logging configuration for the Flask app."""
    if not app.debug:
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(log_dir, exist_ok=True)

        # Set up file handler
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, "app.log"), maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("Application startup")


# Load environment variables
def load_config():
    """Load configuration from environment variables."""
    config = {
        "SECRET_KEY": os.environ.get(
            "SECRET_KEY", "dev-secret-key-change-in-production"
        ),
        "DEBUG": os.environ.get("FLASK_DEBUG", "True").lower() == "true",
        "PORT": int(os.environ.get("PORT", 8000)),
        "HOST": os.environ.get("FLASK_HOST", "0.0.0.0"),
    }
    return config


app = Flask(__name__)
config = load_config()
app.config.update(config)

# Set up logging
setup_logging(app)


@app.before_request
def log_request_info():
    """Log basic request information."""
    app.logger.info(f"{request.method} {request.url} - {request.remote_addr}")


@app.route("/")
def index():
    """Render the main theory page."""
    try:
        return render_template("index.html")
    except Exception as e:
        app.logger.error(f"Error rendering index.html: {str(e)}")
        return "Error loading page", 500


@app.route("/interactive")
def interactive():
    """Render the interactive 3D model page."""
    try:
        return render_template("interactive.html")
    except Exception as e:
        app.logger.error(f"Error rendering interactive.html: {str(e)}")
        return "Error loading interactive page", 500


@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors."""
    app.logger.warning(f"Page not found: {request.url}")
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    app.logger.error(f"Internal server error: {str(error)}")
    return render_template("500.html"), 500


@app.route("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"})


if __name__ == "__main__":
    app.run(debug=config["DEBUG"], host=config["HOST"], port=config["PORT"])
