#!/usr/bin/python

from PIL import Image, ImageFilter
import tensorflow as tf
import numpy as np
import string
import sys
import generate_captcha
import captcha_model
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

Height = 25
Width = 60
IMAGE_PIXELS = Height * Width

Model_dir = './'

def ocrCaptchas(images):
    """
    recognize the preprocessed image
    :param images: list of four images returned by processImg()
    :return: recognition result
    """
    image_data = []
    tf.reset_default_graph()
    for img in images:
        image_array = np.asarray(img, np.uint8)
        image = tf.decode_raw(image_array.tobytes(), tf.uint8)
        image.set_shape([IMAGE_PIXELS])
        image = tf.cast(image, tf.float32) * (1. / 255) - 0.5
        image_data.append(image)
    # w = tf.get_variable(name='w1', shape=[Height * Width, 10])
    w = tf.Variable(tf.zeros([Height * Width, 10]), name='w1')
    saver = tf.train.Saver()
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())
    with sess:
        saver.restore(sess, "capcha_model.ckpt")
        y_pred = tf.matmul(image_data, w)
        pred_array = np.asarray(sess.run(y_pred))
        result = []
        for item in pred_array:
            item[0] = -20  # It is impossible for the result to be 1
            index = np.argmax(item, 0)
            if index == 1:
                index = 0  # index 1 represents result 1 in truth
            result.append(index)
        return ''.join(str(e) for e in result)





if __name__ == '__main__':
    captcha = generate_captcha.generateCaptcha()
    width,height,char_num,characters,classes = captcha.get_parameter()

    gray_image = Image.open(sys.argv[1]).convert('L')
    img = np.array(gray_image.getdata())
    test_x = np.reshape(img,[height,width,1])/255.0
    x = tf.placeholder(tf.float32, [None, height,width,1])
    keep_prob = tf.placeholder(tf.float32)

    model = captcha_model.captchaModel(width,height,char_num,classes)
    y_conv = model.create_model(x,keep_prob)
    predict = tf.argmax(tf.reshape(y_conv, [-1,char_num, classes]),2)
    init_op = tf.global_variables_initializer()
    saver = tf.train.Saver()
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.1)
    with tf.Session(config=tf.ConfigProto(log_device_placement=False,gpu_options=gpu_options)) as sess:
        sess.run(init_op)
        saver.restore(sess, "capcha_model.ckpt")
        pre_list =  sess.run(predict,feed_dict={x: [test_x], keep_prob: 1})
        for i in pre_list:
            s = ''
            for j in i:
                s += characters[j]
            print (s)
