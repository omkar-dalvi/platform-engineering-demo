import os
from datetime import datetime

from flask import Flask, jsonify

EMPLOYEES = [
    {"id": "E001", "name": "Asha Patel", "department": "Engineering"},
    {"id": "E002", "name": "Jonas Rivera", "department": "Product"},
    {"id": "E003", "name": "Mina Shah", "department": "Platform"},
]


def get_config():
    return {
        "SERVICE_NAME": os.getenv("SERVICE_NAME", "platform-engineering-demo"),
        "ENVIRONMENT_NAME": os.getenv("ENVIRONMENT_NAME", "dev"),
        "PLATFORM_TEAM": os.getenv("PLATFORM_TEAM", "platform-team@gmail.com"),
        "DEPLOYMENT_VERSION": os.getenv("DEPLOYMENT_VERSION", "0.1.0"),
        "DEPLOYMENT_TAG": os.getenv("DEPLOYMENT_TAG", "latest"),
        "DEPLOYMENT_BUILD_DATE": os.getenv("DEPLOYMENT_BUILD_DATE", "unknown"),
    }


def create_app() -> Flask:
    app = Flask(__name__)
    config = get_config()
    app.config.update(config)

    @app.route("/")
    def home():
        return jsonify(
            {
                "application": {
                    "name": app.config["SERVICE_NAME"],
                    "description": "Platform engineering demo service for deployment and environment introspection.",
                    "version": app.config["DEPLOYMENT_VERSION"],
                },
                "environment": {
                    "name": app.config["ENVIRONMENT_NAME"],
                    "platform_team": app.config["PLATFORM_TEAM"],
                },
                "metadata": {
                    "deployment_tag": app.config["DEPLOYMENT_TAG"],
                    "deployment_build_date": app.config["DEPLOYMENT_BUILD_DATE"],
                },
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

    @app.route("/employeeddetails")
    def employee_details():
        return jsonify({"employees": EMPLOYEES})

    @app.route("/health")
    def health():
        return jsonify(
            {
                "status": "pass",
                "liveness": "alive",
                "readiness": "ready",
                "environment": app.config["ENVIRONMENT_NAME"],
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

    @app.route("/info")
    def info():
        return jsonify(
            {
                "environment": app.config["ENVIRONMENT_NAME"],
                "platform_team": {
                    "contact": app.config["PLATFORM_TEAM"],
                    "responsibility": "Deployment lifecycle, runtime observability, and container standards.",
                },
                "deployment": {
                    "version": app.config["DEPLOYMENT_VERSION"],
                    "tag": app.config["DEPLOYMENT_TAG"],
                    "build_date": app.config["DEPLOYMENT_BUILD_DATE"],
                },
            }
        )

    return app


app = create_app()
