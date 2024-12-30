# 本文件是程序的安装程序
import subprocess,os
from setting import config


def main():
    try:
        with open('setting.py',encoding='utf-8') as f:
            exec(f.read())

        project_dir = config.project_path
        allure_install_path = config.allure_install_path

        # 检查是否已经安装,若未安装则执行安装程序
        if not os.path.exists(allure_install_path):

            # 创建虚拟环境
            subprocess.run([os.environ.get('python_executable', 'python'), '-m', 'venv','venv'], check=True)

            # 激活虚拟环境
            activate_script = os.path.join('venv', 'Scripts', 'activate.bat')
            activate_env = os.environ.copy()
            activate_env['VIRTUAL_ENV'] = os.path.abspath('venv')
            subprocess.run([activate_script], shell=True, env=activate_env)

            # 安装 requirements.txt 中的依赖
            subprocess.run([os.environ.get('pip_executable', 'pip'), 'install', '-r','requirements.txt'], check=True)

            # 下载 Allure
            allure_zip_path = os.path.join(project_dir, 'allure-2.21.0.zip')
            subprocess.run(['powershell', '-Command',
                            f'(New-Object Net.WebClient).DownloadFile(\'https://github.com/allure-framework/allure2/releases/download/2.21.0/allure-2.21.0.zip\', \'{allure_zip_path}\')'],
                           check=True)

            # 解压 Allure
            subprocess.run(['powershell', 'Expand-Archive', allure_zip_path, '-DestinationPath', project_dir], check=True)

            # 移动解压后的文件
            os.rename(os.path.join(project_dir, 'allure-2.21.0'), allure_install_path)

            # 赋予权限，简单示意
            subprocess.run(['icacls', allure_install_path, '/grant', 'Users:F'], check=True)

            # 删除 allure 压缩包
            os.remove(allure_zip_path)
        else:
            print(f"Allure已经安装在{allure_install_path},跳过安装")

    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"安装出错: {e}")
    finally:
        # 退出虚拟环境
        deactivate_script = os.path.join('venv', 'Scripts', 'deactivate.bat')
        print("==========================================")
        print("安装完成!")
        print("==========================================")
        if os.path.exists(deactivate_script):
            subprocess.run([deactivate_script], shell=True)


if __name__ == "__main__":
    main()