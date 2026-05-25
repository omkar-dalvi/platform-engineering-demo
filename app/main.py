import os

from .server import create_app


def main() -> None:
    app = create_app()
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
