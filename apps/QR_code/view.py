from flask import Blueprint
from flask.templating import render_template
from ..exts.forms import ExcelForm

qrcode_bp=Blueprint("qrcode",__name__)

@qrcode_bp.route("/generate_qrcode")
def generate_qrcode():
    excel_form=ExcelForm()
    return render_template("QRCode/qrcode.html",form=excel_form)