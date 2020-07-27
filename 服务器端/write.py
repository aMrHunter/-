
import numpy as np

max_len = 64


def generate_random(tokenizer, model, s=''):
    """
    随机生成一首诗
    """
    # 将开头词编码
    token_ids = tokenizer.encode(s)
    # 去掉结束字符串[SEP]
    token_ids = token_ids[:-1]
    # 每次预测一个字 把这个字加上后再作为输入 作为最后一个token进行预测下一个结果
    poetry = []
    label = ['，', '。']
    label_ids = {tokenizer.token_to_id(token) for token in label}
    n = 0
    poetry.append(s)
    while len(token_ids) < max_len:
        # 进行预测，只保留第一个样例（我们输入的样例数只有1）的、最后一个token的预测的、不包含[PAD][UNK][CLS]的概率分布
        prowords = model.predict([token_ids, ])[0, -1, 3:]

        # 根据得到的预测概率值进行逆序排序 并取得概率前100的结果的索引值（下标值）
        # argsort()得到的是下标 与实际的下标相差3 所以下面要加上3
        word_args = prowords.argsort()[::-1][:100]
        # 根据下标值取得真实的概率
        word_val = prowords[word_args]
        # 归一化
        p = word_val / sum(word_val)

        # 根据概率随机选取1个作为最终预测结果 选取概率不相同 以p中的概率为基准
        target_index = np.random.choice(len(word_val), p=p)
        #  把上步得到的概率值取下标加上3 得到实际的下标
        target = word_args[target_index] + 3
        token_ids.append(target)

        # 如果加上3后 == 3 说明是结束词 [SEP]的下标是0
        if target in label_ids:
            n = n + 1
        if n == 4:
            break
        if target == 3:
            break
        poetry.append(tokenizer.id_to_token(target))
    return ''.join(poetry)


def generator_head(tokenizer, model, head):
    """
    生成藏头诗
    :return:
    """
    # 使用空串初始化 目的是加上[CLS]开始标志 后面再对输入head每个字处理
    token_ids = tokenizer.encode('')
    # 这时候里面只有[CLS] [SEP] 需要去掉[SEP]
    token_ids = token_ids[:-1]
    # 藏头诗需要判断标点来结束本行
    label = ['，', '。']
    label_ids = {tokenizer.token_to_id(token) for token in label}
    poetry = []
    # 分别对head中的每一个字进行处理 各自生成一行
    for ch in head:
        # 先把这个字加入poetry
        poetry.append(ch)
        token_id = tokenizer.token_to_id(ch)
        token_ids.append(token_id)

        while True:
            # 进行预测，只保留第一个样例（我们输入的样例数只有1）的、最后一个token的预测的、不包含[PAD][UNK][CLS]的概率分布
            prowords = model.predict([token_ids, ])[0, -1, 3:]

            # 根据得到的预测概率值进行逆序排序 并取得概率前100的结果的索引值（下标值）
            # argsort()得到的是下标 与实际的下标相差3 所以下面要加上3
            word_args = prowords.argsort()[::-1][:100]
            # 根据下标值取得真实的概率
            word_val = prowords[word_args]
            # 归一化
            p = word_val / sum(word_val)

            # 根据概率随机选取1个作为最终预测结果 选取概率不相同 以p中的概率为基准
            target_index = np.random.choice(len(word_val), p=p)
            #  把上步得到的概率值取下标加上3 得到实际的下标
            target = word_args[target_index] + 3
            token_ids.append(target)
            # 只有不是结束符才加入到poetry
            if target > 3:
                poetry.append(tokenizer.id_to_token(target))
            # 如果出现标点 本行就结束
            if target in label_ids:
                break
    return ''.join(poetry)

    
















