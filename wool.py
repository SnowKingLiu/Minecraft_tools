# _*_ coding: utf-8 _*_
# by:Snowkingliu
# 2018/1/9 下午1:22
from PIL import Image
import numpy as np


def main():
    colours = {
        "White": 0xE9ECEC,
        "Orange": 0xF07613,
        "Magenta": 0xBD44B3,
        "Light_blue ": 0x3AAFD9,
        "Yellow": 0xF8C627,
        "Lime": 0x70B919,
        "Pink": 0xED8DAC,
        "Gray": 0x3E4447,
        "Light_gray": 0x8E8E86,
        "Cyan": 0x158991,
        "Purple": 0x792AAC,
        "Blue": 0x35399D,
        "Brown": 0x724728,
        "Green": 0x546D1B,
        "Red": 0xA12722,
        "Black": 0x141519,
    }
    # 打开一张图片
    img = Image.open('50.png')
    img_size = img.size
    new_img = Image.new(img.mode, img_size)
    colours_tuple = get_colors_tuple(colours)
    data_mat, colour_label = get_colour_map(colours_tuple)

    for i in range(img_size[0]):
        for j in range(img_size[1]):
            a_point = img.getpixel((i,j))
            new_point = get_similarity(a_point, data_mat, colour_label)
            new_img.putpixel((i, j), new_point)
    new_img.save("new50.png")


def get_similarity(a_point, data_mat, colour_label):
    if a_point[3] == 0:
        return 0, 0, 0, 0
    # diffMat是a_point[0:3]与data_mat每一个值的差组成的矩阵
    diff_mat = np.tile(np.array(a_point[0:3]), (len(data_mat), 1)) - data_mat
    # 获取各项的差的平方
    sq_diff_mat = diff_mat ** 2
    sq_distance = sq_diff_mat.sum(axis=1)
    # 开根号
    distance = sq_distance ** 0.5
    sorted_dist_indicies = distance.argsort()
    return tuple([int(color) for color in data_mat[sorted_dist_indicies[0]]])


def get_colors_tuple(colours):
    res = {}
    for a_color, color_data in colours.items():
        red = int(color_data/(256 * 256))
        green = int((color_data - (256 * 256) * red)/256)
        bule = int(color_data % 256)
        res[a_color] = (red, green, bule)
    return res


def get_colour_map(colours_tuple):
    data_mat = np.zeros((len(colours_tuple), 3))
    colour_label = []
    i = 0
    for a_color, color_data in colours_tuple.items():
        colour_label.append(a_color)
        data_mat[i, :] = np.array(color_data)
        i += 1
    return data_mat, colour_label


if __name__ == '__main__':
    main()
