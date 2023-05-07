import pandas as pd
import re
import csv
import jieba  
import jieba.posseg
import jieba.analyse
import zhconv
import jieba.posseg as pseg
import operator

path = '2020-11.csv'

# 使用pandas读入
data = pd.read_csv(path, on_bad_lines='skip',encoding = "utf-8",quoting=csv.QUOTE_NONE) #读取文件中所有数据
x = data[['content']]#读取某一列

x.head(10)
print("----------------finish reading the csv document------------------")

def del_nonChinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    result = pattern.findall(text)
    return " ".join(result)


# 读取实体名词文件
with open("entity.txt", "r", encoding="utf-8") as f:
    entities = [line.strip() for line in f]
print(entities)

with open("stop.txt", "r", encoding="utf-8") as f:
    stop_words = [line.strip() for line in f]
#print(stop_words)

print("------------------finish reading entities and stop words----------------")


text_list = []

for index, row in data.iterrows():
    #print(row['content']) 
    x = re.sub(r'#.*?#', '', row['content']) #删去超话内容，防止干扰提取情感词
    result = del_nonChinese(x) #删去非中文内容
    text = zhconv.convert(result, 'zh-cn')  #将繁体中文变为简体中文
    #words = [word for word in jieba.cut(text) if word not in stop_words]  #删除停用词
    text_list.append(text)

print("------------------finish processing the texts----------------")

'''
text_without_stopwords = []
text_nos = []

for text in text_list:
    words = [word for word in jieba.cut(text) if word not in stop_words]  #删除停用词
    text_without_stopwords.append(words)
    for text in text_without_stopwords:
        if text != ' ':
            text_s = " ".join(text)
            text_nos.append(text_s)
set_ntext = set(text_nos)
print("------------------finish removing stop words----------------------------")

'''

sentiment_dic = {}
s_text = []


for text in text_list:
    #print(text)
    # 对文本进行分词和词性标注
    words = pseg.cut(text)
    words_with_pos = [(word, flag) for word, flag in words]

    has_entity = False
    new_text_list = []
    new_text_string = ''
    #for text in test_list:
    for i in range(len(words_with_pos)):
        if words_with_pos[i][0] in entities:
            has_entity = True

    # 根据形容词和副词提取情感词
    emotions = []
    for i in range(len(words_with_pos)):
        word, pos = words_with_pos[i]
        if word in stop_words:
            continue
        else:
            if pos.startswith('a') == False and pos.startswith('d') == False:
                word = word + ' '
                new_text_list.append(word)
            if pos.startswith('a'):
                # 如果当前词是形容词
                if i == 0 or not words_with_pos[i-1][1].startswith('d'):
                    # 如果当前词是第一个词或前面没有副词，则将当前词加入情感词
                    emotion = '#' + word + '# '
                    emotions.append(emotion)
                    new_text_list.append(emotion)
                else:
                    # 否则，将副词和形容词组合成情感词
                    emotion = str('#' + words_with_pos[i-1][0] + '_' + word + '# ')
                    emotions.append(emotion)
                    new_text_list.append(emotion)
                    #print(type(word))
                    
            elif pos.startswith('d'):
                # 如果当前词是副词，不处理
                continue

    new_text_string = ''.join(new_text_list)
    s_text.append(new_text_string)
            
        

    # 找到出现最频繁的情感词
    if has_entity:
        for emotion in emotions:
            if emotion not in sentiment_dic.keys():
                sentiment_dic[emotion] = 1
            else:
                sentiment_dic[emotion] = sentiment_dic[emotion] + 1

set_stext = set(s_text)
print("----------------------finish getting sentiment words in the document--------------------")

                


sentiment_words = []

sorted_sentiment_dic = dict(sorted(sentiment_dic.items(),key = operator.itemgetter(1), reverse=True))
count = 0  # 记录已经遍历了多少个key值
for key in sorted_sentiment_dic:
    if count >= 1000:  # 如果已经遍历了500个key值，则退出循环
        break
    if key not in sentiment_words:
        sentiment_words.append(key)  # 打印当前key值
        count += 1  # 计数器加1

with open('sentiment11.txt','w') as f:
    for word in sentiment_words:
        f.write(word + "\n")


print("------------------finish writing sentiment words into sentiment_words.txt-----------------")

with open('new_corpus11.txt','w', encoding = 'utf-8') as f:
    for text in set_stext:
        for entity in entities:
            if entity in text:
                text = text.replace(entity, ' 2020-11 ')
        f.write(text + "\n")


