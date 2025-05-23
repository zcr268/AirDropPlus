import io
import os
import threading
import traceback

import flask
from flask import Flask, request, Blueprint, stream_with_context

from config import Config
from notifier import Notifier
import utils
from utils import file_path_encode, avoid_duplicate_filename, file_path_decode, clean_filename
from result import Result

import clipboard


def get_clipboard_dto(clipboard_type: clipboard.Type, data):
    return {
        'type': clipboard_type.value,
        'data': data
    }


class Server:
    def __init__(self, config: Config, notifier: Notifier):
        self.config = config
        self.notifier = notifier
        self.blueprint = Blueprint('server', __name__)
        self.register_unified_process()
        self.register_test()
        self.register_file()
        self.register_clipboard()
        self.register_settings()
        self.app = Flask(__name__, template_folder='templates')
        self.app.register_blueprint(self.blueprint)

    def check_localhost(self, client_ip):
        allowed_ips = ['127.0.0.1', '::1']
        local_ip = utils.get_local_ip()
        if local_ip is not None:
            allowed_ips.append(local_ip)
        if client_ip not in allowed_ips:
            self.notifier.notify('⚠️错误:', '该接口仅允许本地访问')
            return Result.error(msg='该接口仅允许本地访问', code=403)
    def run(self, host: str, port: int):
        self.app.run(host=host, port=port)

    def run_in_thread(self, host: str, port: int):
        threading.Thread(target=lambda: self.app.run(host=host, port=port)).start()

    def register_unified_process(self):
        # 统一认证
        @self.blueprint.before_request
        def check_api_key():
            if request.path in ['/']:
                return
            if request.path.startswith('/settings'):
                return
            auth_header = request.headers.get("Authorization")
            if auth_header != self.config.key:
                self.notifier.notify("⚠️错误:", "密钥错误")
                return Result.error(msg='密钥错误', code=401)
            version = request.headers.get("ShortcutVersion")
            client_version = '.'.join(self.config.version.split('.')[:2])
            if '.'.join(version.split('.')[:2]) != client_version:
                msg = f'''版本不匹配\n\nWindows版本为：{self.config.version}\n快捷指令版本为：{version}'''
                self.notifier.notify("⚠️错误:", msg)
                return Result.error(msg=msg, code=400)

        # 统一异常处理
        @self.blueprint.errorhandler(Exception)
        def handle_all_exceptions(error):
            traceback.print_exc()
            msg = str(error)
            self.notifier.notify('⚠️错误:', msg)
            return Result.error(msg, 500)

    def register_test(self):
        @self.blueprint.route('/')
        def test():
            self.notifier.notify("Test", "🌎Hello World!")
            return '🌎Hello world!'

    def register_file(self):
        @self.blueprint.route('/file', methods=['POST'])
        def send_file():
            """
            手机端发送文件
            Body(Form):
                - file: file
            """
            if 'file' not in request.files:
                return Result.error(msg="文件不存在")
            file = request.files['file']
            filename = clean_filename(file.filename)
            new_filename = avoid_duplicate_filename(self.config.save_path, filename)
            file_path = os.path.join(self.config.save_path, new_filename)
            with open(file_path, 'wb') as f:
                for chunk in stream_with_context(file.stream):
                    if chunk:
                        f.write(chunk)
            self.notifier.show_file(self.config.save_path, new_filename, filename)
            return Result.success(msg="发送成功")

        # 获取电脑端文件
        @self.blueprint.route('/file/<path>', methods=['GET'])
        def receive_file(path):
            """ 电脑端发送文件 """
            path = file_path_decode(path)
            if path is None:
                self.notifier.notify("⚠️错误：", "文件路径解析出错")
                return
            basename = os.path.basename(path)
            with open(path, 'rb') as f:
                file_content = f.read()
            self.notifier.notify("📄发送文件:", basename)
            return flask.send_file(io.BytesIO(file_content), as_attachment=True, download_name=basename)

    def register_clipboard(self):
        @self.blueprint.route('/clipboard')
        def receive_clipboard():
            """ 电脑端发送剪贴板 """
            # 文本
            success, res = clipboard.get_text()
            if success:
                dto = get_clipboard_dto(clipboard.Type.TEXT, res)
                self.notifier.notify('📝发送剪贴板文本:', res)
                return Result.success(data=dto)
            # 文件
            success, res = clipboard.get_files()
            if success:
                file_path_enc_list = [file_path_encode(path) for path in res]
                dto = get_clipboard_dto(clipboard.Type.FILE, file_path_enc_list)
                return Result.success(data=dto)
            # 图片
            success, res = clipboard.get_img_base64()
            if success:
                dto = get_clipboard_dto(clipboard.Type.IMG, res)
                self.notifier.notify('🏞️发送剪贴板图片', "")
                return Result.success(data=dto)

            self.notifier.notify('⚠️发送剪贴板出错:', 'Windows剪贴板为空')
            return Result.error(msg='Windows剪贴板为空')

        # 接收手机端剪贴板
        @self.blueprint.route('/clipboard', methods=['POST'])
        def send_clipboard():
            """
            手机端发送剪贴板
            Body(Form):
                - clipboard: clipboard contents
            """
            text = request.form['clipboard']
            if text is None or text == '':
                self.notifier.notify('⚠️设置剪贴板出错:', ' iPhone剪贴板为空')
                return Result.error(msg='iPhone剪贴板为空')
            success, msg = clipboard.set_text(text)
            if success:
                self.notifier.notify('📝设置剪贴板文本:', text)
            else:
                self.notifier.notify('⚠️设置剪贴板出错:', msg)
            return Result.success(msg='发送成功') if success else Result.error(msg=msg)
    
    def register_settings(self):
        # 配置页面
        @self.blueprint.route('/settings')
        def settings_page():
            self.check_localhost(request.remote_addr)
            return flask.render_template('settings.html', config=self.config)

        @self.blueprint.route('/settings/configs')
        def get_configs():
            localhost_result = self.check_localhost(request.remote_addr)
            if localhost_result is not None:
                return localhost_result
            config_dict = {
                'key': self.config.key,
                'save_path': self.config.save_path,
                'port': self.config.port,
                'basic_notifier': self.config.basic_notifier,
                'show_icon': self.config.show_icon,
                'version': self.config.version,
            }
            return Result.success(data=config_dict)

        @self.blueprint.route('/settings/configs', methods=['POST'])
        def set_configs():
            localhost_result = self.check_localhost(request.remote_addr)
            if localhost_result is not None:
                return localhost_result
            config_dict = request.json
            update_state = self.config.update(config_dict)
            if update_state is not None:
                self.notifier.notify("⚙️设置", "配置保存失败：" + update_state[0].json['msg'])
                return update_state
            self.notifier.notify("⚙️设置", "配置已保存")
            return Result.success(data=config_dict)