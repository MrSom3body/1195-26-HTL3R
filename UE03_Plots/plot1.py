__author__ = "Karun Sandhu"

import math
import matplotlib.pyplot as plt

background = "#292828"
background_light = "#504945"
foreground = "#ddc7a1"
red = "#ea6962"
blue = "#7daea3"

plt.rcParams.update(
    {
        # Figure & axes backgrounds
        "figure.facecolor": background,
        "axes.facecolor": background,
        # Text & label colors
        "text.color": foreground,
        "xtick.color": foreground,
        "ytick.color": foreground,
        # Axis
        "axes.edgecolor": foreground,
        # Background Box
        "patch.facecolor": background_light,
        # Arrows
        "patch.edgecolor": foreground,
    }
)

PI = math.pi

CNT = 1024
X = [(-PI) + i * (2 * PI / 1023) for i in range(1024)]
C = [math.cos(x) for x in X]
S = [math.sin(x) for x in X]

plt.title("Plot von Karun Sandhu, HTL3R")

plt.plot(X, C, color=blue, linewidth=2.5, label="Cosinus")
plt.plot(X, S, color=red, linewidth=2.5, label="Sinus")

plt.xticks(
    [-PI, -PI / 2, 0, PI / 2, PI],
    [r"$-\pi$", r"$-\frac{\pi}{2}$", r"$0$", r"$+\frac{\pi}{2}$", r"$+\pi$"],
)
plt.yticks([-1, 1], [r"$-1$", r"$+1$"])

plt.legend(loc="upper left", frameon=False)

ax = plt.gca()
ax.spines["right"].set_color("none")
ax.spines["top"].set_color("none")
ax.xaxis.set_ticks_position("bottom")
ax.spines["bottom"].set_position(("data", 0))
ax.yaxis.set_ticks_position("left")
ax.spines["left"].set_position(("data", 0))


t1 = 2 * PI / 3
plt.plot([t1, t1], [0, math.sin(t1)], color=red, linewidth=1, linestyle="--")
plt.scatter([t1], [math.sin(t1)], 25, color=red)
plt.plot([t1, t1], [0, math.cos(t1)], color=blue, linewidth=1, linestyle="--")
plt.scatter([t1], [math.cos(t1)], 25, color=blue)

plt.annotate(
    r"$\sin\left(\frac{2\pi}{3}\right)=\frac{\sqrt{3}}{2}$",
    xy=(t1, math.sin(t1)),
    xycoords="data",
    xytext=(+10, +30),
    textcoords="offset points",
    fontsize=16,
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),
)

plt.annotate(
    r"$\cos\left(\frac{2\pi}{3}\right)=-\frac{1}{2}$",
    xy=(t1, math.cos(t1)),
    xycoords="data",
    xytext=(-90, -50),
    textcoords="offset points",
    fontsize=16,
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),
)

t2 = math.radians(-45)
plt.plot([t2, t2], [0, math.sin(t2)], color=red, linestyle="--")
plt.scatter([t2], [math.sin(t2)], color=red)
plt.plot([t2, t2], [0, math.cos(t2)], color=blue, linestyle="--")
plt.scatter([t2], [math.cos(t2)], color=blue)

plt.annotate(
    r"$\sin(-45°)=-\frac{\sqrt{2}}{2}$",
    xy=(t2, math.sin(t2)),
    xycoords="data",
    xytext=(-100, -70),
    textcoords="offset points",
    fontsize=16,
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),
)

plt.annotate(
    r"$\cos(-45°)=\frac{\sqrt{2}}{2}$",
    xy=(t2, math.cos(t2)),
    xycoords="data",
    xytext=(-170, -50),
    textcoords="offset points",
    fontsize=16,
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-.2"),
)

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(16)
    label.set_bbox(dict(edgecolor="None", alpha=0.65))
ax.set_axisbelow(False)

plt.savefig("plot1_sandhu.png", dpi=500)
