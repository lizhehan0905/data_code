"""
https://blog.csdn.net/qq_51607131/article/details/128475133
"""
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import glob
import os



def search_file(data_dir, pattern=r'\.png$'):
    root_dir = os.path.abspath(data_dir)
    for root, dirs, files in os.walk(root_dir):
        for f in files:
                yield f



bdd_label_dir = r"D:\\datasets\\homemade3\\labels"
for path in search_file(bdd_label_dir, r"\.txt$"):
  txtfile = path.replace( "txt","jpg")
  txt_path = os.path.join(r"D:\\datasets\\homemade3\\images", txtfile)
  jpg_path = os.path.join(bdd_label_dir, path)
  # print("begin!")
  if not os.path.exists(txt_path):
    print(txt_path)
    # os.remove(jpg_path)
