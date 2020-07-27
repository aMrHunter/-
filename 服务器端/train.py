
import tensorflow as tf
from dataprocess import PDGenerator, poetry, tokenizer
from model import model
import write

# 最佳权重保存路径
BEST_MODEL_PATH = './best_model.h5'
TRAIN_EPOCHS = 20

loss_value = []


class Evaluate(tf.keras.callbacks.Callback):
    """
    定义一个evaluate类，它继承了tensorflow中自带的一个Callback类 作为模型的回调函数
    也就是每次epoch完成后 调用一次
    """

    def __init__(self):
        # 调用了super初始化了父类的构造函数
        # 当需要继承父类构造函数中的内容，
        # 且子类需要在父类的基础上补充时，使用super().__init__()方法
        super().__init__()
        # 赋一个较大的初始值
        self.lowest = 1e10

    def on_epoch_end(self, epoch, logs=None):
        # 每个epoch训练完后调用 如果当前loss更低 就保存当前模型
        # 也可以设置logs['loss'] 小于一个值时候停止训练
        loss_value.append(logs['loss'])
        print(loss_value)
        if logs['loss'] <= self.lowest:
            self.lowest = logs['loss']
            model.save(BEST_MODEL_PATH)

        # 随机生成几首 看看效果
        # print()
        #   for i in range(5):
        #    print(write.generate_random(tokenizer, model))


# 创建数据集生成器
dataset = PDGenerator(poetry, random=True)

# 生成器与模型并行运行，以提高效率
model.fit_generator(dataset.for_fit(), steps_per_epoch=dataset.steps,
                    epochs=TRAIN_EPOCHS,
                    callbacks=[Evaluate()])



