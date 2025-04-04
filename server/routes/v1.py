from flask import Blueprint, jsonify, request
from flask_login import login_required
from transformers import MarianMTModel, MarianTokenizer

v1 = Blueprint("v1", __name__, url_prefix="/api/v1/")


@v1.route("/translate", methods=["POST"])
@login_required
def translate():
    data = request.get_json()
    query = data.get("query")
    src_language = data.get("src")
    dst_language = data.get("dst")
    model = f"Helsinki-NLP/opus-mt-{src_language}-{dst_language}"


@v1.route("/get_languages")
@login_required
def get_languages():
    pass
