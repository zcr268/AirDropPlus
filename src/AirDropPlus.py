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


def start_server() -> tuple[bool, str]:
    if not os.path.exists(config.save_path):
        return False, _('Directory "%(path)s" does not exist, please check configuration file', path=config.save_path)
    if utils.is_port_in_use(config.port):
        return False, _('Port %(port)s is already in use', port=config.port)
    try:
        server = Server(config, notifier)
        server.run_in_thread('0.0.0.0', config.port)
    except Exception as e:
        return False, _('Error message: %(error)s', error=str(e))
    return True, _('Port: %(port)s\nSave path: %(path)s', port=config.port, path=config.save_path)


if __name__ == '__main__':
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
