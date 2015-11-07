#!/usr/bin/env python3
# -*- coding: GBK -*-
"""
File: Translation_utility.py
Author: Zeyue Liang
Date: November 5, 2015
Email: zeyue.liang@outlook.com
Github: https://github.com/zeyue
Description:

"""


from easygui import *
import sys
import os
import codecs
import xlwt


reload(sys)
sys.setdefaultencoding('utf-8')

msgbox(u"Hi 超哥, 战斗吧！爆发吧小宇宙！")
# output_dir = r'../output/'

while 1:
    
	
    key_word_pairs = []
	
	#读取文件
    msg = u"选择一个你要翻译的文件："
    title = u"打开"
    full_file_path = fileopenbox(msg, title)
    # suffix = os.path.splitext(full_file_path)[1][1:]
    # while suffix != "properties":
        # msg = u"不正确的文件类型！是否重新选择？"
        # title = u"警告"
        # if ccbox(msg, title):
            # msg = u"选择一个你要翻译的文件："
            # title = u"打开要翻译的文件"
            # full_file_path = fileopenbox(msg, title)
            # suffix = os.path.splitext(full_file_path)[1][1:]
        # else:
            # sys.exit(0)

	#获得输出目录
    msg = u"选择文件输出的目录："
    title = u"输出目录"
    output_dir = diropenbox(msg, title)
	
	#文件位置
    translation_file_path = output_dir + "/" + os.path.splitext(os.path.basename(full_file_path))[0] + '/' + os.path.basename(full_file_path)
    record_file_path = output_dir + "/" + os.path.splitext(os.path.basename(full_file_path))[0] + '/' + 'translation_records.xls'

    #判断目录是否存在
    subdir = output_dir + "/" + os.path.splitext(os.path.basename(full_file_path))[0]

    while os.path.exists(subdir):
        msg = u"文件夹已存在！请选择其他文件夹！"
        title = u"警告！"
        if ccbox(msg, title):
            msg = u"选择文件输出的目录："
            title = u"输出目录"
            output_dir = diropenbox(msg, title)
        else:
            sys.exit(0)

    #新建目录
    os.mkdir(subdir)

    #新建翻译后的properties文件
    f1 = codecs.open(translation_file_path, 'w', 'utf-8')
    f1.close()
    
    #新建记录表格
    record_book = xlwt.Workbook(encoding='utf-8')
    booksheet = record_book.add_sheet('sheet1', cell_overwrite_ok=True)
    booksheet.write(0,0,u'Key')
    booksheet.write(0,1,u'Word')
    booksheet.write(0,2,u'翻译')
    booksheet.write(0,3,u'Unicode')
    record_book.save(record_file_path)

    msg = u"输入想要开始工作的行数"
    title = u"行数选择"
    start_index = integerbox(msg, title, '', 1, 10000)

	#分割键值
    end_index = 0
    with open(full_file_path, "r") as lines:
        for line in lines:
            # line = line.strip()
            # if line.strip():
            end_index += 1
            key_word_pairs += [line]
				
    for index in range(start_index - 1, end_index):
        if key_word_pairs[index] == "\n":
            f1 = codecs.open(translation_file_path, 'a', 'utf-8')
            f1.write("\n")
            f1.close() 

        elif key_word_pairs[index][0] == "#":
            f1 = codecs.open(translation_file_path, 'a', 'utf-8')
            f1.write(key_word_pairs[index])
            f1.close()

        else:
            splitPair = key_word_pairs[index].split("=")
            key = splitPair[0]
            if len(splitPair) > 2:
                word = '='.join(splitPair[1:])
            else:
                word = splitPair[1]
            msg = u"第" + str(index + 1) + u"个" + u" / 共" + str(len(key_word_pairs)) + u"个: " + "\n" \
                        + u"Key: " + key + "\n" \
                        + u"Word(请翻译): " + word
            translation = enterbox(msg, u"输入翻译（没有输入视为忽略）")
            
		    #判断是否有值输入，以及是否按了取消
            if translation is '':
                unicode_str = word
            elif translation is None:
                break
            else:
                unicode_str = str(repr(translation))[2:-1] + "\n"
                pass
            
            #打印翻译结果
            one_line1 = key + " = " + unicode_str
            f1 = codecs.open(translation_file_path, 'a', 'utf-8')
            f1.write(one_line1)
            f1.close()
		    
            #打印翻译记录
            row = booksheet.row(index + 1)
            row.write(0, key)
            row.write(1, word)
            row.write(2, translation)
            row.write(3, unicode_str)
            record_book.save(record_file_path)


	#询问是否继续工作
    msg = u"是否继续工作？喝杯咖啡吗？"
    title = u"接下来做什么？"
    if ccbox(msg, title):
        pass
    else:
        sys.exit(0)
