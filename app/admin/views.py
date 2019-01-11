# 从模块的初始化文件中导入蓝图。
from app import admin


# 路由定义使用装饰器进行定义
@admin.route("/")
def index():
    return "<h1 style='color:red'>this is admin</h1>"