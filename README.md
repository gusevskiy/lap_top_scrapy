## Паук для сбора отзывов на ноутбуки, для последующего анализа на негатив/позитив
Scrapy в данном проекте больше выступает как удобная оболочка для работы с Selenium

Данный паук открывает сайт по продаже ноутбуков с заранее заданными характеристиками. Отбирает нужные объявления, открывает каждое, и собирает два последних отзыва с самой низкой оценкой.

### Инструкция (на примере windows)
```bash
mkdir lap_top_scrapy

py -3.12 -m venv venv

python -m venv venv

git clone https://github.com/gusevskiy/lap_top_scrapy.git

./venv/Scripts/activate

pip install -r requirements.txt
```
В фале `settings.py` заменить на свои proxy и user-agentы
```bash
USER_AGENT_LIST = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
] 

PROXY_LIST = [
    'https://188.130.186.172:1050',
]
```

В папке корневой папке находится файл `config.xlsx` в нем указать нужные характеристики согласно описанию указанному в нем же.

### Запуск
```bash
cd lap_top_scrapy
scrapy crawl lap_top -O lap_top.json
```
* в файле `lap_top.json` будут данные в формате ключ: значение (модель ноутбука: два отзова)
* Ведется логирование каждого запуска в отдельном файле `logs`

#### При разработке использовался 
python==3.12  
Scrapy==2.11.2  
openpyxl==3.1.5  
scrapy-selenium==0.0.7  
selenium==4.25.0  

#### Доработки (в планах)
* выпилить scrapy-selenium (не обновляется и часть логики у него не работает)
* развертывание на сервере
* запуск по команде с доставкой результата
* настройка CI/CD
