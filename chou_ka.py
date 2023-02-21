import random
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

sp_rate = 0.0025
ssr_rate = 0.01
sr_rate = 0.2
r_rate = 0.7875

sp_rate_up = sp_rate * 2.5
ssr_rate_up = ssr_rate * 2.5
sr_rate_up = (1 - sp_rate_up - ssr_rate_up) * sr_rate / (sr_rate + r_rate)
r_rate_up = (1 - sp_rate_up - ssr_rate_up) * r_rate / (sr_rate + r_rate)

rate_list = [sp_rate, ssr_rate, sr_rate, r_rate]
rate_up_list = [sp_rate_up, ssr_rate_up, sr_rate_up, r_rate_up]

old_dic = {'sp': {'qt': {0: 0.1, 50: 0.15, 100: 0.2, 150: 0.25, 200: 0.3, 250: 0.35, 300: 0.4, 350: 0.5, 400: 0.6, 450: 0.8, 500: 1},
                  'fqt': {0: 0.03, 50: 0.04, 100: 0.05, 150: 0.06, 200: 0.08, 250: 0.1, 300: 0.11, 350: 0.12, 400: 0.13, 450: 0.14, 500: 0.15, 600: 0.25}},
           'ssr': {'qt': {0: 0.15, 50: 0.2, 100: 0.25, 150: 0.3, 200: 0.35, 250: 0.4, 300: 0.5, 350: 0.6, 400: 0.7, 450: 0.8, 500: 1},
                   'fqt': {0: 0.04, 50: 0.05, 100: 0.06, 150: 0.08, 200: 0.1, 250: 0.11, 300: 0.12, 350: 0.13, 400: 0.14, 450: 0.15, 500: 0.2, 600: 0.3}}}

new_dic = {'sp': {'qt': {0: 0.1, 60: 0.12, 120: 0.14, 180: 0.18, 240: 0.25, 300: 0.4, 360: 0.55, 420: 0.8, 450: 1},
                  'fqt': {0: 0.03, 60: 0.05, 120: 0.08, 180: 0.1, 240: 0.15, 300: 0.2, 360: 0.25, 420: 0.3, 480: 0.4, 540: 0.5, 600: 0.7, 660: 0.8, 720: 0.9, 780: 1}},
           'ssr': {'qt': {0: 0.1, 60: 0.12, 120: 0.14, 180: 0.18, 240: 0.25, 300: 0.4, 360: 0.55, 420: 0.8, 450: 1},
                   'fqt': {0: 0.03, 60: 0.05, 120: 0.08, 180: 0.1, 240: 0.15, 300: 0.2, 360: 0.25, 420: 0.3, 480: 0.4, 540: 0.5, 600: 0.7, 660: 0.8, 720: 0.9, 780: 1}}}

result = {'sp': np.array([1, 0, 0, 0]), 'ssr': np.array([0, 1, 0, 0]), 'sr': np.array([0, 0, 1, 0]),
          'r': np.array([0, 0, 0, 1])}


def simulate(rate):
    [r1, r2, r3] = rate[:-1]
    r = random.random()
    if r < r1:
        return 'sp'
    elif r < r1 + r2:
        return 'ssr'
    elif r < r1 + r2 + r3:
        return 'sr'
    else:
        return 'r'


def random_sp_ssr():
    r = random.random()
    if r < sp_rate / (sp_rate + ssr_rate):
        return 'sp'
    elif sp_rate / (sp_rate + ssr_rate) <= r:
        return 'ssr'


def is_current_old(n, shishen_type, qt):
    rate_curve = old_dic[shishen_type][qt]
    keys = list(rate_curve.keys())
    current_rate = 0
    for i in range(len(keys)):
        if i < len(keys) - 1:
            if keys[i] <= n < keys[i + 1]:
                current_rate = rate_curve[keys[i]]
                break
        elif i == len(keys) - 1:
            if keys[i] <= n:
                current_rate = rate_curve[keys[i]]
    r = random.random()
    if r < current_rate:
        return True
    else:
        return False


def is_current_new(n, shishen_type, qt):
    rate_curve = new_dic[shishen_type][qt]
    keys = list(rate_curve.keys())
    current_rate = 0
    for i in range(len(keys)):
        if i < len(keys) - 1:
            if keys[i] <= n < keys[i + 1]:
                current_rate = rate_curve[keys[i]]
                break
        elif i == len(keys) - 1:
            if keys[i] <= n:
                current_rate = rate_curve[keys[i]]
    r = random.random()
    if r < current_rate:
        return True
    else:
        return False


def old_mode(n, shishen_type, qt):
    up = 0
    flag = True
    shishen = np.zeros([n, 4])
    for i in range(n):
        if i == 599 and qt == 'qt' and flag:
            flag = False
            shishen[i, :] = shishen[i - 1, :] + result[shishen_type]
            continue
        if up < 3:
            tmp = simulate(rate_up_list)
            if tmp in ['sp', 'ssr']:
                up += 1
                if is_current_old(i + 1, shishen_type, qt):
                    flag = False
            if i == 0:
                shishen[i, :] = result[tmp]
            else:
                shishen[i, :] = shishen[i - 1, :] + result[tmp]
        else:
            tmp = simulate(rate_list)
            if tmp in ['sp', 'ssr'] and is_current_old(i + 1, shishen_type, qt):
                flag = False
            shishen[i, :] = shishen[i - 1, :] + result[tmp]
    return shishen


def new_mode(n, shishen_type, qt):
    shishen = np.zeros([n, 4])
    counter = 0
    flag = True
    for i in range(n):
        if i == 39:
            tmp = random_sp_ssr()
            shishen[i, :] = shishen[i - 1, :] + result[tmp]
            if is_current_new(n, shishen_type, qt):
                flag = False
            continue
        if i == 449 and qt == 'qt' and flag:
            shishen[i, :] = shishen[i - 1, :] + result[shishen_type]
            counter = 0
            continue
        if i == 799 and qt == 'fqt' and flag:
            shishen[i, :] = shishen[i - 1, :] + result[shishen_type]
            counter = 0
            continue
        if counter < 59:
            tmp = simulate(rate_list)
            if i == 0:
                shishen[i, :] = result[tmp]
            else:
                shishen[i, :] = shishen[i - 1, :] + result[tmp]
            if tmp in ['sp', 'ssr']:
                counter = 0
                if is_current_new(n, shishen_type, qt):
                    flag = False
            else:
                counter += 1
        elif counter == 59:
            counter = 0
            tmp = random_sp_ssr()
            shishen[i, :] = shishen[i - 1, :] + result[tmp]
            if is_current_new(n, shishen_type, qt):
                flag = False
    return shishen


if __name__ == '__main__':
    iteration = int(1e5)
    num = 800
    data = np.zeros([num, 4])

    for m in tqdm(range(iteration), desc='Progress', ncols=100):
        tmp1 = new_mode(800, 'sp', 'qt')
        data += tmp1
    data /= iteration

    fig = plt.figure(figsize=(10, 6))
    plt.plot(data[:, 0])
    plt.plot(data[:, 1])
    plt.plot(data[:, 2])
    plt.plot(data[:, 3])
    plt.plot(data[:, 0] + data[:, 1])
    plt.xlabel('n')
    plt.ylabel('num')
    plt.legend(['sp', 'ssr', 'sr', 'r', 'sp+ssr'])
    plt.ylim([0, 15])
    plt.grid()
    fig.tight_layout()
    plt.show()
