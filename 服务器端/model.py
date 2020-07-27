import tensorflow as tf
from dataprocess import tokenizer

# 构建模型
model = tf.keras.Sequential([
    # 不定长输入
    tf.keras.layers.Input((None,)),
    # 词嵌入层
    tf.keras.layers.Embedding(input_dim=tokenizer.vocabulary_size, output_dim=128),
    # 第一个 LSTM层
    tf.keras.layers.LSTM(128, dropout=0.5, return_sequences=True),

    tf.keras.layers.LSTM(128, dropout=0.5, return_sequences=True),
    # 预测下一个词的概率
    tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(tokenizer.vocabulary_size, activation='softmax')),

])


model.summary()
# 配置优化器 损失函数
model.compile(optimizer=tf.keras.optimizers.Adam(), loss=tf.keras.losses.categorical_crossentropy)

