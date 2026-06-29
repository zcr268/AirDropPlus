import os
import signal
import sys
import time

from PIL import Image

import i18n
from config import Config
import utils
from notifier import Notifier
from server import Server

from pystray import Icon, MenuItem
import webbrowser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(SCRIPT_DIR, 'config', 'config.ini')
config = Config(config_file_path)

# 初始化国际化：资源目录 + 配置中解析出的生效语言。须在任何 _() 调用前完成。
i18n.init(os.path.join(SCRIPT_DIR, 'translations'), config.language)
from i18n import _

notifier = Notifier(config.basic_notifier)


def create_icon():
    def on_exit(icon, item):
        notifier.notify(_('AirDrop Plus'), "👋 " + _('Exit'))
        icon.stop()
        os.kill(os.getpid(), signal.SIGINT)

    def on_web_config(icon, item):
        url = f"http://localhost:{config.port}/settings"
        try:
            webbrowser.open(url)
            notifier.notify(_('AirDrop Plus'), "🌐 " + _('Opened localhost in default browser'))
        except Exception as e:
            notifier.notify("⚠️ " + _('AirDrop Plus'), _('Failed to open browser:') + str(e))

    menu = (
        MenuItem(text=_('Settings'), action=on_web_config),
        MenuItem(text=_('Exit'), action=on_exit),
    )
    image = Image.open(os.path.join(SCRIPT_DIR, 'static', 'icon.ico'))
    icon = Icon(_('AirDrop Plus'), image, _('AirDrop Plus'), menu)
    icon.run()


def resolve_port() -> bool:
    """启动前检测端口占用。若被占用则自动换一个可用端口并写入配置，
    同时弹出警告通知，提醒用户同步修改 iPhone 快捷指令里的端口。

    返回 True 表示有可用端口（无论是否更换），False 表示找不到可用端口。
    """
    if not utils.is_port_in_use(config.port):
        return True
    old_port = config.port
    new_port = utils.find_available_port(old_port + 1)
    if new_port is None:
        return False
    config.save_port(new_port)
    notifier.notify(
        "⚠️ " + _('Port changed'),
        _('Port %(old)s is in use, changed to %(new)s.\nPlease update the port in your iPhone Shortcut settings.',
          old=old_port, new=new_port)
    )
    return True


def start_server() -> tuple[bool, str]:
    if not os.path.exists(config.save_path):
        return False, _('Directory "%(path)s" does not exist, please check configuration file', path=config.save_path)
    try:
        server = Server(config, notifier)
        server.run_in_thread('0.0.0.0', config.port)
    except Exception as e:
        return False, _('Error message: %(error)s', error=str(e))
    return True, _('Port: %(port)s\nSave path: %(path)s', port=config.port, path=config.save_path)


if __name__ == '__main__':
    if not resolve_port():
        notifier.notify("⚠️ " + _('Start failed'), _('No available port found'))
        sys.exit()
    flag, msg = start_server()
    if flag:
        notifier.notify("🚀 " + _('Started'), msg)
    else:
        notifier.notify("⚠️ " + _('Start failed'), msg)
        sys.exit()
    if config.show_icon:
        create_icon()
    else:
        while True:
            time.sleep(10)
