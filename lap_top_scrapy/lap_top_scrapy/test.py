# import os

# geckodriver_path = os.path.join(
#     os.path.dirname(os.path.abspath(__file__)),
#     r"..\utils\geckodriver.exe",
# )

# print(os.path.exists(geckodriver_path))



# from pathlib import Path

# # Получаем путь к корню проекта
# project_root = Path(__file__).resolve().parent.parent

# # Указываем путь к geckodriver
# geckodriver_path = project_root / "utils" / "geckodriver.exe"
# print(geckodriver_path)



from pathlib import Path
from openpyxl import load_workbook
from scrapy.utils.project import get_project_settings


settings = get_project_settings()

path_config = settings.get("CONFIGFILE_PATH")

print(path_config)