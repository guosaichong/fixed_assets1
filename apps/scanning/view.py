from flask import Blueprint
from flask.templating import render_template

scan_bp=Blueprint("scan",__name__)

@scan_bp.route("/inventory")
def inverntory():
    return render_template("scanning/inventory.html")