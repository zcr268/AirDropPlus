import os
import shutil
import subprocess

# 切换到本脚本所在目录（src/），使下方所有相对路径（translations、config、
# static、templates）无论从哪个工作目录调用都能正确解析。
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def build():
    # Clean previous build
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')

    subprocess.run(['pybabel', 'compile', '-d', 'translations'])

    # config.ini 不纳入版本库（含隐私数据）。打包分发给最终用户，需用干净模板，
    # 避免把开发者本机的隐私数据打进程序。打包前临时用模板覆盖，打包后恢复本机配置。
    config_ini = os.path.join('config', 'config.ini')
    config_example = os.path.join('config', 'config.ini.example')
    backup = None
    if os.path.exists(config_example):
        if os.path.exists(config_ini):
            backup = config_ini + '.devbak'
            shutil.copy(config_ini, backup)
        shutil.copy(config_example, config_ini)

    try:
        subprocess.run([
            'pyinstaller',
            '--name=AirDropPlus',
            '--icon=static/icon.ico',
            '--add-data=translations;translations',
            '--add-data=static;static',
            '--add-data=config;config',
            '--add-data=templates;templates',
            '--noconsole',
            '--hidden-import=winrt.windows.foundation.collections',
            '--clean',
            '-w',
            'AirDropPlus.py'
        ])
    finally:
        # 恢复开发者本机的真实配置
        if backup:
            shutil.move(backup, config_ini)

if __name__ == '__main__':
    build()