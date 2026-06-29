import configparser
import os
from result import Result
from utils import is_port_in_use, get_system_language
import i18n
from i18n import _

SUPPORTED_LANGUAGES = ['en', 'ru', 'zh']

class Config:
    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding='utf-8')

        self.config_path = config_path
        self.key = self.config.get('config', 'key')
        self.save_path = self.config.get('config', 'save_path')
        if self.save_path == '' or self.save_path is None:
            self.save_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        self.port = int(self.config.get('config', 'port'))
        self.basic_notifier = self.config.get('config', 'basic_notifier')=='1'
        self.show_icon = self.config.get('config', 'show_icon') == '1'
        self.version = self.config.get('info', 'version')
        
        # Add language configuration
        # language_setting 为配置中的原始值（可能是 'auto'，表示跟随系统），用于前端回显；
        # language 为实际生效语言（en/ru/zh），供 i18n 渲染使用。
        # 'auto' / 空 / 缺失 时按操作系统语言解析（无法匹配则默认英文），但不覆盖配置里的 'auto'。
        lang = self.config.get('config', 'language', fallback='auto')
        if lang in ('', None):
            lang = 'auto'
        self.language_setting = lang
        if lang == 'auto':
            self.language = get_system_language(SUPPORTED_LANGUAGES, default='en')
        else:
            self.language = lang

    def update(self, data):
        if not os.path.exists(data['save_path']):
            return Result.success(msg=_('Directory "%(path)s" does not exist, please check', path=data['save_path']))

        port_int = int(data['port'])
        if port_int < 1024 or port_int > 65535:
            return Result.success(msg=_('Port number must be between 1024 and 65535'))

        if port_int != int(self.port) and is_port_in_use(port_int):
            return Result.success(msg=_('Port %(port)s is already in use, please change', port=data['port']))

        self.config.set('config', 'key', data['key'])
        self.config.set('config', 'save_path', data['save_path'])
        self.config.set('config', 'port', str(data['port']))
        self.config.set('config', 'basic_notifier', str(int(data['basic_notifier'])))
        self.config.set('config', 'show_icon', str(int(data['show_icon'])))
        self.config.set('config', 'language', data['language'])

        self.key = data['key']
        self.save_path = data['save_path']
        self.port = data['port']
        self.basic_notifier = data['basic_notifier']
        self.show_icon = data['show_icon']
        # 保留原始设定（可能是 auto），并解析出实际生效语言
        self.language_setting = data['language']
        if data['language'] == 'auto':
            self.language = get_system_language(SUPPORTED_LANGUAGES, default='en')
        else:
            self.language = data['language']
        # 通知国际化模块切换语言，使桌面通知/托盘/模板全局即时生效
        i18n.set_language(self.language)

        self.config.write(open(self.config_path, 'w', encoding='utf-8'))

    def save_port(self, port):
        """仅更新并持久化端口，用于启动时自动换端口的场景。"""
        self.port = port
        self.config.set('config', 'port', str(port))
        self.config.write(open(self.config_path, 'w', encoding='utf-8'))