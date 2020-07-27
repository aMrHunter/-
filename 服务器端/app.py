from flask import Flask, request, jsonify
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

app = Flask(__name__)

a = "1,2,3"
@app.route('/index', methods=['GET', 'POST'])
def dataprocess():
    # head = request.form['head']
    # print(head)
    s = request.form

    head = s['head']

    sort = s['sort']
    print(sort)
    poem = []
    if sort == '0':
        poem = generate_random()
    elif sort == '1':
        poem = generate_head(head)
    else:
        poem = generate_gon(head)

    print(poem)
    data = {
        "body": poem

    }
    print(data)
    return jsonify(data)


def generate_random():

    poem = write.generate_random(tokenizer, model)
    return poem


def generate_head(s):

    print(s)

    # if sort == 0:
    #
    #     return poem
    # elif sort == 1:
    poem = write.generator_head(tokenizer, model, head=s)
    return poem


def generate_gon(s):
    poem = write.generate_random(tokenizer, model, s)

    return poem

# @app.route('/log')
# def sad():
#     return '1234'


if __name__ == '__main__':
    app.run(debug=True)
