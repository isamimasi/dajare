# janomeをつかって形態素解析を行い、名詞と動詞を抜きだします。
#
#
#
#
#
from janome.tokenizer import Tokenizer
def janome(word):
    list=[]
    t = Tokenizer()
    for token in t.tokenize(word):
        if token.part_of_speech[0]=="名" or token.part_of_speech[0]=="動":
            #hiragana=jaconv.kata2hira(token.reading)
            dictionary={"voc":token.surface,"pronouce":token.reading,"wordCount":len(token.reading)}
            list.append(dictionary)
    return list