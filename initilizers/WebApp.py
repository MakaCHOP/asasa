import os
import subprocess
from os import listdir


# todo
def run_web_app():
    # subprocess.check_call("rm -rf WebApp", shell=True, cwd=os.getcwd())
    #
    # if "WebApp" not in listdir(os.getcwd()):
    #     subprocess.check_call("git clone https://github.com/AmirSeraj/webtelegram.git WebApp", shell=True,
    #                           cwd=os.getcwd())
    #
    # subprocess.check_call("git fetch --all", shell=True, cwd=os.path.join(os.getcwd(), "WebApp"))
    # subprocess.check_call("git pull --all", shell=True, cwd=os.path.join(os.getcwd(), "WebApp"))
    # subprocess.check_call("git checkout websocket", shell=True, cwd=os.path.join(os.getcwd(), "WebApp"))
    # subprocess.check_call('npm install -g serve pnpm', shell=True, cwd=os.path.join(os.getcwd(), "WebApp"))
    # subprocess.check_call('pnpm install', shell=True, cwd=os.path.join(os.getcwd(), "WebApp"))
    # subprocess.check_call('pnpm run build', shell=True, cwd=os.path.join(os.getcwd(), "WebApp"))
    subprocess.check_call('PORT=3000 serve -s build', shell=True, cwd=os.path.join(os.getcwd(), "WebApp"))
