from flask import Blueprint, render_template

web_blueprint = Blueprint('web', __name__)


@web_blueprint.route('/')
def index():
    return render_template('index.html')
