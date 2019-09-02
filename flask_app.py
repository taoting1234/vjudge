from app import create_app
from app.libs.error import NotFound

app = create_app()


@app.errorhandler(404)
def handle_404():
    return NotFound()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
