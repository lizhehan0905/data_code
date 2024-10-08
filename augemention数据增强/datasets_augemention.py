# import cv2
# import math
# import numpy as np
# import os
# import xml.etree.ElementTree as ET
# import random
# import xml.dom.minidom as DOC
# from skimage import exposure
#
#
# # 从xml文件中提取bounding box信息, 格式为[[x_min, y_min, x_max, y_max, name]]
# def parse_xml(xml_path):
#     '''
#     输入：
#         xml_path: xml的文件路径
#     输出：
#         从xml文件中提取bounding box信息, 格式为[[x_min, y_min, x_max, y_max, name]]
#     '''
#     tree = ET.parse(xml_path)
#     root = tree.getroot()
#     objs = root.findall('object')
#     coords = list()
#     for ix, obj in enumerate(objs):
#         name = obj.find('name').text
#         box = obj.find('bndbox')
#         x_min = int(box[0].text)
#         y_min = int(box[1].text)
#         x_max = int(box[2].text)
#         y_max = int(box[3].text)
#         coords.append([x_min, y_min, x_max, y_max, name])
#     return coords
#
#
# # 将bounding box信息写入xml文件中, bouding box格式为[[x_min, y_min, x_max, y_max, name]]
# def generate_xml(img_name, coords, img_size, out_root_path):
#     '''
#     输入：
#         img_name：图片名称，如a.jpg
#         coords:坐标list，格式为[[x_min, y_min, x_max, y_max, name]]，name为概况的标注
#         img_size：图像的大小,格式为[h,w,c]
#         out_root_path: xml文件输出的根路径
#     '''
#     doc = DOC.Document()  # 创建DOM文档对象
#
#     annotation = doc.createElement('annotation')
#     doc.appendChild(annotation)
#
#     title = doc.createElement('folder')
#     title_text = doc.createTextNode('VOC2007')
#     title.appendChild(title_text)
#     annotation.appendChild(title)
#
#     title = doc.createElement('filename')
#     title_text = doc.createTextNode(img_name)
#     title.appendChild(title_text)
#     annotation.appendChild(title)
#
#     source = doc.createElement('source')
#     annotation.appendChild(source)
#
#     title = doc.createElement('database')
#     title_text = doc.createTextNode('The VOC2007 Database')
#     title.appendChild(title_text)
#     source.appendChild(title)
#
#     title = doc.createElement('annotation')
#     title_text = doc.createTextNode('PASCAL VOC2007')
#     title.appendChild(title_text)
#     source.appendChild(title)
#
#     size = doc.createElement('size')
#     annotation.appendChild(size)
#
#     title = doc.createElement('width')
#     title_text = doc.createTextNode(str(img_size[1]))
#     title.appendChild(title_text)
#     size.appendChild(title)
#
#     title = doc.createElement('height')
#     title_text = doc.createTextNode(str(img_size[0]))
#     title.appendChild(title_text)
#     size.appendChild(title)
#
#     title = doc.createElement('depth')
#     title_text = doc.createTextNode(str(img_size[2]))
#     title.appendChild(title_text)
#     size.appendChild(title)
#
#     for coord in coords:
#         object = doc.createElement('object')
#         annotation.appendChild(object)
#
#         title = doc.createElement('name')
#         title_text = doc.createTextNode(coord[4])
#         title.appendChild(title_text)
#         object.appendChild(title)
#
#         pose = doc.createElement('pose')
#         pose.appendChild(doc.createTextNode('Unspecified'))
#         object.appendChild(pose)
#         truncated = doc.createElement('truncated')
#         truncated.appendChild(doc.createTextNode('1'))
#         object.appendChild(truncated)
#         difficult = doc.createElement('difficult')
#         difficult.appendChild(doc.createTextNode('0'))
#         object.appendChild(difficult)
#
#         bndbox = doc.createElement('bndbox')
#         object.appendChild(bndbox)
#         title = doc.createElement('xmin')
#         title_text = doc.createTextNode(str(int(float(coord[0]))))
#         title.appendChild(title_text)
#         bndbox.appendChild(title)
#         title = doc.createElement('ymin')
#         title_text = doc.createTextNode(str(int(float(coord[1]))))
#         title.appendChild(title_text)
#         bndbox.appendChild(title)
#         title = doc.createElement('xmax')
#         title_text = doc.createTextNode(str(int(float(coord[2]))))
#         title.appendChild(title_text)
#         bndbox.appendChild(title)
#         title = doc.createElement('ymax')
#         title_text = doc.createTextNode(str(int(float(coord[3]))))
#         title.appendChild(title_text)
#         bndbox.appendChild(title)
#
#     # 将DOM对象doc写入文件
#     f = open(os.path.join(out_root_path, "shift_img" + img_name[:-4] + '.xml'), 'w')
#     f.write(doc.toprettyxml(indent=''))
#     f.close()
#
#
# class ImgAugemention():
#     def __init__(self, crop_rate=0.5, shift_rate=0.5, change_light_rate=0.5, add_noise_rate=0.5,
#                  cutout_rate=0.5, cut_out_length=50, cut_out_holes=1, cut_out_threshold=0.5, angle=90):
#         self.crop_rate = crop_rate
#         self.shift_rate = shift_rate
#         self.change_light_rate = change_light_rate
#         # self.cutout_rate = cutout_rate
#         self.add_noise_rate = add_noise_rate
#         # self.cut_out_length = cut_out_length
#         # self.cut_out_holes = cut_out_holes
#         # self.cut_out_threshold = cut_out_threshold
#         self.angle = angle  # rotate_img
#
#     # rotate_img
#     def rotate_image(self, src, angle, scale=1.):
#         w = src.shape[1]
#         h = src.shape[0]
#         # convet angle into rad
#         rangle = np.deg2rad(angle)  # angle in radians
#         # calculate new image width and height
#         nw = (abs(np.sin(rangle) * h) + abs(np.cos(rangle) * w)) * scale
#         nh = (abs(np.cos(rangle) * h) + abs(np.sin(rangle) * w)) * scale
#         # ask OpenCV for the rotation matrix
#         rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), angle, scale)
#         # calculate the move from the old center to the new center combined
#         # with the rotation
#         rot_move = np.dot(rot_mat, np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0]))
#         # the move only affects the translation, so update the translation
#         # part of the transform
#         rot_mat[0, 2] += rot_move[0]
#         rot_mat[1, 2] += rot_move[1]
#         # map
#         return cv2.warpAffine(
#             src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))),
#             flags=cv2.INTER_LANCZOS4)
#
#     def rotate_xml(self, src, xmin, ymin, xmax, ymax, angle, scale=1.):
#         w = src.shape[1]
#         h = src.shape[0]
#         rangle = np.deg2rad(angle)  # angle in radians
#         # now calculate new image width and height
#         # get width and heigh of changed image
#         nw = (abs(np.sin(rangle) * h) + abs(np.cos(rangle) * w)) * scale
#         nh = (abs(np.cos(rangle) * h) + abs(np.sin(rangle) * w)) * scale
#         # ask OpenCV for the rotation matrix
#         rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), angle, scale)
#         # calculate the move from the old center to the new center combined
#         # with the rotation
#         rot_move = np.dot(rot_mat, np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0]))
#         # the move only affects the translation, so update the translation
#         # part of the transform
#         rot_mat[0, 2] += rot_move[0]
#         rot_mat[1, 2] += rot_move[1]
#         # rot_mat: the final rot matrix
#         # get the four center of edges in the initial martix，and convert the coord
#         point1 = np.dot(rot_mat, np.array([(xmin + xmax) / 2, ymin, 1]))
#         point2 = np.dot(rot_mat, np.array([xmax, (ymin + ymax) / 2, 1]))
#         point3 = np.dot(rot_mat, np.array([(xmin + xmax) / 2, ymax, 1]))
#         point4 = np.dot(rot_mat, np.array([xmin, (ymin + ymax) / 2, 1]))
#         # concat np.array
#         concat = np.vstack((point1, point2, point3, point4))
#         # change type
#         concat = concat.astype(np.int32)
#         # print(concat)
#         rx, ry, rw, rh = cv2.boundingRect(concat)
#         return rx, ry, rw, rh
#
#     def process_img(self, imgs_path, xmls_path, img_save_path, xml_save_path, angle_list):
#         # xml_save_path = xml_save_path + 'rotate\\'
#         # img_save_path = img_save_path + 'rotate\\'
#         # assign the rot angles
#         for angle in angle_list:
#             for img_name in os.listdir(imgs_path):
#                 # split filename and suffix
#                 n, s = os.path.splitext(img_name)
#                 # for the sake of use yolo model, only process '.jpg'
#                 if s == ".jpg":
#                     img_path = os.path.join(imgs_path, img_name)
#                     img = cv2.imread(img_path)
#                     rotated_img = self.rotate_image(img, angle)
#                     save_name = n + "_" + str(angle) + ".jpg"
#                     # 写入图像
#                     cv2.imwrite(img_save_path + '/' + save_name, rotated_img)
#                     # print("log: [%sd] %s is processed." % (angle, img))
#                     xml_url = img_name.split('.')[0] + '.xml'
#                     xml_path = os.path.join(xmls_path, xml_url)
#                     tree = ET.parse(xml_path)
#                     # file_name = tree.find('filename').text  # it is origin name
#                     # path = tree.find('path').text  # it is origin path
#                     # change name and path
#                     tree.find('filename').text = save_name  # change file name to rot degree name
#                     # tree.find('path').text = save_name  #  change file path to rot degree name
#                     root = tree.getroot()
#                     # if angle in [90, 270], need to swap width and height
#                     if angle in [90, 270]:
#                         d = tree.find('size')
#                         width = int(d.find('width').text)
#                         height = int(d.find('height').text)
#                         # swap width and height
#                         d.find('width').text = str(height)
#                         d.find('height').text = str(width)
#
#                     for box in root.iter('bndbox'):
#                         xmin = float(box.find('xmin').text)
#                         ymin = float(box.find('ymin').text)
#                         xmax = float(box.find('xmax').text)
#                         ymax = float(box.find('ymax').text)
#                         x, y, w, h = self.rotate_xml(img, xmin, ymin, xmax, ymax, angle)
#                         # change the coord
#                         box.find('xmin').text = str(x)
#                         box.find('ymin').text = str(y)
#                         box.find('xmax').text = str(x + w)
#                         box.find('ymax').text = str(y + h)
#                         box.set('updated', 'yes')
#                     # write into new xml
#                     tree.write(xml_save_path + '/' + n + "_" + str(angle) + ".xml")
#                 # print("[%s] %s is processed." % (angle, img_name))
#
#         # 高斯模糊
#
#     def addGaussi(self, img_path, xml_path, img_save_path, xml_save_path):
#         # xml_save_path=xml_save_path+'GaussianBlur\\'
#         # img_save_path=img_save_path+'GaussianBlur\\'
#         for imgs in os.listdir(img_path):
#             img = cv2.imread(img_path + '/' + imgs)
#             size = random.choice((5, 9, 11))
#             Gau_img = cv2.GaussianBlur(img, ksize=(size, size), sigmaX=0, sigmaY=0)
#             # 写入图像
#             cv2.imwrite(img_save_path + '/' + "Gau_img" + imgs, Gau_img)
#             xml = xml_path + '/' + imgs[:-4] + ".xml"
#             tree = ET.parse(xml)
#             tree.write(xml_save_path + '/' + "Gau_img" + imgs[:-4] + ".xml")
#
#     # 调整亮度
#     def changeLight(self, img_path, xml_path, img_save_path, xml_save_path):
#
#         # xml_save_path = xml_save_path +'changeLight'
#         # img_save_path = img_save_path +'changeLight'
#         for imgs in os.listdir(img_path):
#             flag = random.uniform(0.6, 1.3)  # flag>1为调暗,小于1为调亮
#             img = cv2.imread(img_path + '/' + imgs)
#             light_img = exposure.adjust_gamma(img, flag)
#             cv2.imwrite(img_save_path + '/' + "light_img" + imgs, light_img)
#             xml = xml_path + '/' + imgs[:-4] + ".xml"
#             tree = ET.parse(xml)
#             tree.write(xml_save_path + '/' + "light_img" + imgs[:-4] + ".xml")
#
#     # 平移
#     def shift_pic_bboxes(self, xml_path, img_path, img_save_path, save_path_xml):
#         # img_save_path=img_save_path+'shift'
#         # save_path_xml=save_path_xml+'shift'
#         for xmls in os.listdir(xml_path):
#             x = xml_path + '/' + xmls
#             coords = parse_xml(x)  # 读xml文件
#             img = cv2.imread(img_path + '/' + xmls[:-4] + ".jpg")
#             names = [coord[4] for coord in coords]
#             bboxes = [coord[:4] for coord in coords]
#             '''
#             平移后的图片要包含所有的框
#             输入:
#                 img:图像array
#                 bboxes:该图像包含的所有boundingboxs,一个list,每个元素为[x_min, y_min, x_max, y_max,label],要确保是数值
#             输出:
#                 shift_img:平移后的图像array
#                 shift_bboxes:平移后的bounding box的坐标list
#             '''
#             # ---------------------- 平移图像 ----------------------
#             w = img.shape[1]
#             h = img.shape[0]
#             x_min = w  # 裁剪后的包含所有目标框的最小的框
#             x_max = 0
#             y_min = h
#             y_max = 0
#             for bbox in bboxes:
#                 x_min = min(x_min, bbox[0])
#                 y_min = min(y_min, bbox[1])
#                 x_max = max(x_max, bbox[2])
#                 y_max = max(y_max, bbox[3])
#
#             d_to_left = x_min  # 包含所有目标框的最大左移动距离
#             d_to_right = w - x_max  # 包含所有目标框的最大右移动距离
#             d_to_top = y_min  # 包含所有目标框的最大上移动距离
#             d_to_bottom = h - y_max  # 包含所有目标框的最大下移动距离
#
#             x = random.uniform(-(d_to_left - 1) / 3, (d_to_right - 1) / 3)
#             y = random.uniform(-(d_to_top - 1) / 3, (d_to_bottom - 1) / 3)
#
#             M = np.float32([[1, 0, x], [0, 1, y]])  # x为向左或右移动的像素值,正为向右负为向左; y为向上或者向下移动的像素值,正为向下负为向上
#             shift_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
#
#             # ---------------------- 平移boundingbox ----------------------
#             shift_bboxes = list()
#             for bbox in bboxes:
#                 i = 0
#                 shift_bboxes.append([bbox[0] + x, bbox[1] + y, bbox[2] + x, bbox[3] + y, names[i]])
#                 i += 1
#             cv2.imwrite(img_save_path + '/' + "shift_img" + xmls[:-4] + ".jpg", shift_img)
#             file = xmls[:-4] + ".jpg"
#             auged_img = shift_img
#             auged_bboxes = shift_bboxes
#             generate_xml(file, auged_bboxes, list(auged_img.shape), save_path_xml)
#
#     # 裁剪
#     def crop_img_bboxes(self, xml_path, img_path, img_save_path, save_path_xml):
#         '''
#         裁剪后的图片要包含所有的框
#         输入:
#             img:图像array
#             bboxes:该图像包含的所有boundingboxs,一个list,每个元素为[x_min, y_min, x_max, y_max,label],要确保是数值
#         输出:
#             crop_img:裁剪后的图像array
#             crop_bboxes:裁剪后的bounding box的坐标list
#         '''
#         # ---------------------- 裁剪图像 ----------------------
#         # img_save_path=img_save_path+'crop'
#         # save_path_xml=save_path_xml+'crop'
#         for imgs in os.listdir(img_path):
#             imgPath = img_path + imgs
#             img = cv2.imread(img_path + '/' + imgs)
#             w = img.shape[1]
#             h = img.shape[0]
#             x_min = w  # 裁剪后的包含所有目标框的最小的框
#             x_max = 0
#             y_min = h
#             y_max = 0
#             xmlPath = xml_path + '/' + imgs[:-4] + ".xml"
#             coords = parse_xml(xmlPath)  # 读xml文件
#             names = [coord[4] for coord in coords]
#             bboxes = [coord[:4] for coord in coords]
#             for bbox in bboxes:
#                 x_min = min(x_min, bbox[0])
#                 y_min = min(y_min, bbox[1])
#                 x_max = max(x_max, bbox[2])
#                 y_max = max(y_max, bbox[3])
#
#             d_to_left = x_min  # 包含所有目标框的最小框到左边的距离
#             d_to_right = w - x_max  # 包含所有目标框的最小框到右边的距离
#             d_to_top = y_min  # 包含所有目标框的最小框到顶端的距离
#             d_to_bottom = h - y_max  # 包含所有目标框的最小框到底部的距离
#
#             # 随机扩展这个最小框
#             crop_x_min = int(x_min - random.uniform(0, d_to_left))
#             crop_y_min = int(y_min - random.uniform(0, d_to_top))
#             crop_x_max = int(x_max + random.uniform(0, d_to_right))
#             crop_y_max = int(y_max + random.uniform(0, d_to_bottom))
#
#             # 确保不要越界
#             crop_x_min = max(0, crop_x_min)
#             crop_y_min = max(0, crop_y_min)
#             crop_x_max = min(w, crop_x_max)
#             crop_y_max = min(h, crop_y_max)
#
#             crop_img = img[crop_y_min:crop_y_max, crop_x_min:crop_x_max]
#
#             # ---------------------- 裁剪boundingbox ----------------------
#             # 裁剪后的boundingbox坐标计算
#             crop_bboxes = list()
#             for bbox in bboxes:
#                 i = 0
#                 crop_bboxes.append(
#                     [bbox[0] - crop_x_min, bbox[1] - crop_y_min, bbox[2] - crop_x_min, bbox[3] - crop_y_min, names[i]])
#                 i += 1
#             cv2.imwrite(img_save_path + '/' + "crop_img" + imgs, crop_img)
#             auged_img = crop_img
#             auged_bboxes = crop_bboxes
#             file = xmls[:-4] + ".jpg"
#             generate_xml(file, auged_bboxes, list(auged_img.shape), save_path_xml)
#
#             generate_xml(imgs, auged_bboxes, list(auged_img.shape), save_path_xml)
#
#
# if __name__ == '__main__':
#     img_aug = ImgAugemention()
#     # 路径修改为自己的
#     imgs_path = 'D:\\temp\\images'
#     xmls_path = 'D:\\temp\\xmls'
#     save_xml = 'D:\\temp\\new_xmls'
#     save_img = 'D:\\temp\\new_images'
#     # print("start rorate!!!")
#     # angle_list = [60, 90, 120, 150, 180, 270]
#     # img_aug.process_img(imgs_path, xmls_path, save_img, save_xml, angle_list)
#
#     print("start addGaussi!!!")
#     img_aug.addGaussi(imgs_path, xmls_path, save_img, save_xml)
#     print("start changeLight!!!")
#     img_aug.changeLight(imgs_path, xmls_path, save_img, save_xml)
#     print("start shift_pic_bboxes!!!")
#     img_aug.shift_pic_bboxes(xmls_path, imgs_path, save_img, save_xml)
#     print("start crop_img_bboxes!!!")
#     img_aug.crop_img_bboxes(xmls_path, imgs_path, save_img, save_xml)

'''
Author: CodingWZP
Email: codingwzp@gmail.com
Date: 2021-08-06 10:51:35
LastEditTime: 2021-08-09 10:53:43
Description: Image augmentation with label.
'''
import xml.etree.ElementTree as ET
import os
import imgaug as ia
import numpy as np
import shutil
from tqdm import tqdm
from PIL import Image
from imgaug import augmenters as iaa

ia.seed(1)


def read_xml_annotation(root, image_id):
    in_file = open(os.path.join(root, image_id))
    tree = ET.parse(in_file)
    root = tree.getroot()
    bndboxlist = []

    for object in root.findall('object'):  # 找到root节点下的所有country节点
        bndbox = object.find('bndbox')  # 子节点下节点rank的值

        xmin = int(bndbox.find('xmin').text)
        xmax = int(bndbox.find('xmax').text)
        ymin = int(bndbox.find('ymin').text)
        ymax = int(bndbox.find('ymax').text)
        # print(xmin,ymin,xmax,ymax)
        bndboxlist.append([xmin, ymin, xmax, ymax])
        # print(bndboxlist)

    bndbox = root.find('object').find('bndbox')
    return bndboxlist


def change_xml_list_annotation(root, image_id, new_target, saveroot, id):
    in_file = open(os.path.join(root, str(image_id) + '.xml'))  # 这里root分别由两个意思
    tree = ET.parse(in_file)
    # 修改增强后的xml文件中的filename
    elem = tree.find('filename')
    elem.text = (str(id) + '.jpg')
    xmlroot = tree.getroot()
    # 修改增强后的xml文件中的path
    elem = tree.find('path')
    if elem != None:
        elem.text = (saveroot + str(id) + '.jpg')

    index = 0
    for object in xmlroot.findall('object'):  # 找到root节点下的所有country节点
        bndbox = object.find('bndbox')  # 子节点下节点rank的值

        # xmin = int(bndbox.find('xmin').text)
        # xmax = int(bndbox.find('xmax').text)
        # ymin = int(bndbox.find('ymin').text)
        # ymax = int(bndbox.find('ymax').text)

        new_xmin = new_target[index][0]
        new_ymin = new_target[index][1]
        new_xmax = new_target[index][2]
        new_ymax = new_target[index][3]

        xmin = bndbox.find('xmin')
        xmin.text = str(new_xmin)
        ymin = bndbox.find('ymin')
        ymin.text = str(new_ymin)
        xmax = bndbox.find('xmax')
        xmax.text = str(new_xmax)
        ymax = bndbox.find('ymax')
        ymax.text = str(new_ymax)

        index = index + 1

    tree.write(os.path.join(saveroot, str(id + '.xml')))


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False
#     imgs_path = 'D:\\temp\\images'
#     xmls_path = 'D:\\temp\\xmls'
#     save_xml = 'D:\\temp\\new_xmls'
#     save_img = 'D:\\temp\\new_images'

if __name__ == "__main__":

    IMG_DIR = "D:\\temp\\images"
    XML_DIR = "D:\\temp\\xmls"

    AUG_XML_DIR = "D:\\temp\\new_xmls"  # 存储增强后的XML文件夹路径
    try:
        shutil.rmtree(AUG_XML_DIR)
    except FileNotFoundError as e:
        a = 1
    mkdir(AUG_XML_DIR)

    AUG_IMG_DIR = "D:\\temp\\new_images"  # 存储增强后的影像文件夹路径
    try:
        shutil.rmtree(AUG_IMG_DIR)
    except FileNotFoundError as e:
        a = 1
    mkdir(AUG_IMG_DIR)

    AUGLOOP = 10  # 每张影像增强的数量

    boxes_img_aug_list = []
    new_bndbox = []
    new_bndbox_list = []

    # 影像增强
    seq = iaa.Sequential([
        # iaa.Invert(0.5),
        # iaa.Fliplr(0.5),  # 镜像
        iaa.Crop(percent=(0, 0.1)),
        iaa.Multiply((0.5, 1.5)),  # change brightness, doesn't affect BBs
        iaa.GaussianBlur(sigma=(0, 3.0)),  # iaa.GaussianBlur(0.5),
        iaa.Affine(
            translate_px={"x": 15, "y": 15},
            scale=(0.8, 0.95),
        )  # translate by 40/60px on x/y axis, and scale to 50-70%, affects BBs
    ])

    for name in tqdm(os.listdir(XML_DIR), desc='Processing'):

        bndbox = read_xml_annotation(XML_DIR, name)

        # 保存原xml文件
        # shutil.copy(os.path.join(XML_DIR, name), AUG_XML_DIR)
        # 保存原图
        # og_img = Image.open(IMG_DIR + '/' + name[:-4] + '.jpg')
        # og_img.convert('RGB').save(AUG_IMG_DIR+ '/' + name[:-4] + '.jpg', 'JPEG')
        og_xml = open(os.path.join(XML_DIR, name))
        tree = ET.parse(og_xml)
        # 修改增强后的xml文件中的filename
        elem = tree.find('filename')
        elem.text = (name[:-4] + '.jpg')
        # tree.write(os.path.join(AUG_XML_DIR, name))

        for epoch in range(AUGLOOP):
            seq_det = seq.to_deterministic()  # 保持坐标和图像同步改变，而不是随机
            # 读取图片
            img = Image.open(os.path.join(IMG_DIR, name[:-4] + '.jpg'))
            # sp = img.size
            img = np.asarray(img)
            # bndbox 坐标增强
            for i in range(len(bndbox)):
                bbs = ia.BoundingBoxesOnImage([
                    ia.BoundingBox(x1=bndbox[i][0], y1=bndbox[i][1], x2=bndbox[i][2], y2=bndbox[i][3]),
                ], shape=img.shape)

                bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]
                boxes_img_aug_list.append(bbs_aug)

                # new_bndbox_list:[[x1,y1,x2,y2],...[],[]]
                n_x1 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x1)))
                n_y1 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y1)))
                n_x2 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x2)))
                n_y2 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y2)))
                if n_x1 == 1 and n_x1 == n_x2:
                    n_x2 += 1
                if n_y1 == 1 and n_y2 == n_y1:
                    n_y2 += 1
                if n_x1 >= n_x2 or n_y1 >= n_y2:
                    print('error', name)
                new_bndbox_list.append([n_x1, n_y1, n_x2, n_y2])
            # 存储变化后的图片
            image_aug = seq_det.augment_images([img])[0]
            path = os.path.join(AUG_IMG_DIR,
                                str(str(name[:-4]) + '_' + str(epoch)) + '.jpg')
            image_auged = bbs.draw_on_image(image_aug, size=0)
            Image.fromarray(image_auged).convert('RGB').save(path)

            # 存储变化后的XML
            change_xml_list_annotation(XML_DIR, name[:-4], new_bndbox_list, AUG_XML_DIR,
                                       str(name[:-4]) + '_' + str(epoch))
            # print(str(str(name[:-4]) + '_' + str(epoch)) + '.jpg')
            new_bndbox_list = []
    print('Finish!')


