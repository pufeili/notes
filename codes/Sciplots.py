#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
 @FileName  :Sciplots.py
 @Time      :2023/3/19 12:55
 @Author    :LPF
"""
import matplotlib.pyplot as plt
import numpy as np
import scienceplots


if __name__ == "__main__":
    pparam = dict(xlabel='Purity', ylabel=r'Accuracy')

    x = np.arange(0.5, 1.0, 0.05)
    y1 = np.array([64.25, 64.37, 64.78, 65.20, 64.93, 64.46, 64.34, 64.72, 65.28, 65.94])
    y2 = np.array([84.13, 84.80, 84.99, 86.11, 85.64, 85.64, 85.04, 85.60, 84.85, 84.87])

    with plt.style.context(['science', 'ieee', 'std-colors']):
        fig, ax = plt.subplots()
        ax2 = ax.twinx()  # 做镜像处理
        ax.plot(x, y1, '-', label='I → V')
        ax2.plot(x, y2, 'r--', label='V → I')
        fig.legend(title='Order', loc='upper left', bbox_to_anchor=(0, 1), bbox_transform=ax.transAxes)
        ax.autoscale(tight=True)
        ax2.autoscale(tight=True)

        ax.set(**pparam)

        # fig.savefig('figures/fig2b.pdf')
        fig.savefig('./fig.jpg', dpi=300)
        plt.show()
    run_code = 0
