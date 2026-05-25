import os
from datetime import datetime
import psycopg2
from flask import Flask, jsonify


def get_config():
    return {
        "SERVICE_NAME": os.getenv("SERVICE_NAME", "platform-engineering-demo"),
        "ENVIRONMENT_NAME": os.getenv("ENVIRONMENT_NAME", "dev"),
        "PLATFORM_TEAM": os.getenv("PLATFORM_TEAM", "platform-team@gmail.com"),
        "DEPLOYMENT_VERSION": os.getenv("DEPLOYMENT_VERSION", "0.1.0"),
        "DEPLOYMENT_TAG": os.getenv("DEPLOYMENT_TAG", "latest"),
        "DEPLOYMENT_BUILD_DATE": os.getenv("DEPLOYMENT_BUILD_DATE", "unknown"),
        
    }


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "host.docker.internal"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "employee"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "mysecretpassword"),
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None


def init_db():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS Employee (
                    id SERIAL PRIMARY KEY,
                    customer_name TEXT NOT NULL,
                    department TEXT NOT NULL
                );
            """
            )
            conn.commit()
            print("Table 'Employee' checked/created successfully.")
            cur.execute("SELECT COUNT(*) FROM Employee")
            count = cur.fetchone()[0]

            # 3. Insert sample rows only if the table is empty
            if count == 0:
                sample_data = [
                    ("Alice Smith", "Engineering"),
                    ("Bob Jones", "Human Resources"),
                    ("Charlie Brown", "Product Management"),
                ]
                cur.executemany(
                    """
                    INSERT INTO Employee (customer_name, department) 
                    VALUES (%s, %s);
                """,
                    sample_data,
                )
                conn.commit()
                print("Three sample rows inserted.")
            else:
                print("Table already has data. Skipping sample insertion.")
    except Exception as e:
        print(f"Error creating table: {e}")
        conn.rollback()

def create_app() -> Flask:
    app = Flask(__name__)
    config = get_config()
    app.config.update(config)
    
    with app.app_context():
        init_db()

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

    @app.route("/employeedetails")
    def employee_details():
        db = get_db_connection()
        cur = db.cursor()
        cur.execute("SELECT id, customer_name, department FROM Employee ORDER BY id")
        employees = [
            {"id": row[0], "customer_name": row[1], "department": row[2]}
            for row in cur.fetchall()
        ]
        cur.close()
        return jsonify({"employees": employees})

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
