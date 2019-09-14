#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

a = np.arange(0, 730, 10)
v = a ** 3 - np.sqrt(a)

fig, ax = plt.subplots()
ax.plot(a, v)

ax.set(xlabel='time (a)', ylabel='speed (v)',
       title='y = x^3 - sqrt(x)')
ax.grid()

plt.show()
