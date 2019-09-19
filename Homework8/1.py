#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

# в градусах
a = np.arange(0, 730, 10)
# в радианах
r = np.radians(a)
v = 2 * r - np.cos(r)

fig, ax = plt.subplots()
ax.plot(a, v)

ax.set(xlabel='angle (a)', ylabel='speed (v)',
       title='y = 2*x - cos(x)')
ax.grid()

plt.show()
