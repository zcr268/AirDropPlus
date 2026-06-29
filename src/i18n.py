"""轻量国际化模块，基于标准库 gettext。

设计目标：
- 单用户桌面应用，语言来自配置文件的单一设定，而非每个 HTTP 请求协商；
- 桌面通知（主线程）、托盘菜单、HTTP 请求、Jinja 模板共用同一个翻译器；
- 切换语言时全局立即生效，无需任何 Flask app context 包裹。

用法：
    import i18n
    i18n.init('translations', 'zh')   # 启动时调用一次
    from i18n import _
    _('Settings')                      # -> '设置'
    _('Port %(port)s is already in use', port=8888)
    i18n.set_language('en')            # 运行期切换，全局生效
"""
import gettext as _gettext

# 翻译资源所在目录（translations/<lang>/LC_MESSAGES/messages.mo），init 时记录，供切换语言复用。
_localedir = None
# 当前生效的翻译器，默认 NullTranslations 表示原样返回（未 init 时也不报错）。
_translation = _gettext.NullTranslations()


def init(localedir: str, lang: str):
    """初始化国际化，记录资源目录并加载初始语言。"""
    global _localedir
    _localedir = localedir
    set_language(lang)


def set_language(lang: str):
    """切换当前语言，全局立即生效。fallback=True 时缺失语言/条目原样返回 msgid。"""
    global _translation
    if _localedir is None:
        return
    _translation = _gettext.translation(
        'messages', localedir=_localedir, languages=[lang], fallback=True
    )


def gettext(message, **kwargs):
    """翻译并按命名占位符（%(name)s）做插值，兼容原 flask_babel 的调用方式。"""
    text = _translation.gettext(message)
    return text % kwargs if kwargs else text


# 与原代码保持一致的简写别名。
_ = gettext
