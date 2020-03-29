import os
import datetime
import re
import pandas as pd
import shutil


# 該当ファイルをregexで抽出
def dateDecide(fromPath): 
    """Decide date of data"""
    exdirs = os.listdir(fromPath)
    print(exdirs)
    print("日付を入力してください。(例 20201204)")
    dataDate0 = input()
    regex = dataDate0 +  r"_.+"
    regex2 = r".+_extract"
    pattern = re.compile(regex)
    pattern2 = re.compile(regex2)
    for exdir in exdirs:
        if pattern.match(exdir):
            if not(pattern2.match(exdir)):
                date_path = os.path.join(fromPath, exdir).replace("\\", "/")
            else:
                continue
        else:
            continue
#    dataDate0 = "190812_test"
    try:
        return date_path
    except UnboundLocalError:
        print("エラー　外部ストレージにデータが見つかりませんでした。")

def chooseFile(fromDir, rdataname):
    """Load csvFile"""
    dataFiles = os.listdir(fromDir)
    regex = ".+" + rdataname
    pattern = re.compile(regex)
    filelist = []
    for dataFile in dataFiles:
        if pattern.match(dataFile):
            data_path = os.path.join(fromDir, dataFile).replace("\\", "/")
            filelist.append(data_path)
        else:
            continue
    try:
        return filelist
    except UnboundLocalError:
        print("エラー　外部ストレージにデータが見つかりませんでした。")

def editCSV(datapath, dir_name):
    rawFile = open(datapath, "r")
    # temp file(for editing) = datapath_w
    file, ext = os.path.splitext(os.path.basename(datapath))
    datapath_w = os.path.join(dir_name, file+"_temp").replace("\\", "/")+ext
    print(datapath_w)
    #     datapath_w = "C:/Users/190214/Desktop/test.txt"
    outputFile = open(datapath_w, "w")
    string = rawFile.readline()
    while(string):
    #     print(string)
        regex_start = '[M_EBR Data]\n'
    #     pattern_start = re.compile(regex_start)
        if string == regex_start:
            regex_end = "[ADDC Result]\n"
            while(string!=regex_end):
                string = rawFile.readline()
                outputFile.write(string)
            break
        else:
            string = rawFile.readline()
    rawFile.close()
    outputFile.close()
    a = pd.read_csv(datapath_w, sep="\t", index_col=1,  header=0)
    #     a.head()
    EBR1Width_dfs = a[a["EBR1Width(um)"] >= 0]
    #     EBR1Width_dfs.head()

    EBR1Width_dfs.to_csv(datapath_w, sep="\t", index=False)
    editFile = open(datapath_w, "r")


    # finished file = output_w
    
    output_w = os.path.join(dir_name, file+"_extract").replace("\\", "/")+ext
    outputFile = open(output_w, "w")


    rawFile = open(datapath, "r")
    string = rawFile.readline()
    while(string):
        regex_start = '[M_EBR Data]\n'
        if string == regex_start:
            outputFile.write(string)
            # editFile insert
            string_edit = editFile.readline()
            while(string_edit):
                outputFile.write(string_edit)
                string_edit = editFile.readline()
            # string = m_ebr, editFile=360
            regex_end = "[ADDC Result]\n"
            while(string!=regex_end):
                string = rawFile.readline()
        else:
            outputFile.write(string)
            string = rawFile.readline()
    outputFile.close()
    editFile.close()
    os.remove(datapath_w)
    
    
if _name_ == "_main_":
    fromSubpath = "//tklgfile8/Process/01_共通/01_Open/PTEA/02 Evaluation DATA@2020"
    yourName = "K.Sakaguchi"
    dir_path0 = os.path.join(fromSubpath, yourName).replace("\\", "/")
    experiment_name = "WiseCAM Raw Data"
    dir_path1 = os.path.join(dir_path0, experiment_name).replace("\\", "/")
    
    dirname0 = dateDecide(dir_path1)
    print(dirname0)
    rdataname = "ImageAnalyzeResult.txt"
    
    fileList = chooseFile(dirname0, rdataname)
    print(fileList)
        
    dir_name = os.path.dirname(fileList[0])+"_extract" 
    if(os.path.isdir(dir_name) == False):
        os.mkdir(dir_name)
        print(dir_name)
    else:
        shutil.rmtree(dir_name)
        os.mkdir(dir_name)
        
    for file in fileList:
    editCSV(file, dir_name)
