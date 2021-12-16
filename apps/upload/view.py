from flask import Blueprint, request, redirect, render_template
from flask.helpers import flash, send_from_directory, url_for
from ..exts.forms import UploadForm
import os
from settings import File_UPLOAD_PATH
from uuid import uuid4

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["GET", "POST"])
def upload():
    form = UploadForm()
    if request.method == "POST":
        f = request.files.get("file")

        upload_path = os.path.join(
            File_UPLOAD_PATH, f.filename)
        f.save(upload_path)
        flash("上传成功！")
        return render_template("upload/upload.html", form=form)
    
    return render_template("upload/upload.html", form=form)


@upload_bp.route("/software")
def software():
    soft_list = os.listdir(os.path.join(File_UPLOAD_PATH, "办公软件"))
    docu_list = os.listdir(os.path.join(File_UPLOAD_PATH, "常用文件"))
    temp_list = os.listdir(os.path.join(File_UPLOAD_PATH, "临时文件"))
    return render_template("upload/software.html", soft_list=soft_list, docu_list=docu_list, temp_list=temp_list)


@upload_bp.route("/download_software/<folder>/<filename>")
def download_software(folder, filename):
    return send_from_directory(os.path.join(File_UPLOAD_PATH, folder), filename, as_attachment=True)
