# coding: utf-8
import numpy
import random


def random_linspace(num, length):
    """辅助函数
    传入要分成的几段 -> num ；长度 -> length, 生成一个递增的、随机的、不严格等差数列
    """
    # 数列的起始值 、 结束值。 这里以平均值的 0.5 作为起始值，平均值的 1.5倍作为结束值。
    start, end = 0.5 * (length / num), 1.5 * (length / num)
    # 借助三方库生成一个标准的等差数列，主要是得出标准等差 space
    origin_list = numpy.linspace(start, end, num)
    space = origin_list[2] - origin_list[1]
    # 在标准等差的基础上，设置上下浮动的大小，（上下浮动10%）
    min_random, max_random = -(space / 10), space / 10
    result = []
    # 等差数列的初始值不变，就是我们设置的start
    value = start
    # 将等差数列添加到 list
    result.append(value)
    # 初始值已经添加，循环的次数 减一
    for i in range(num - 1):
        # 浮动的等差值 space
        random_space = space + random.uniform(min_random, max_random)
        value += random_space
        result.append(value)
    return result


def slide_list(total_length):
    """等差数列生成器，根据传入的长度，生成一个随机的，先递增后递减，不严格的等差数列"""
    # 具体分成几段是随机的
    total_num = random.randint(10, 15)

    # 中间的拐点是随机的
    mid = total_num - random.randint(3, 5)

    # 第一段、第二段的分段数
    first_num, second_num = mid, total_num - mid

    # 第一段、第二段的长度，根据总长度，按比例分成
    first_length, second_length = (
        total_length * (first_num / total_num),
        total_length * (second_num / total_num),
    )

    # 调用上面的辅助函数，生成两个随机等差数列
    first_result = random_linspace(first_num, first_length)
    second_result = random_linspace(second_num, second_length)

    # 第二段等差数列进行逆序排序
    slide_result = first_result + second_result[::-1]

    # 由于随机性，判断一下总长度是否满足，不满足的再补上一段
    if sum(slide_result) < total_length:
        slide_result.append(total_length - sum(slide_result))
    return slide_result
