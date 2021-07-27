import os
from multiprocessing import Pool, cpu_count

path = r"C:\Users\Lenovo\Desktop\pics"


def run():
    num_process = cpu_count()
    pool = Pool(num_process)


def imgList(path):
    file_list = []
    file = os.listdir(path)
    for img in file:
        file_list.append(img)
    return file_list

# def partition():

