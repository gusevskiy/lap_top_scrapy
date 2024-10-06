import logging
import time
import os
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from lap_top_scrapy.utils.create_url import main_url_create

logger = logging.getLogger()


class QuotesSpider(scrapy.Spider):
    name = "lap_top"

    def start_requests(self):
        time.sleep(3)
        # путь передаю так, можно и через .env
        start_url, dict_config = main_url_create()
        logger.info(start_url)
        
        yield SeleniumRequest(
            url=start_url,
            wait_time=10,
            script="window.scrollTo(0, document.body.scrollHeight);",
            callback=self.parse,
            # можно и другие настройки из конфига передавать, если появятся
            meta={
                "count_element": dict_config["count_elm"],
                "reviews": dict_config["reviews"],
            },
        )

    def parse(self, response):
        time.sleep(10)
        driver = response.request.meta["driver"]

        # кол-во элементов задано в config.xlsx
        count_element = response.meta["count_element"]
        reviews = response.meta["reviews"]
        logger.info(f"нужно обработать {count_element} объявлений.")

        # получаем все элементы на странице
        count_elements = response.xpath("//div[@class='_1ENFO']")
        flag_count_elements = 0
        logger.info(f"all elements: {len(count_elements)}")
        for element in count_elements:
            # кол-во оценок
            score = element.xpath("./div[3]/span[2]/text()").get()

            # выходим из цикла если нужно кол-во объявлений обработано
            if flag_count_elements >= count_element:
                break

            # если оценки нет или она < 10 то пропускаем этот элемент, скорее всего это из за рубежа и там еще нет отзывов
            if score is not None and int(score.split()[2]) > reviews:
                # прибавляем счетчик обработанных объявлений
                flag_count_elements += 1

                # ссылка для перехода к элементу
                href = f"https://market.yandex.ru/{element.xpath('./div/div/a/@href').get()}"

                # перешли к элементу
                driver.get(href)
                logger.info(f"True review: {href}")
                time.sleep(2)

                # клик по строке рейтинга и оценок для перехода в отзовы
                driver.find_element(
                    By.XPATH, "//div[@class='_23gJ9']//div[@class='_3KaoG cia-vs']//a"
                ).click()
                logger.info("go to reviews page")
                time.sleep(2)

                # кликаем по отзывам с 1й 2мя и 3мя звездами.
                # таким способом останутся только отзовы с наименьшими оценками
                for i in range(1, 4):
                    # если строки с каким то рейтингом отзывов нет то просто пропускаем.
                    try:
                        driver.find_element(
                            By.XPATH,
                            f"//div[@class='_26Jvk']//div[@data-rate='{i}']/preceding-sibling::span",
                        ).click()
                        time.sleep(1)
                    except:
                        continue
                logger.info("переходим к отзывам")
                yield from self.review_parse(driver)
            else:
                logger.info(f"False review: {href}")

    def review_parse(self, driver):
        try:
            # driver = response.request.meta["driver"]
            logger.info("start append review")
            time.sleep(2)
            # Название ноутбука и его краткие характеристики
            description = driver.find_element(
                By.XPATH, "//h1[@data-auto='productCardTitle']"
            ).text
            # кнопка фильтрации по оценке, чтобы отзовы отсортировались от max -> min
            driver.find_element(By.XPATH, "//*[text()='по оценке']").click()
            # всего отзовов
            review_count = driver.find_elements(
                By.XPATH, "//div[@data-auto='review-description']"
            )
            # берем два самых последних с минимальной оценкой, по индексу из общего массива
            reviews = []
            for number in range(
                len(review_count) - 1, max(len(review_count) - 3, -1), -1
            ):
                review = review_count[number].text
                reviews.append(f"отзыв {number} - {review.replace("\n", " ")}")
                logger.info(review)

            time.sleep(2)

            yield {
                "description": description,
                "reviews": reviews,
            }
        except NoSuchElementException as e:
            logger.exception(f"reviews not found {str(e)}")
