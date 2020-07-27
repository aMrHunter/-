
from collections import Counter
import math
import numpy as np
import tensorflow as tf




class Tokenizer:
    # 定义一个分词器

    def __init__(self, token_dict):
        self.token_dict = token_dict
        self.token_dict_rev = {value: key for key, value in self.token_dict.items()}
        self.vocabulary_size = len(self.token_dict)

    # 编号 到 字的映射
    def id_to_token(self, token_id):
        return self.token_dict_rev[token_id]

    # 字 到 编号的映射
    # 找不到对应字 就用[UNK] 代替
    def token_to_id(self, token):
        return self.token_dict.get(token, self.token_dict['[UNK]'])

    # 对古诗进行编码  即转换成相应的编号序列 并加上开始结束标志
    def encode(self, tokens):

        tokens_ids = [self.token_to_id('[CLS]'), ]
        for token in tokens:
            tokens_ids.append(self.token_to_id(token))
        tokens_ids.append(self.token_to_id('[SEP]'))
        return tokens_ids

    # 对古诗进行解码 即把编码序列转换成字序列 注意处理开始结束标志
    def decode(self, token_ids):

        sepc_tokens = {'[CLS]', '[SEP]'}
        tokens = []
        for token_id in token_ids:
            token = self.id_to_token(token_id)
            if token in sepc_tokens:
                continue
            tokens.append(token)

        return ''.join(tokens)


# 禁用词 一旦发现诗中有就丢弃
disallowed_words = ['（', '）', '(', ')', '__', '《', '》', '【', '】', '[', ']']

# 句子的最大长度 超出就丢弃
max_len = 64
# 最低词频 低于就丢弃
min_word_frequency = 8
# 一次的训练样本数 这里也就是一次8首古诗
batch_size = 8

with open('./poetry.txt', 'r', encoding='utf-8') as f:
    # 一次性读取整个文件的字符串列表
    lines = f.readlines()
    # 统一冒号格式
    lines = [line.replace('：', ':') for line in lines]

# 创建空的诗集列表
poetry = []
# 逐行处理数据
for line in lines:

    if line.count(':') != 1:
        continue
    # 把题目和诗句划分开
    __, last_part = line.split(':')
    flag = False
    for k in disallowed_words:
        if k in last_part:
            flag = True
            break
    if flag:
        continue
    if len(last_part) > max_len - 2:
        continue
    # 把符合条件的诗句加到诗集列表中
    poetry.append(last_part.replace('\n', ''))

counter = Counter()
# 统计词频 这里是每个字的频率
for line in poetry:
    counter.update(line)

# 去掉低频词
words = [(token, count) for token, count in counter.items() if count > min_word_frequency]

# 按照词频排序
words = sorted(words, key=lambda x: -x[1])
# 去掉词频列表 只留下词列表
words = [token for token, count in words]

# 把特殊符号加到字典中
words = ['[PAD]', '[UNK]', '[CLS]', '[SEP]'] + words

# 创建词典 token->id映射关系
token_id_dict = dict(zip(words, range(len(words))))

# 使用新词典重新建立分词器
tokenizer = Tokenizer(token_id_dict)
# 打乱列表诗句的顺序
np.random.shuffle(poetry)


# for i in range(10):
#     print(poetry[i])



class PDGenerator:
    # 数据生成器


    def __init__(self, data, random=False):
        self.data = data

        self.batch_size = batch_size
        # 每个epoch迭代的步数
        self.steps = int(math.floor(len(self.data) / self.batch_size))
        # 每个epoch开始时是否随机混洗
        self.random = random

    def sequence_padding(self, data, length=None, padding=None):
        # 因为一个字符对应生成一个字符 需要对训练集进行切片操作 产生等长错位的x y 用于训练
        # 找出字数最多的一行古诗作为标准 不够就填充
        if length is None:
            length = max(map(len, data))
        # 使用专门的填充词填充 用对应的词典id填充
        if padding is None:
            padding = tokenizer.token_to_id('[PAD]')
        outputs = []
        # 依次对每行进行填充
        for line in data:
            padding_length = length - len(line)
            if padding_length > 0:
                # 不够长度就进行填充
                outputs.append(np.concatenate([line, [padding] * padding_length]))
            else:
                outputs.append(line[:length])
        # 返回二维数组
        return np.array(outputs)


    def __len__(self):
        return self.steps

    def __iter__(self):
        total = len(self.data)

        if self.random:
            np.random.shuffle(self.data)
        # 开始迭代 步长为 batch_size 步数也就是epoch上面已经求出 一次epoch 一次yield一个baych_data
        for start in range(0, total, self.batch_size):
            # 如果最后一步没有超出total
            end = min(start + self.batch_size, total)
            # 每次重新建立
            batch_data = []
            # 依次对古诗进行编码 并将序列加到batch_data中
            for single_data in self.data[start:end]:
                batch_data.append(tokenizer.encode(single_data))

            # 每行古诗填充为相同的长度 返回后是二维数组
            batch_data = self.sequence_padding(batch_data)
            # 子生成器 yield x,y numpy的切片  逗号前对行操作 逗号后面对列操作
            # x为16首古诗的第一个字符到倒数第二个 y为16首古诗第二个到最后一个字符
            yield batch_data[:, :-1], tf.one_hot(batch_data[:, 1:], tokenizer.vocabulary_size)
            del batch_data


    def for_fit(self):
        """
        委托生成器

        """
        while True:
            yield from self.__iter__()




