
######################################
#
#  ダジャレメーカー
#
#　１　かなの辞書を読み込む
#　２　入力文字を分解し、平仮名にかえる
#　３　辞書の中から、音の似ているものをみつける
#　４　似ている音の単語を漢字、カナに変換し、文章を変換する
#　５　ダジャレが何個もできる
#　６　おもしろいものをえらぶ
#######################################
import sub01_dictionary
import sub02_breaksentence
import difflib
import pandas as pd
import random
def main(sentence):
    Table=[]
    #日本語辞書の読み込み
    jpnDict=sub01_dictionary.readDict()
    #sentenceを形態素解析をし、言葉を分解します
    #「世界の中心で愛を叫ぶ」では、「世界、中心、愛、叫ぶ」に分けられます。
    brokenSentence=sub02_breaksentence.janome(sentence)
    ###何個の単語を変えますか？
    #短い文章だと単語の１か所だけを変更します。
    #長い文章では変更する単語数を増やします。
    convertNumber =int(len(brokenSentence)/6+1)
    #単語の長さ順に並び変えている
    #形態素解析された単語は音の長い順に並びかえます
    #長い単語の部分をダジャレにした方が、おもしろいことが多いのです。
    TableOne=pd.DataFrame(brokenSentence)
    TableOne=TableOne.sort_values('wordCount', ascending=False)
    #後ほど単語をローマ字に変換します
    #そのための設定です↓
    from pykakasi import kakasi
    kakasi = kakasi()
    kakasi.setMode('K', 'a')
    conv = kakasi.getConverter()
    #設定終了↑
    #
    #あまりに単語数が多いと計算負荷がかかるので最高４単語にしています。
    #レター数が多い順に４単語を選びます。
    if len(brokenSentence)>4:
        sentenceNum=4
    else:
        sentenceNum=len(brokenSentence)
    #単語数が多いと変換する単語が増えます。sentenceNum回繰り返します。
    for num in range (sentenceNum):
        #ひらがなをローマ字に変えます。
        pronouce=TableOne.iat[num,0]
        romaji=conv.do(pronouce)
        #母音を強調するためにa,i,u,e,o をaaa,iii,uuu,eee,oooにします。
        #世界は「せかい」と変わり、「sekai」とかわり「seeekaaaiii」となります。
        #母音が似ている単語をダジャレにつかった方が理解しやすいのです
        romaji=romaji.replace("a","aaa").replace("i","iii").replace("u","uuu").replace("e","eee").replace("o","ooo")
        for k in range(len(jpnDict)):
            #辞書内のローマ字と今回の単語を比較します。
            score = difflib.SequenceMatcher(None, romaji,jpnDict.iat[k,5]).ratio()
            #あまりに似ている場合は、候補から落とします。
            if score>0.93:
                jpnDict.iat[k,6]=0.000
            else:
                if jpnDict.iat[k,3]>0:
                    #辞書の中に、ダジャレになると面白いだろうなぁという単語に数値を入れています。
                    #世界の中心で愛を叫ぶで「世界の中心で杏里を叫ぶ'」がでるのは、固有名詞のスコアが高いからです。
                    score=score+(jpnDict.iat[k,3]*.1)
                jpnDict.iat[k,6]=score
        #jpnDict_sのデータフレームの中に「score」があります。
        #このスコアは単語の響きがにており、かつ面白い単語であれば高くなります。
        jpnDict_s = jpnDict.sort_values('score', ascending=False)
        #Tableの中に「オリジナの単語」　「世界」とそれに似た単語リスト「正解、仙台、せっかち・・・」と似ている単語が入ります。
        Table.append([TableOne.iat[num,1],jpnDict_s])
    #####100個のダジャレをつくります。
    dajare100=[]
    for repeat in range (100):
        dajare=sentence
        for ii in range(convertNumber):
            ranTable = random.randint(1,len(Table)-1)
            #スコアが0.9を超える単語を使い（どれを選ぶかはランダム）ダジャレをつくります。
            df_new=Table[ranTable][1]
            over08=len(df_new[df_new["score"]>0.9])
            rannum = random.randint(1,over08+3)
            dajare=dajare.replace(Table[ranTable][0],df_new.iat[rannum,0])
        dajare100.append(dajare)
    #重複したダジャレを消します。
    dajareList=list(set(dajare100))
    print(dajareList)
    #とりあえず、ひとつ選びます。一番おもしろいかどうかわかりません。ランダムです。
    selecrandom=random.randint(1,len(dajareList)-1)
    dajareOne=dajareList[selecrandom]
    print (dajareOne)
    return dajareOne,dajareList
main("世界の中心で愛を叫ぶ")
main("名探偵コナン ゼロの執行人")
main("国境の長いトンネルを抜けると雪国であった。夜の底が白くなった。")