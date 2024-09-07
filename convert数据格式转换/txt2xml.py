# # .txt-->.xml
# # ! /usr/bin/python
# # -*- coding:UTF-8 -*-
# import os
# import cv2
#
#
# def txt_to_xml(txt_path, img_path, xml_path):
#     # 1.字典对标签中的类别进行转换
#     dict = {'0': "red", '1': "yellow", '2': "green", '3': "redleft",
#             '4': "redright", '5': "greenleft", '6': "greenright", '7': "redforward",
#             '8': "greenforward", '9': "yellowleft", '10': "yellowright", '11': "yellowforward",
#             '12': "redturn", '13': "greenturn", '14': "yellowturn", '15': "off" }
#     # 2.找到txt标签文件夹
#     files = os.listdir(txt_path)
#     # 用于存储 "老图"
#     pre_img_name = ''
#     # 3.遍历文件夹
#     for i, name in enumerate(files):
#         # 许多人文件夹里有该文件，默认的也删不掉，那就直接pass
#         if name == "desktop.ini":
#             continue
#         print(name)
#         # 4.打开txt
#         txtFile = open(txt_path + name)
#         # 读取所有内容
#         txtList = txtFile.readlines()
#         # 读取图片名称
#         img_name = name.split(".")[0]
#         # print(img_path + img_name + ".jpg")
#         pic = cv2.imread(img_path + img_name + ".jpg")
#         # 获取图像大小信息
#         Pheight, Pwidth, Pdepth = pic.shape
#         # 5.遍历txt文件中每行内容
#         for row in txtList:
#             # 按' '分割txt的一行的内容
#             oneline = row.strip().split(" ")
#             # 遇到的是一张新图片
#             if img_name != pre_img_name:
#                 # 6.新建xml文件
#                 xml_file = open((xml_path + img_name + '.xml'), 'w')
#                 xml_file.write('<annotation>\n')
#                 xml_file.write('    <folder>VOC2007</folder>\n')
#                 xml_file.write('    <filename>' + img_name + '.jpg' + '</filename>\n')
#                 xml_file.write('<source>\n')
#                 xml_file.write('<database>orgaquant</database>\n')
#                 xml_file.write('<annotation>organoids</annotation>\n')
#                 xml_file.write('</source>\n')
#                 xml_file.write('    <size>\n')
#                 xml_file.write('        <width>' + str(Pwidth) + '</width>\n')
#                 xml_file.write('        <height>' + str(Pheight) + '</height>\n')
#                 xml_file.write('        <depth>' + str(Pdepth) + '</depth>\n')
#                 xml_file.write('    </size>\n')
#                 xml_file.write('    <object>\n')
#                 xml_file.write('<name>' + dict[oneline[0]] + '</name>\n')
#                 xml_file.write('        <bndbox>\n')
#                 xml_file.write('            <xmin>' + str(
#                     int(((float(oneline[1])) * Pwidth + 1) - (float(oneline[3])) * 0.5 * Pwidth)) + '</xmin>\n')
#                 xml_file.write('            <ymin>' + str(
#                     int(((float(oneline[2])) * Pheight + 1) - (float(oneline[4])) * 0.5 * Pheight)) + '</ymin>\n')
#                 xml_file.write('            <xmax>' + str(
#                     int(((float(oneline[1])) * Pwidth + 1) + (float(oneline[3])) * 0.5 * Pwidth)) + '</xmax>\n')
#                 xml_file.write('            <ymax>' + str(
#                     int(((float(oneline[2])) * Pheight + 1) + (float(oneline[4])) * 0.5 * Pheight)) + '</ymax>\n')
#                 xml_file.write('        </bndbox>\n')
#                 xml_file.write('    </object>\n')
#                 xml_file.close()
#                 pre_img_name = img_name  # 将其设为"老"图
#             else:  # 不是新图而是"老图"
#                 # 7.同一张图片，只需要追加写入object
#                 xml_file = open((xml_path + img_name + '.xml'), 'a')
#                 xml_file.write('    <object>\n')
#                 xml_file.write('<name>' + dict[oneline[0]] + '</name>\n')
#                 '''  按需添加这里和上面
#                 xml_file.write('        <pose>Unspecified</pose>\n')
#                 xml_file.write('        <truncated>0</truncated>\n')
#                 xml_file.write('        <difficult>0</difficult>\n')
#                 '''
#                 xml_file.write('        <bndbox>\n')
#                 xml_file.write('            <xmin>' + str(
#                     int(((float(oneline[1])) * Pwidth + 1) - (float(oneline[3])) * 0.5 * Pwidth)) + '</xmin>\n')
#                 xml_file.write('            <ymin>' + str(
#                     int(((float(oneline[2])) * Pheight + 1) - (float(oneline[4])) * 0.5 * Pheight)) + '</ymin>\n')
#                 xml_file.write('            <xmax>' + str(
#                     int(((float(oneline[1])) * Pwidth + 1) + (float(oneline[3])) * 0.5 * Pwidth)) + '</xmax>\n')
#                 xml_file.write('            <ymax>' + str(
#                     int(((float(oneline[2])) * Pheight + 1) + (float(oneline[4])) * 0.5 * Pheight)) + '</ymax>\n')
#                 xml_file.write('        </bndbox>\n')
#                 xml_file.write('    </object>\n')
#                 xml_file.close()
#
#         # 8.读完txt文件最后写入</annotation>
#         xml_file1 = open((xml_path + pre_img_name + '.xml'), 'a')
#         xml_file1.write('</annotation>')
#         xml_file1.close()
#     print("Done !")
#
#
# # 修改成自己的文件夹 注意文件夹最后要加上/
# txt_to_xml("D:\\temp\\labels\\",
#            "D:\\temp\\images\\",
#            "D:\\temp\\xmls\\")
#
import cv2
import os

xml_head = '''<annotation>
    <folder>VOC2007</folder>
    <filename>{}</filename>
    <source>
        <database>The VOC2007 Database</database>
        <annotation>PASCAL VOC2007</annotation>
        <image>flickr</image>
    </source>
    <size>
        <width>{}</width>
        <height>{}</height>
        <depth>{}</depth>
    </size>
    <segmented>0</segmented>
    '''
xml_obj = '''
    <object>        
        <name>{}</name>
        <pose>Rear</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{}</xmin>
            <ymin>{}</ymin>
            <xmax>{}</xmax>
            <ymax>{}</ymax>
        </bndbox>
    </object>
    '''
xml_end = '''
</annotation>'''

# 需要修改为你自己数据集的分类
labels = ["red", "yellow","green","redleft","redright","greenleft","greenright","redforward",
            "greenforward","yellowleft","yellowright","yellowforward","redturn","greenturn","yellowturn","off"]  # label for datasets
num_32=num_64=num_96=0
cnt = 0
# txt_to_xml("D:\\temp\\labels\\",
#            "D:\\temp\\images\\",
#            "D:\\temp\\xmls\\")
txt_path = os.path.join('D:\\temp\\labels\\')  # yolo存放txt的文件目录
image_path = os.path.join('D:\\temp\\images\\')  # 存放图片的文件目录
path = os.path.join('D:\\temp\\xmls\\')  # 存放生成xml的文件目录

for (root, dirname, files) in os.walk(image_path):  # 遍历图片文件夹
    for ft in files:
        # print(ft)
        ftxt = ft.replace('jpg', 'txt')  # ft是图片名字+扩展名，将jpg和txt替换
        fxml = ft.replace('jpg', 'xml')
        xml_path = path + fxml
        obj = ''

        img = cv2.imread(root + ft)
        img_h, img_w = img.shape[0], img.shape[1]
        head = xml_head.format(str(fxml), str(img_w), str(img_h), 3)

        with open(txt_path + ftxt, 'r') as f:  # 读取对应txt文件内容
            for line in f.readlines():
                yolo_datas = line.strip().split(' ')
                label = int(float(yolo_datas[0].strip()))
                center_x = round(float(str(yolo_datas[1]).strip()) * img_w)
                center_y = round(float(str(yolo_datas[2]).strip()) * img_h)
                bbox_width = round(float(str(yolo_datas[3]).strip()) * img_w)
                bbox_height = round(float(str(yolo_datas[4]).strip()) * img_h)
                # if bbox_height>100 or bbox_width>100:
                #     print(bbox_width)
                # print(bbox_height)
                bbox=bbox_width*bbox_height
                if bbox<= 1024:
                    num_32+=1
                elif bbox<=4096:
                    num_64+=1
                else:
                    num_96+=1



                xmin = str(int(center_x - bbox_width / 2))
                ymin = str(int(center_y - bbox_height / 2))
                xmax = str(int(center_x + bbox_width / 2))
                ymax = str(int(center_y + bbox_height / 2))
                # print(int(center_x + bbox_width / 2)-int(center_x - bbox_width / 2))
                # print(int(center_y + bbox_height / 2)-int(center_y - bbox_height / 2))
                obj += xml_obj.format(labels[label], xmin, ymin, xmax, ymax)
        with open(xml_path, 'w') as f_xml:
            f_xml.write(head + obj + xml_end)
        cnt += 1
print(num_32)
print(num_64)
print(num_96)
