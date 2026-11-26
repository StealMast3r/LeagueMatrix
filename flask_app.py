from flask import Flask

from website.routes.pages import pages_bp

app = Flask(
    __name__,
    template_folder="website/templates",
    static_folder="website/static"
)

app.register_blueprint(pages_bp)

if __name__ == "__main__":
    app.run(debug=True)