from flask import Blueprint, render_template
from flask import Flask, request, jsonify

app = Flask(__name__)



settlements = Blueprint('settlements', __name__)


@settlements.route('/settlement')
def settlement():
    return render_template('settlement.html')
