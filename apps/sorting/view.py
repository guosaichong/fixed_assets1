
from flask.helpers import url_for
from flask.templating import render_template
from flask import Blueprint,request,redirect
from settings import File_UPLOAD_PATH
import os
sorting_bp = Blueprint("sorting", __name__)

# 奇数提示页面


@sorting_bp.route("/odd_tips")
def odd_tips():
    """
    奇数提示
    """
    # 检查上传的文件夹目录下是否有`奇数.txt`文件
    if "奇数.txt" in os.listdir(File_UPLOAD_PATH):
        odd_list=[]
        with open(File_UPLOAD_PATH+os.sep+"奇数.txt","r") as f:
            odd_list=f.readlines()
        return render_template("sorting/odd_tips.html",odd_list=odd_list)
    else:

        # print(os.listdir(File_UPLOAD_PATH))
        if "DownLoadBill.txt" in os.listdir(File_UPLOAD_PATH):
            odd_str = ""
            even_str = ""
            # 打开文件
            with open(File_UPLOAD_PATH+os.sep+"DownLoadBill.txt", "r") as f:

                for i in f.readlines()[1:]:
                    if int(i.split(";")[9]) % 2 != 0:
                        odd_str = odd_str+i.split(";")[3]+"\n"
                    else:
                        even_str = even_str+i.split(";")[3]+"\n"
            with open(File_UPLOAD_PATH+os.sep+"奇数.txt","w") as f:
                f.write(odd_str)
            with open(File_UPLOAD_PATH+os.sep+"偶数.txt","w") as f:
                f.write(even_str)
            return redirect(url_for("sorting.odd_tips"))
        else:
            return render_template("sorting/nothingness_odd.html")

@sorting_bp.route("/del_odd")
def del_odd():
    os.system("del "+File_UPLOAD_PATH+os.sep+"奇数.txt")
    os.system("del "+File_UPLOAD_PATH+os.sep+"DownLoadBill.txt")
    return {"code":200}

@sorting_bp.route("/even_tips")
def even_tips():
    """
    偶数提示
    """
    # 检查上传的文件夹目录下是否有`奇数.txt`文件
    if "偶数.txt" in os.listdir(File_UPLOAD_PATH):
        even_list=[]
        with open(File_UPLOAD_PATH+os.sep+"偶数.txt","r") as f:
            even_list=f.readlines()
        return render_template("sorting/even_tips.html",even_list=even_list)
    else:

        if "DownLoadBill.txt" in os.listdir(File_UPLOAD_PATH):
            odd_str = ""
            even_str = ""
            # 打开文件
            with open(File_UPLOAD_PATH+os.sep+"DownLoadBill.txt", "r") as f:

                for i in f.readlines()[1:]:
                    if int(i.split(";")[9]) % 2 != 0:
                        odd_str = odd_str+i.split(";")[3]+"\n"
                    else:
                        even_str = even_str+i.split(";")[3]+"\n"
            with open(File_UPLOAD_PATH+os.sep+"奇数.txt","w") as f:
                f.write(odd_str)
            with open(File_UPLOAD_PATH+os.sep+"偶数.txt","w") as f:
                f.write(even_str)
            # time.sleep(1)
            return redirect(url_for("sorting.even_tips"))
        else:
            return render_template("sorting/nothingness_even.html")

@sorting_bp.route("/del_even")
def del_even():
    os.system("del "+File_UPLOAD_PATH+os.sep+"偶数.txt")
    os.system("del "+File_UPLOAD_PATH+os.sep+"DownLoadBill.txt")
    return {"code":200}
