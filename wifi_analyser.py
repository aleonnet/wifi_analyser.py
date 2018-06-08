# INPUT:
# ----------------------------------------------------------------------
# #/bin/sh -e
# while true
# do sudo iwlist wlp2s0b1 scanning |\
# grep '\(Frequency\|ESSID\|Quality\)' | sed 'N;s/\n/ /;N;s/\n/ /' |\
# awk '{printf "%s %3s %s %s %s\n", $3, $4, $5, $7, $9}'
# echo DONE
# done
# ----------------------------------------------------------------------

import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from adjustText import adjust_text

r = r'.* (\d+)\)\s+Quality=(\d+)/70\s+level=-(\d+)\s+ESSID:"(.+)"'
wifi_plots = {}


def main():

    fig = plt.figure()
    scat = plt.scatter([], [], s=20)

    ax = fig.axes[0]
    ax.set_xlim([0, 14])
    ax.set_ylim([0, 70])
    ax.set_xticks(range(15))
    ax.set_xlabel('channel')
    ax.set_ylabel('quality')

    ani = FuncAnimation(fig, update, frames=range(1), fargs=(scat, fig))

    plt.show()


def band_plot(channel, signal):
    xdata = np.linspace(channel - 1, channel + 1)
    return xdata, [
        - signal * ((x - channel) ** 2 - 1)
        for x in xdata
    ]


def update(frame, scat, fig):

    networks = process_scan()

    # x = [int(network[0]) for network in networks]  # channels
    # y = [int(network[1]) for network in networks]  # networks quality
    # names = [network[-1] for network in networks]  # networks essids
    data = {
        network[-1]: np.array((int(network[0]), int(network[1])))
        for network in networks
    }

    ax = fig.axes[0]

    printed = {
        text.get_text(): text
        for text in ax.texts
    }

    n = set(data)
    p = set(printed)
    u = n.union(p)

    mark_new = u - p
    mark_update = n.intersection(p)
    mark_delete = u - n

    text_offset = (.3, .5)
    for essid in mark_update:
        printed[essid].set_position((
            data[essid][0] + text_offset[0],
            data[essid][1] + text_offset[1]
        ))
        xdata, ydata = band_plot(
            data[essid][0], data[essid][1])
        wifi_plots[essid].set_xdata(xdata)
        wifi_plots[essid].set_ydata(ydata)

    for essid in mark_new:
        ax.text(
            data[essid][0] + text_offset[0],
            data[essid][1] + text_offset[1],
            essid
        )
        xdata, ydata = band_plot(
            data[essid][0], data[essid][1])
        line, = ax.plot(xdata, ydata)
        wifi_plots[essid] = line

    for essid in mark_delete:
        printed[essid].remove()
        wifi_plots[essid].remove()

    scat.set_offsets(np.vstack(data[essid] for essid in data))
    colors = [wifi_plots[essid].get_markerfacecolor() for essid in data]
    scat.set_facecolors(colors)
    scat.set_edgecolors(colors)

    adjust_text(ax.texts)

    fig.canvas.draw()


def process_scan():
    networks = []
    while True:
        try:
            pre = input()
        except EOFError:
            return []
        if pre == 'DONE':
            return networks
        m = re.match(r, pre)
        # match groups are channel, quality, level, esssid in that order
        if m:
            networks.append(m.groups())
            # print(m.groups())


main()
