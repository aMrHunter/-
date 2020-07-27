import tensorflow as tf
from dataprocess import tokenizer
import write
import os
BEST_MODEL_PATH = './best_model.h5'
gpu_no = '0' # or '1'
os.environ["CUDA_VISIBLE_DEVICES"] = gpu_no

# 定义TensorFlow配置
config = tf.compat.v1.ConfigProto()

# 配置GPU内存分配方式，按需增长，很关键
config.gpu_options.allow_growth = True

# 配置可使用的显存比例
config.gpu_options.per_process_gpu_memory_fraction = 0.1

# 在创建session的时候把config作为参数传进去
sess = tf.compat.v1.InteractiveSession(config=config)

model = tf.keras.models.load_model(BEST_MODEL_PATH)

i = int(input('请输入123其中一个数（其中1是随机生成，2是续写，3是藏头诗）：'))

if i == 1:
    print(write.generate_random(tokenizer, model))
elif i == 2:
    s = input('请输入部分信息（七个字以内）：')
    if len(s) <= 7:
        print(write.generate_random(tokenizer, model, s=s))
    else:
        print('输入不符合要求')
elif i == 3:
    head = input('请输入藏头字（字数为偶数）：')
    if len(head) % 2 == 0:
        print(head)
        print(write.generator_head(tokenizer, model, head=head))
    else:
        print('输入不符合要求')
else:
    print('输入不符合要求')