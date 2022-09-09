import ScentenceScore as scoring
from PDF_reader import *
import os
import pandas as pd
import numpy as np
import warnings


def getcompanies(path):
    Companies = []
    compname = []
    compname = os.listdir(path)
    for c in compname:
        Companies.append(path+'//' + c)
    return [Companies, compname]


def getyear(companies):
    Year = []
    for home, dirs, files in os.walk(companies):
        Year.append(home)
    del Year[0]

    return Year


def getreports(Company):
    Reports = []
    for home, dirs, files in os.walk(Company):
        for filename in files:
            Reports.append(os.path.join(home, filename))
    return Reports


if __name__ == '__main__':
    # warnings.filterwarnings("ignore")
    df00 = pd.read_excel(r'C:\Users\Eleven最沉着\Desktop\venv\指标关键词v1.xls')
    # print(index)
    # df00 = pd.DataFrame()
    # df00.insert(0, column='大项', value=index['大项'].values)
    # df00.insert(1, column='中项', value=index['中项'].values)
    # df00.insert(2, column='指标', value=index['指标'].values)
    # df00.insert(3, column='数据类型', value=index['数据类型'].values)
    # [SecondIndustry, SecondIndus] = getcompanies('C://Users//Eleven最沉着//Desktop//venv//化工')
    n=-1

    # for SecondInduss in SecondIndustry:
    # df01 = pd.DataFrame()
    n+=1
    [companies,compname]=getcompanies('C://Users//Eleven最沉着//Desktop//venv//各企业报表')

    j = -1
    #df01.insert(0, column='数据类型', value=index['数据类型'].values)
    keywords = df00['关键词'].values
    # keywords=keywords[np.isnan(keywords)]
    # print(keywords)

    for company in companies:
        zishu = []
        zishu2018 = []
        zishu2019 = []
        zishu2020 = []
        j = j + 1
        # print(j)
        t = 2018
        years = getyear(company)
        i = 4
        for year in years:
            # print(years)
            xinxi = []
            xinxi1=[]
            xinxi2=[]
            m=-1

            reports=getreports(year)
            for pdf_path in reports:
                m+=1
                pdf_path = pdf_path.replace('\\', '//')
                print(pdf_path)
                try:
                    paragraph = pdf_reader(pdf_path)
                    scoreTextObj = scoring.scoreText()

                    for keyword in keywords:
                        c = ''
                        matchedSentences = scoreTextObj.sentenceMatch(keyword, paragraph)
                        for text in matchedSentences:
                            a = text + ' '
                            c = c + a
                        if m==0:
                            xinxi1.append(c)
                        else:
                            xinxi2.append(c)
                    # print(xinxi1)
                    # print(xinxi2)
                except:
                    print(pdf_path + '打不开')

            if xinxi1 and xinxi2:
                for s in range(len(xinxi1)):
                    xinxi.append(xinxi1[s]+' '+xinxi2[s])
                    if t == 2018:
                        zishu2018.append(len(xinxi1[s])+len(xinxi2[s]))
                    elif t == 2019:
                        zishu2019.append(len(xinxi1[s])+len(xinxi2[s]))
                    elif t == 2020:
                        zishu2020.append(len(xinxi1[s])+len(xinxi2[s]))
            elif xinxi1==[]and xinxi2!=[]:
                for s in range(len(xinxi2)):
                    xinxi.append(xinxi2[s])
                    if t == 2018:
                        zishu2018.append(len(xinxi2[s]))
                    elif t == 2019:
                        zishu2019.append(len(xinxi2[s]))
                    elif t == 2020:
                        zishu2020.append(len(xinxi2[s]))
            elif xinxi2==[]and xinxi1!=[]:
                for s in range(len(xinxi1)):
                    xinxi.append(xinxi1[s])
                    if t == 2018:
                        zishu2018.append(len(xinxi1[s]))
                    elif t == 2019:
                        zishu2019.append(len(xinxi1[s]))
                    elif t == 2020:
                        zishu2020.append(len(xinxi1[s]))
            elif xinxi1==[]and xinxi2==[]:
                for a in range(len(keywords)):
                    xinxi.append(' ')
                    if t == 2018:
                        zishu2018.append(100)
                    elif t == 2019:
                        zishu2019.append(100)
                    elif t == 2020:
                        zishu2020.append(100)

            b = compname[j] + str(t)
            # print(xinxi)
            df00.insert(i, column=b, value=xinxi)
            t += 1
            i+=1
            print(b + '输出成功')
        d = compname[j] + '年均得分'
        for s in range(len(zishu2018)):
            zishu.append((zishu2018[s] + zishu2019[s] + zishu2020[s]) / 3)
        df00.insert(i, column=d, value=zishu)
        i += 1
    # df00.to_csv('excel_output_v3.csv', sheet_name=SecondIndus[n],na_rep=' ', encoding='gbk')
    g='文字指标结果_消费品（日用品）.csv'
    # with pd.ExcelWriter('excel_output_v3.xls') as writer:
    # print(df01)
    # df02= pd.concat([df00, df01], axis=1)
    # print(df02)
    # df02=df02.iloc[:,0:8]
    # df01.drop(df01.index, inplace=True)
    df00.to_csv(g,na_rep=' ', encoding='gbk',errors='ignore')