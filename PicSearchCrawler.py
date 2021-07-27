import os
from multiprocessing import Pool, cpu_count
from selenium import webdriver

path = r"C:\Users\Lenovo\Desktop\pics"


def run():
    num_process = cpu_count()
    pool = Pool(num_process)
    result = partition(imgList(path),num_process)


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
        self.option = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=self.option)



