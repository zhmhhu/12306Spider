# 12360Spider

基于 [easy12306](https://github.com/zhaipro/easy12306),感谢[作者](https://github.com/zhaipro)。

区别在于 easy12306 基于 api 接口，而12306 的所有接口都不能直接爬了。
本项目基于 pyppeteer 模拟浏览器进行登录。验证码识别操作仍然使用 easy12306 项目的深度学习方法。

## 启动

本项目基于 python3.6

如果不考虑深度学习的识别过程，直接看效果的话，启动 zt12306Spider.py。

## 验证码识别
验证码识别基于深度学习算法，包括数据集的采集，预处理数据，训练算法，得到模型，等等。

### 运行顺序
1. 运行`pretreatment.py`得到`data.npz`数据集，里面包含所有的`labels`的图片数据，以及所有待选择图片的`whash`值。其中，原始图片数据下载较慢，可以到 kaggle 上下载，点击[此处](https://www.kaggle.com/wangsai9386/starter-12306-captcha-image-e6917dec-a)，然后将所有图片放入 imgs 文件夹下
2. 保存好了`data.npz`后，运行`baidu.py`,从百度OCR的API去识别这些`labels`上面的文字。并保存到`texts.log`中。
3. 运行`get_top80_category.py`，通过频次统计，发现其实12306的验证码图片就80类，获取这80类识别正确的labels图片与识别结果，作为`texts.npz`数据集，识别的80类（高频）放在了`text_top_80.txt`中。由于我爬取的图片只有8000多张，正确识别的只有4800张左右，识别的80类还是有点问题，具体的80类可以参考[zhaipro/easy12306的repo](https://github.com/zhaipro/easy12306/blob/master/texts.txt)，用这个文件替换`text_top_80.txt`。
4. 用生成的`texts.npz`作为数据集，跑`mlearn.py`文件，运行其中的main函数，得到`models.v1.0.h5`模型。
5. 跑`category_images.py`得到`captcha.npz`数据集。
6. 运行`mlearn_for_images.py`得到图片识别模型。
