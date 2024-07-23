from flask import Flask, render_template
from flask_limiter import Limiter
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
# Flask,render_template เริ่มต้นใช้ Flask Main
# Limiter สำหรับ กำหนด limit Call
# from .api_auth import middleware


def create_app():
    # สร้าง app (core server) ภายในไฟล์
    app = Flask(__name__)

    # Config app
    app.config.from_object('src.config')
    CORS(app)
    ### swagger specific ###
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Seans-Python-Flask-REST-Boilerplate"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    ### end swagger specific ###

    # app.wsgi_app = middleware(app.wsgi_app)
    
    # limiter = Limiter(
    #     app,
    #     key_func=get_remote_address,

    #     # set default limit
    #     # example set
    #     # default_limits=["2 per minute", "1 per second"]
    #     # default_limits=["1000 per day", "1 per second"],
    #     default_limits=["3000 per day"],
    # )

   # Binds the application only
    with app.app_context():

        from .controllers import Lab_Api
        from .controllers import package
        # emp.emp_bp from emp.py
        # app.register_blueprint(emp.emp_bp, url_prefix="/api/v2/emp")
        # set route index path

        @app.route('/')
        def index():
            return render_template('index.html')

    return app

