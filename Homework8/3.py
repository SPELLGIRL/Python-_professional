#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

t = np.arange(0, 2 * np.pi, 0.01)
r = (np.sin(t) * np.sqrt(np.abs(np.cos(t)))) / (np.sin(t) + 7 / 5) -\
    2 * np.sin(t) + 2
ax = plt.subplot(111, projection='polar')
ax.plot(t, r)
ax.set(rmax=4, rticks=[], rlabel_position=-22.5)
ax.grid()

ax.set_title("Heart", va='bottom')
plt.show()
