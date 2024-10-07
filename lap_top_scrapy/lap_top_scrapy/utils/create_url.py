"""параметры для поиска ноутбуков по заданым параметрам"""

from openpyxl import load_workbook
from scrapy.utils.project import get_project_settings
settings = get_project_settings()


def main_url_create():
    """Формирует main_url по данным из config.xlsx"""
    
    path_config = settings.get("CONFIGFILE_PATH")
    print(path_config)
    wb = load_workbook(path_config)
    sheet = wb.active
    # читаем только ячейки с нужными данными
    data = sheet["A2":"B15"]

    # Словари с параметрами, по ключу нужно подставить эти значения в адресную строку
    # т.е. в этих цифрах зашифрованы значения у yandex-market в адресной строке

    # значения добавил не прям все, а так можно хоть все фильтры сюда перенести

    dict_hard_disk = {256: "39025878", 512: "39025848", 1: "39025873"}
    dict_processor = {
        "amd": "50198831%2C50198796%2C50198830%2C50198806%2C53327653%2C50198854%2C53327625%2C53327674%2C53327627%2C53327684%2C50198838%2C50198858%2C50198832%2C50198810%2C53327636%2C50198848%2C53327662%2C53327685",
        "intel": "50198855%2C50198821%2C50198840%2C50198812%2C50198785%2C50198782%2C53327620%2C50198857%2C53327651%2C53790795%2C53766350%2C53327638%2C50198862%2C50198798%2C53327673%2C53327687%2C50198807%2C54381314%2C54709156%2C54646910",
    }
    dict_ram = {8: "24892650", 12: "24892692", 16: "24892630"}
    dict_sort = {
        "подешевле": "aprice",
        "подороже": "dprice",
        "высокий рейтинг": "rating",
    }
    # словарь для хранения данных из Config.xlsx
    dict_config = {}
    # заполняем dict_config
    for row in data:
        dict_config[row[0].value] = row[1].value

    battery_life = ""
    sort = ""
    ram = ""
    processor = ""
    hard_disk = ""
    weight = ""
    four_rating = ""
    # если ячейка была не пустой, то заполняем переменные в соответствии с введеными значениями
    # если была пустая, ни чего не подставится и фильтр просто не применится.
    if dict_config.get("battery_life", "") != "":
        battery_life = f"&glfilter=24083873%3A{dict_config['battery_life']}"

    if dict_config.get("sort", "") != "":
        sort = f"&how={dict_sort.get(dict_config['sort'], '')}"

    if dict_config.get("ram", "") != "":
        ram = f"&glfilter=24892510%3A{dict_ram.get(dict_config['ram'], '')}"

    if dict_config.get("processor", "") != "":
        processor = (
            f"&glfilter=37331890%3A{dict_processor.get(dict_config['processor'], '')}"
        )

    if dict_config.get("hard_disk", "") != "":
        hard_disk = (
            f"&glfilter=37699290%3A{dict_hard_disk.get(dict_config['hard_disk'], '')}"
        )

    if dict_config.get("weight", "") != "":
        weight = f"&glfilter=23674510%3A{dict_config['weight']}"

    if dict_config.get("four_rating", "") != "":
        four_rating = f"&qrfrom={dict_config['four_rating']}"

    # Формируем URL с фильтрами по этому URL будет переходить скрапер
    main_url = (
        f"https://market.yandex.ru/catalog--noutbuki/26895412/list?hid=91013{sort}"
        f"&glfilter=21194330%3A36779198{processor}{ram}{hard_disk}{weight}{battery_life}"
        f"&resale_goods=resale_new{four_rating}"
    )

    return main_url, dict_config


if __name__ == "__main__":
    print(main_url_create())
