import re
import matplotlib.pyplot as plt
import numpy as np

pattern = re.compile(r'[^\u4e00-\u9fa5]')


def get_top_80_category():
    with open('texts.log', 'r', encoding='utf-8') as f:
        category = f.readlines()

    category = [re.sub(pattern, '', c) for c in category]
    dict_cat = {}
    for c in category:
        if c in dict_cat.keys():
            dict_cat[c] += 1
        else:
            dict_cat[c] = 1

    list_cat = sorted(dict_cat.items(), key=lambda x: x[1], reverse=True)
    x = np.array(list_cat)[:, 0]
    y = np.array(list_cat)[:, 1]

    with open('text_top_80.txt', 'w') as f:
        for i in range(80):
            f.writelines([x[i], '\n'])

    plt.plot(y)
    plt.show()


def format_texts_set():
    with open('text_top_80.txt', 'r') as f:
        category = f.readlines()
    category = [c.strip() for c in category]

    with open('texts.log', 'r', encoding='utf-8') as f:
        labels = f.readlines()
    ls = [l.strip() for l in labels]
    texts_f = np.load('./data/data.npz')['texts']
    imgs = []
    labels = []
    for l in ls:
        try:
            index = int(l.split(' ')[0])
            label = l.split(' ')[1]
            if label in category:
                imgs.append(texts_f[index, :, :])
                labels.append(category.index(label))
        except:
            pass
    np.savez('./data/texts.npz', texts=imgs, labels=labels)


def load_texts_set_test():
    f = np.load('./data/texts.npz')
    print(f['texts'].shape)
    print(f['labels'].shape)


if __name__ == '__main__':
    get_top_80_category()
    format_texts_set()
    load_texts_set_test()
