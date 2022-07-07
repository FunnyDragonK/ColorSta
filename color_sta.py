# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 21:35:55 2022

@author: chen
"""
import cv2
import numpy as np

color_def = {
    "黑": {"h": [[0, 180]], "s": [[0, 255]], "v": [[0, 46]]},
    "灰": {"h": [[0, 180]], "s": [[0, 43]], "v": [[46, 220]]},
    "白": {"h": [[0, 180]], "s": [[0, 30]], "v": [[221, 255]]},
    "红": {"h": [[0, 10], [156, 180]], "s": [[43, 255]], "v": [[46, 255]]},
    "橙": {"h": [[11, 25]], "s": [[43, 255]], "v": [[46, 255]]},
    "黄": {"h": [[26, 34]], "s": [[43, 255]], "v": [[46, 255]]},
    "绿": {"h": [[35, 77]], "s": [[43, 255]], "v": [[46, 255]]},
    "青": {"h": [[78, 99]], "s": [[43, 255]], "v": [[46, 255]]},
    "蓝": {"h": [[100, 124]], "s": [[43, 255]], "v": [[46, 255]]},
    "紫": {"h": [[125, 155]], "s": [[43, 255]], "v": [[46, 255]]},
}


def list_or(bool_list: list) -> np.ndarray:
    """
    :param bool_list: list of np.array
    :return: list
    """
    assert len(bool_list) > 0
    res = bool_list[0]
    for i in range(1, len(bool_list)):
        res = res | bool_list[i]
    return res


def list_and(bool_list: list) -> np.ndarray:
    """
    :param bool_list: list of np.array
    :return: list
    """
    assert len(bool_list) > 0
    res = bool_list[0]
    for i in range(1, len(bool_list)):
        res = res & bool_list[i]
    return res


def color_sta(image: np.ndarray) -> dict:
    """
    :param image: hsv image
    :return: percentage of every pre-defined color
    """
    color_cnt = {}
    for key, val in color_def.items():
        res_temp = []
        for i, (name, range_list) in enumerate(val.items()):
            clip = image[:, :, i]
            temp_list = []
            for item in range_list:
                temp_list.append((item[0] < clip) * (clip < item[1]))
            res_temp.append(list_or(temp_list))
        res = list_and(res_temp)
        color_cnt[key] = res.sum()
    temp = sorted(color_cnt.items(), key=lambda x: x[1], reverse=True)
    total_num = sum([x[1] for x in temp])
    color_percent_cnt = {key: val / total_num for key, val in temp}
    return color_percent_cnt


if __name__ == "__main__":
    image_path = "/Users/luweichen/Downloads/01475461bb572911013e8cd0185258.jpg@1280w_1l_2o_100sh.jpg"
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    color_cnt = color_sta(image)
    print(color_cnt)
