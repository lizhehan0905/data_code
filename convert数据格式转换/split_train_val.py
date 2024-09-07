# from sklearn.model_selection import train_test_split
# from PIL import Image
# import os
#
# path = "D:/毕业资料/数据集/我的数据集/S2TLD/temp/images"  # 你要划分的数据集
#
# dat = os.listdir(path)
#
# train, test = train_test_split(dat, test_size=0.2)  # 0.2表示需要划分的测试集比例
#
# for file in train:
#     im2 = Image.open("D:/毕业资料/数据集/我的数据集/S2TLD/temp/images/" + file)
#     im2.save("D:/毕业资料/数据集/我的数据集/S2TLD/temp/train/" + file)  # 划分后的训练集存放位置
#     txtfile = file.replace("jpg", "txt")
#
# for file in test:
#     im2 = Image.open("D:/毕业资料/数据集/我的数据集/S2TLD/temp/images/" + file)
#     im2.save("D:/毕业资料/数据集/我的数据集/S2TLD/temp/val/" + file)  # 划分后的训练集存放位置


import os
import random
import shutil

def get_imlist(path):
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]

def getData(src_path):

    dest_dir = src_path+'val' #划分出来的验证集
    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    img_list = get_imlist(src_path)
    random.shuffle(img_list)
    le = int(len(img_list) * 0.91)  # 这个可以修改划分比例
    for f in img_list[le:]:
        shutil.move(f, dest_dir)


'''
函数功能：
划分数据集
'''
def SplitImg(filePath):
    getData(filePath)

'''
函数功能：
根据划分的数据集进行移动标注文件
'''
def MoveAn(filePathAn,filePathImg):
    Imgs=os.listdir(filePathImg)
    if not os.path.isdir(filePathAn+'val'):
        os.mkdir(filePathAn+'val')

    for file in os.listdir(filePathAn):
        #print(filePathAn,filePathImg)
        #print(os.path.join(filePathAn,file),os.path.join(filePathAn+'val',file))
        if file[:-4]+'.jpg' in Imgs:

            shutil.move(os.path.join(filePathAn,file),os.path.join(filePathAn+'val',file))

if __name__=='__main__':
    filePath='D:/毕业资料/数据集/我的数据集/融合数据集/datasets/test2/images'# 换成你的数据集

    #拆分的数据集
    SplitImg(filePath)
    filePathAn='D:/毕业资料/数据集/我的数据集/融合数据集/datasets/test2/labels'# 换成你的标注文件地址

    # 根据数据集进行移动标注文件
    MoveAn(filePathAn,filePath+'val')
