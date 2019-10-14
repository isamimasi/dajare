"""
辞書を読む


"""

import pandas as pd
import pickle
import os
def readDict():
    #日本語辞書（"./dictionary/nihongolist.xlsx"）の読み込み
    #読み込んだあと、"dictionary"内にnihongolist.binaryfileでpickle保存する。
    #２回目以降はnihongolist.binaryfileを読み込む。
    #辞書を更新したあとは、nihongolist.binaryfileを削除してください。
    if os.path.isfile('./dictionary/nihongolist.binaryfile'):
        with open('./dictionary/nihongolist.binaryfile', 'rb') as web:
            df = pickle.load(web)
    else:
        df=pd.read_excel("./dictionary/nihongolist.xlsx")
        df["romaji"]="_"
        df["score"]=0.000
        from pykakasi import kakasi
        kakasi = kakasi()
        kakasi.setMode('H', 'a')
        conv = kakasi.getConverter()
        for n in range (len(df)):
            #print(df.iat[n,1])
            romaji=conv.do(df.iat[n,1])
            romaji=romaji.replace("a","aaa").replace("i","iii").replace("u","uuu").replace("e","eee").replace("o","ooo")
            df.iat[n,5]=romaji
            #print(df.iat[n,5])
        with open('./dictionary/nihongolist.binaryfile', 'wb') as web:
            pickle.dump(df , web)
    return df
#readDict()