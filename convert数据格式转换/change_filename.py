# import os  
# import shutil  
  
# def replace_filename_chars_and_rename(folder_path):  
#     # 遍历指定文件夹下的所有jpg文件  
#     for filename in os.listdir(folder_path):  
#         if filename.endswith('.jpg'):  
#             # 构建原文件的完整路径  
#             print("find jpg")  
#             old_file_path = os.path.join(folder_path, filename)  
              
#             # 替换文件名中的空格、左括号和右括号为下划线  
#             new_filename = filename.replace(' ', '_').replace('(', '_').replace(')', '_')  
              
#             # 构建新文件的完整路径  
#             new_file_path = os.path.join(folder_path, new_filename)  
              
#             # 如果新文件名和原文件名不同，并且新文件不存在，则进行重命名  
#             if new_filename != filename and not os.path.exists(new_file_path):  
#                 try:  
#                     # 删除原文件  
#                     os.remove(old_file_path)  
                      
#                     # 如果原文件是一个文件而不是文件夹，则重命名（但这里我们实际上是通过复制和删除来模拟的）  
#                     shutil.copy2(old_file_path, new_file_path)  # 注意：这里我们假设原文件已经被删除了，所以实际上这行代码不会执行  
                      
#                     # 再次删除原文件（因为我们假设它已经被删除了）  
#                     # os.remove(old_file_path)  # 这行代码是多余的，因为我们已经假设删除了原文件  
                      
#                     print(f"Renamed '{filename}' to '{new_filename}'")  
#                 except Exception as e:  
#                     print(f"Error renaming '{filename}': {e}")  
#             else:  
#                 print(f"No changes needed for '{filename}'")  
  
# # 使用示例  
# folder_to_process = '/data/datasets/new_dataset/rename/iamges/test'  # 替换为你的文件夹路径  
# replace_filename_chars_and_rename(folder_to_process)




# """
# txt改名
# """
# import os
# from PIL import Image
# import glob


# png_dir = '/data/datasets/new_dataset/rename/test'

# # 修改为你想要存储jpg图片的路径
# jpg_dir = '/data/datasets/new_dataset/rename/temp'

# # 保证目标文件夹存在
# if not os.path.exists(jpg_dir):
#     os.makedirs(jpg_dir)

# # 获取png文件列表
# png_files = [f for f in os.listdir(png_dir) if f.endswith('.jpg')]

# # 按照文件名排序
# # sorted_png_files = sorted(png_files)

# # 批量转换并重命名
# for i, png_file in enumerate(png_files):
#     img = Image.open(os.path.join(png_dir, png_file))
#     rgb_img = img.convert('RGB')
#     jpg_file = os.path.join(jpg_dir, f'{i+0}.jpg')
#     rgb_img.save(jpg_file, 'JPEG')
#     # with open(os.path.join(png_dir, png_file), "r") as f_in:
#     #     lines = f_in.readlines()
#     # txt_file = os.path.join(jpg_dir, f'{i+10304}.txt')
#     # with open(txt_file, "w") as f_out:
#     #     f_out.writelines(lines)

import os  
from pathlib import Path  
  
def rename_and_replace_jpg_files(image_path, label_path, start_number):  
    # 确保提供的文件夹路径是存在的  
    if not os.path.isdir(image_path):  
        print(f"Error: The directory {image_path} does not exist.")  
        return 
    if not os.path.isdir(label_path):  
        print(f"Error: The directory {label_path} does not exist.")  
        return  
  
    # 遍历文件夹下的所有文件  
    for filename in os.listdir(image_path):  
        # 检查文件是否是jpg文件  
        if filename.lower().endswith('.jpg'):  
            # 构建文件完整路径  
            old_file_path = os.path.join(image_path, filename)
            # 生成新文件名  
            new_filename = f"{start_number:06d}.jpg"  # 假设我们想要至少4位数的文件名，不足部分用0填充  
            new_file_path = os.path.join(image_path, new_filename)  
            # 增加数字以确保文件名唯一  
            while os.path.exists(new_file_path):  
                start_number += 1  
                new_filename = f"{start_number:06d}.jpg"  
                new_file_path = os.path.join(image_path, new_filename)  
  
            # 重命名文件（实际上是复制并删除原文件）  
            try:  
                Path(old_file_path).rename(new_file_path)  
                print(f"Renamed '{filename}' to '{new_filename}'")  
            except OSError as e:  
                print(f"Error: {e.strerror} when renaming {old_file_path} to {new_file_path}")  
        
        txt_name = filename.replace('.jpg','.txt') 
        if txt_name.lower().endswith('.txt'):  
            # 构建文件完整路径  
            old_file_path = os.path.join(label_path, txt_name)
            # 生成新文件名  
            new_filename = f"{start_number:06d}.txt"  # 假设我们想要至少4位数的文件名，不足部分用0填充  
            new_file_path = os.path.join(label_path, new_filename)  
            # 增加数字以确保文件名唯一  
            while os.path.exists(new_file_path):  
                start_number += 1  
                new_filename = f"{start_number:06d}.txt"  
                new_file_path = os.path.join(label_path, new_filename)  
  
            # 重命名文件（实际上是复制并删除原文件）  
            try:  
                Path(old_file_path).rename(new_file_path)  
                print(f"Renamed '{txt_name}' to '{new_filename}'")  
            except OSError as e:  
                print(f"Error: {e.strerror} when renaming {old_file_path} to {new_file_path}") 
  
# 使用示例  
image_path = "/data/datasets/new_dataset/rename/images/test_origin"  # 替换为你的文件夹路径  
label_path = "/data/datasets/new_dataset/rename/labels/test_origin"  # 替换为你的文件夹路径  
start_number_to_use = 0  # 从哪个数字开始编排文件名  
rename_and_replace_jpg_files(image_path, label_path,start_number_to_use)
