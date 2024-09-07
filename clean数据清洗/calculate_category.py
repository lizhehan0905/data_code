# # """
# # 删掉没有标签的、只有红绿黄无标签的标注文件
# # "Red, Yellow, Green, off, RedLeft, RedRight, GreenLeft, GreenRight,RedStraight,GreenStraight"
# # 874, 67,1838,119,1092,5,178,13,9,20
# # """
# # import xml.etree.ElementTree as ET
# # import pickle
# # import os
# # from os import listdir, getcwd
# # from os.path import join
# # import glob
# # import os
# # for i in range(20):
# #     globals()["num"+str(i)]=0


# # for txt in glob.glob("*.txt"):
# #     with open(txt, 'r') as file:
# #         lines = file.readlines()
# #     new_lines = []
# #     for line in lines:
# #         # if line[0]==str(9):
# #         # print(line[0])
# #         for i in range(20):
# #             if line[0] == str(i) or line[0:2] == str(i):
# #                 globals()["num"+str(i)]+=1



# # # sum=0
# # # for i in range(20):
# # #     sum+=eval("num" + str(i))
# # #     print("num_" + str(i) + ":", eval("num" + str(i)))
# # # print(f"sum:{sum}")


# import os  
# # for i in range(20):
# #     globals()["num"+str(i)]=0

# def modify_files_in_directory(directory):  
#     # 遍历指定目录下的所有文件  
#     for filename in os.listdir(directory):  
#         if filename.endswith(".txt"):  # 确保只处理txt文件  
#             file_path = os.path.join(directory, filename)  
              
#             # 读取文件内容  
#             with open(file_path, 'r', encoding='utf-8') as file:  
#                 lines = file.readlines()  
              
#             # 修改内容  
#             modified_lines = []  
#             for line in lines:  
#                 # 去除行首的空白字符，然后检查第一个字符是否为数字且不是0  
#                 stripped_line = line.lstrip()  
#                 # print(stripped_line[0])
#                 # if stripped_line and stripped_line[0].isdigit():
#                 #     globals()["num"+str(stripped_line[0])]+=1
#                 if stripped_line and stripped_line[0].isdigit() and stripped_line[0] != '0':  
#                     # 如果第一个数字不是0，则替换为0，并保留原行的其余部分  
#                     # 注意：这里假设数字与后续内容之间可能有空白字符  
#                     modified_line = '0' + stripped_line[1:]  
#                     # 如果原行首有空格或制表符等，需要将其加回到替换后的行首  
#                     leading_whitespace = line[:len(line) - len(stripped_line)]  
#                     modified_lines.append(leading_whitespace + modified_line)  
#                 else:  
#                     # 如果第一个字符不是数字或已经是0，则直接保留原行  
#                     modified_lines.append(line)  
              
#             # 将修改后的内容写回文件  
#             with open(file_path, 'w', encoding='utf-8') as file:  
#                 file.writelines(modified_lines)  
#     # for i in range(20):
#     #     print(globals()["num"+str(i)])
  
# # 指定目录路径  
# directory_path = 'D:\\datasets\\homemade3\\labels'  
# modify_files_in_directory(directory_path)



import os  
import re  
  
def modify_files_in_directory(directory):  
    # 遍历指定目录下的所有文件  
    for filename in os.listdir(directory):  
        if filename.endswith(".txt"):  # 确保只处理txt文件  
            file_path = os.path.join(directory, filename)  
              
            # 读取文件内容  
            with open(file_path, 'r', encoding='utf-8') as file:  
                lines = file.readlines()  
              
            # 过滤并修改内容  
            modified_lines = []  
            for line in lines:  
                # 去除行首和行尾的空白字符  
                stripped_line = line.strip()  
                  
                # 检查第一个字符（在去除行首空白字符后）是否为0开头的数字  
                if stripped_line and stripped_line[0] == '0' and stripped_line[1:].isdigit():  
                    # 检查整行是否恰好为5个数字（在去除所有非数字字符后）  
                    if len(re.sub(r'\D', '', stripped_line)) == 5:  
                        modified_lines.append(line)  # 符合条件，保留原行  
                  
            # 将修改后的内容写回文件  
            with open(file_path, 'w', encoding='utf-8') as file:  
                file.writelines(modified_lines)  
  
# 指定目录路径  
directory_path = 'D:\\datasets\\homemade3\\labels'  
modify_files_in_directory(directory_path)