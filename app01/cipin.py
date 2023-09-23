import jieba
#加载停用词表
def cipin_exec(txt):
    words  = jieba.lcut(txt)
    stopwords = [line.strip() for line in open("./cipin/CS.txt", encoding="utf-8").readlines()]

    counts = {}
    for word in words:
        #不在停用词表中
        if word not in stopwords:
            #不统计字数为一的词
            if len(word) == 1:
                continue
            else:
                counts[word] = counts.get(word,0) + 1
    items = list(counts.items())
    items.sort(key=lambda x:x[1], reverse=True)
    return_items = []
    for i in range(30):
        word, count = items[i]
        return_items.append({"name":word,"value":count})
    # print(return_items[:15])
    return return_items[:15]