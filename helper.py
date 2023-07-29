"""
Date created: 4/28/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Contributors:
    https://github.com/josephedradan

Reference:

"""
import matplotlib.pyplot as plt
from IPython import display
# plt.ion()

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# import tkinter as tk

# root = tk.Tk()
figure, axes = plt.subplots()

ax: plt.Axes = axes

print(type(ax))

# figure_canvas = FigureCanvasTkAgg(figure, master=root)
# figure_canvas.get_tk_widget().pack()  # Place the canvas into tkinter


def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    # plt.clf()  # Clear the figure, works on plt only

    ax.clear()  # Clear the axis

    ax.set_title('Training...')
    ax.set_xlabel('Number of Games')
    ax.set_ylabel('Score')

    ax.plot(scores)
    ax.plot(mean_scores)

    ax.set_ylim(ymin=0)
    ax.text(len(scores)-1, scores[-1], str(scores[-1]))
    ax.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    # figure_canvas.draw()

    # plt.show(block=False)  # Does not work with tkinter, use figure_canvas.draw()
    # plt.pause(.1)  # Does not work with tkinter



# root.mainloop()
