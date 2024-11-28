import os

os.system("pytest -s -q --alluredir=./temps")
os.system("allure serve ./temps/ -o ./temps/ --clean")