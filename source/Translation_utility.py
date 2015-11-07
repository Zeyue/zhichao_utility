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

msgbox(u"Hi ����, ս���ɣ�������С���棡")
# output_dir = r'../output/'

while 1:
    
	
    key_word_pairs = []
	
	#��ȡ�ļ�
    msg = u"ѡ��һ����Ҫ������ļ���"
    title = u"��"
    full_file_path = fileopenbox(msg, title)
    # suffix = os.path.splitext(full_file_path)[1][1:]
    # while suffix != "properties":
        # msg = u"����ȷ���ļ����ͣ��Ƿ�����ѡ��"
        # title = u"����"
        # if ccbox(msg, title):
            # msg = u"ѡ��һ����Ҫ������ļ���"
            # title = u"��Ҫ������ļ�"
            # full_file_path = fileopenbox(msg, title)
            # suffix = os.path.splitext(full_file_path)[1][1:]
        # else:
            # sys.exit(0)

	#������Ŀ¼
    msg = u"ѡ���ļ������Ŀ¼��"
    title = u"���Ŀ¼"
    output_dir = diropenbox(msg, title)
	
	#�ļ�λ��
    translation_file_path = output_dir + "/" + os.path.splitext(os.path.basename(full_file_path))[0] + '/' + os.path.basename(full_file_path)
    record_file_path = output_dir + "/" + os.path.splitext(os.path.basename(full_file_path))[0] + '/' + 'translation_records.xls'

    #�ж�Ŀ¼�Ƿ����
    subdir = output_dir + "/" + os.path.splitext(os.path.basename(full_file_path))[0]

    while os.path.exists(subdir):
        msg = u"�ļ����Ѵ��ڣ���ѡ�������ļ��У�"
        title = u"���棡"
        if ccbox(msg, title):
            msg = u"ѡ���ļ������Ŀ¼��"
            title = u"���Ŀ¼"
            output_dir = diropenbox(msg, title)
        else:
            sys.exit(0)

    #�½�Ŀ¼
    os.mkdir(subdir)

    #�½�������properties�ļ�
    f1 = codecs.open(translation_file_path, 'w', 'utf-8')
    f1.close()
    
    #�½���¼���
    record_book = xlwt.Workbook(encoding='utf-8')
    booksheet = record_book.add_sheet('sheet1', cell_overwrite_ok=True)
    booksheet.write(0,0,u'Key')
    booksheet.write(0,1,u'Word')
    booksheet.write(0,2,u'����')
    booksheet.write(0,3,u'Unicode')
    record_book.save(record_file_path)

    msg = u"������Ҫ��ʼ����������"
    title = u"����ѡ��"
    start_index = integerbox(msg, title, '', 1, 10000)

	#�ָ��ֵ
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
            msg = u"��" + str(index + 1) + u"��" + u" / ��" + str(len(key_word_pairs)) + u"��: " + "\n" \
                        + u"Key: " + key + "\n" \
                        + u"Word(�뷭��): " + word
            translation = enterbox(msg, u"���뷭�루û��������Ϊ���ԣ�")
            
		    #�ж��Ƿ���ֵ���룬�Լ��Ƿ���ȡ��
            if translation is '':
                unicode_str = word
            elif translation is None:
                break
            else:
                unicode_str = str(repr(translation))[2:-1] + "\n"
                pass
            
            #��ӡ������
            one_line1 = key + " = " + unicode_str
            f1 = codecs.open(translation_file_path, 'a', 'utf-8')
            f1.write(one_line1)
            f1.close()
		    
            #��ӡ�����¼
            row = booksheet.row(index + 1)
            row.write(0, key)
            row.write(1, word)
            row.write(2, translation)
            row.write(3, unicode_str)
            record_book.save(record_file_path)


	#ѯ���Ƿ��������
    msg = u"�Ƿ�����������ȱ�������"
    title = u"��������ʲô��"
    if ccbox(msg, title):
        pass
    else:
        sys.exit(0)
