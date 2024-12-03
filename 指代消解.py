import re
from stanfordcorenlp import StanfordCoreNLP
# 启动命令java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
def replace_pronouns_with_nouns(text):
    nlp = StanfordCoreNLP('http://localhost', port=9000)
    coref_result = nlp.coref(text)

    # 对于每个指代链，找到代表性提及并准备替换其他提及
    for cluster in coref_result:
        representative_mention = cluster[0][3]  # 代表性提及的文本

        for mention in cluster[1:]:  # 跳过第一个提及，因为它是代表性的
            mention_text = mention[3]  # 提及的文本

            # 使用正则表达式确保只替换作为独立单词出现的代词
            # \b是单词边界的元字符，确保匹配整个单词
            pattern = r'\b' + re.escape(mention_text) + r'\b'
            text = re.sub(pattern, representative_mention, text)

    nlp.close()  # 关闭NLP客户端
    return text

# 示例文本
sentence = '"On a sunny morning, little Jack and his father went fishing by the lake. They sat in a boat, and Dad taught Jack how to cast the line. Soon, Jack felt a heavy tug and shouted with excitement. He pulled with all his might and finally hauled a big, shimmering fish onto the boat. "Well done!" cheered Dad. They released the fish back into the lake, hoping it would swim happily ever after.".'
sentence2 = '"Lili and tom are playing in the garden. There is beautiful and they are happy.".'
# 执行替换
replaced_text = replace_pronouns_with_nouns(sentence)
print("Original text:", sentence)
print("Replaced text:", replaced_text)
print()
replaced_text = replace_pronouns_with_nouns(sentence2)
print("Original text:", sentence2)
print("Replaced text:", replaced_text)
