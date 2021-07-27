import os
from multiprocessing import Pool, cpu_count

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

path = r"C:\Users\Lenovo\Desktop\pics"


def run():
    num_process = cpu_count()
    pool = Pool(num_process)
    result = partition(imgList(path), num_process)


def imgList(path):
    file_list = []
    file = os.listdir(path)
    for img in file:
        file_list.append(img)
    return file_list


def partition(ls, size):
    num_per_list = len(ls) // size
    result = []
    if num_per_list * size == len(ls):
        for i in range(size):
            result.append(ls[num_per_list * i:num_per_list * (i + 1)])
    else:
        for i in range(size - 1):
            result.append(ls[num_per_list * i:num_per_list * (i + 1)])
        result.append(ls[num_per_list * (size - 1):])
    return result


class GooglePicSearcher:
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.option = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=self.option)

    def upload_img(self):
        self.driver.get("https://images.google.com")

        # 等待相机按钮出现
        condition_1 = EC.visibility_of_element_located(
            (By.CLASS_NAME, "LM8x9c"))
        WebDriverWait(self.driver, timeout=20,
                      poll_frequency=0.5).until(condition_1)
        # 相机按钮出现后点击
        image_button = self.driver.find_element_by_class_name("LM8x9c")
        image_button.send_keys(Keys.ENTER)

        # 等待出现上传图片字样
        condition_2 = EC.visibility_of_element_located(
            (By.ID, "dRSWfb"))
        WebDriverWait(self.driver, timeout=20, poll_frequency=0.5).until(
            condition_2)

        # 点击上传图片
        upload = self.driver.find_element_by_xpath('//*[@id="dRSWfb"]/div/a')
        upload.send_keys(Keys.ENTER)

