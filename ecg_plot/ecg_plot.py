import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import os
from math import ceil 

# Global Constants
LEAD_INDEX = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
DEFAULT_PATH = './'
SHOW_COUNTER = 1

def _ax_plot(ax, x, y, secs, lwidth=0.5, amplitude_ecg=1.8, time_ticks=0.2):
    ax.set_xticks(np.arange(0, 11, time_ticks))    
    ax.set_yticks(np.arange(-ceil(amplitude_ecg), ceil(amplitude_ecg), 1.0))
    ax.minorticks_on()
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.set_ylim(-amplitude_ecg, amplitude_ecg)
    ax.set_xlim(0, secs)
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle='-', linewidth='0.5', color=(1, 0.7, 0.7))
    ax.plot(x, y, linewidth=lwidth)

def plot_12(ecg, sample_rate=500, title='ECG 12', lead_index=LEAD_INDEX, lead_order=None,
            columns=2, speed=50, voltage=20, line_width=0.6):
    """Plot multi lead ECG chart."""
    if not lead_order:
        lead_order = list(range(0, len(ecg)))

    leads = len(lead_order)
    seconds = len(ecg[0]) / sample_rate
    plt.rcParams.update({'font.size': 8})
    fig, ax = plt.subplots(
        ceil(len(lead_order)/columns), columns,
        sharex=True, 
        sharey=True,
        figsize=((speed/25) * seconds * columns, (4.1 * voltage/25) * leads / columns)
    )
    fig.subplots_adjust(hspace=0, wspace=0.04, left=0.04, right=0.98, bottom=0.06, top=0.95)
    fig.suptitle(title)
    step = 1.0 / sample_rate

    for i in range(0, len(lead_order)):
        t_ax = ax[i] if columns == 1 else ax[i//columns, i%columns]
        t_lead = lead_order[i]
        t_ax.set_ylabel(lead_index[t_lead])
        t_ax.tick_params(axis='x', rotation=90)
        _ax_plot(t_ax, np.arange(0, len(ecg[t_lead]) * step, step), ecg[t_lead], seconds, line_width)

def plot(ecg, sample_rate=500, title='ECG 12', lead_index=LEAD_INDEX, lead_order=None,
         style=None, columns=2, row_height=6, show_lead_name=True, show_grid=True, show_separate_line=True):
    """Plot multi lead ECG chart."""
    # Initial setup
    if not lead_order:
        lead_order = list(range(0, len(ecg)))

    secs, leads = len(ecg[0]) / sample_rate, len(lead_order)
    rows = int(ceil(leads / columns))
    display_factor = 1
    line_width = 0.5
    fig, ax = plt.subplots(figsize=(secs * columns * display_factor, rows * row_height / 5 * display_factor))
    display_factor = display_factor ** 0.5

    # Adjustments and settings
    fig.subplots_adjust(hspace=0, wspace=0, left=0, right=1, bottom=0, top=1)
    fig.suptitle(title)
    x_min, x_max, y_min, y_max = 0, columns * secs, row_height / 4 - (rows / 2) * row_height, row_height / 4
    colors = {
        'bw': ((0.4, 0.4, 0.4), (0.75, 0.75, 0.75), (0, 0, 0)),
        'default': ((1, 0, 0), (1, 0.7, 0.7), (0, 0, 0.7))
    }
    color_major, color_minor, color_line = colors['bw'] if style == 'bw' else colors['default']

    # Grid settings
    if show_grid:
        ax.set_xticks(np.arange(x_min, x_max, 0.2))    
        ax.set_yticks(np.arange(y_min, y_max, 0.5))
        ax.minorticks_on()
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        ax.grid(which='major', linestyle='-', linewidth=0.5 * display_factor, color=color_major)
        ax.grid(which='minor', linestyle='-', linewidth=0.5 * display_factor, color=color_minor)
    ax.set_ylim(y_min, y_max)
    ax.set_xlim(x_min, x_max)

    # Plotting
    step = 1.0 / sample_rate
    for c in range(0, columns):
        for i in range(0, rows):
            if c * rows + i < leads:
                y_offset = -(row_height / 2) * ceil(i % rows)
                x_offset = secs * c if c > 0 else 0
                if c > 0 and show_separate_line:
                    ax.plot([x_offset, x_offset], [ecg[t_lead][0] + y_offset - 0.3, ecg[t_lead][0] + y_offset + 0.3],
                            linewidth=line_width * display_factor, color=color_line)
                t_lead = lead_order[c * rows + i]
                if show_lead_name:
                    ax.text(x_offset + 0.07, y_offset - 0.5, lead_index[t_lead], fontsize=9 * display_factor)
                ax.plot(np.arange(0, len(ecg[t_lead]) * step, step) + x_offset, ecg[t_lead] + y_offset,
                        linewidth=line_width * display_factor, color=color_line)

def plot_1(ecg, sample_rate=500, title='ECG', fig_width=15, fig_height=2, line_w=0.5, ecg_amp=1.8, timetick=0.2):
    """Plot single lead ECG chart."""
    plt.figure(figsize=(fig_width, fig_height))
    plt.suptitle(title)
    plt.subplots_adjust(hspace=0, wspace=0.04, left=0.04, right=0.98, bottom=0.2, top=0.88)
    seconds = len(ecg) / sample_rate
    ax = plt.subplot(1, 1, 1)
    step = 1.0 / sample_rate
    _ax_plot(ax, np.arange(0, len(ecg) * step, step), ecg, seconds, line_w, ecg_amp, timetick)

def show():
    plt.show()

def save_as_png(file_name, path=DEFAULT_PATH, dpi=100, layout='tight'):
    plt.savefig(f"{path}{file_name}.png", dpi=dpi, bbox_inches=layout)
    plt.close()

def save_as_svg(file_name, path=DEFAULT_PATH):
    plt.savefig(f"{path}{file_name}.svg")
    plt.close()

def save_as_jpg(file_name, path=DEFAULT_PATH):
    plt.savefig(f"{path}{file_name}.jpg")
    plt.close()

def show_svg(tmp_path=DEFAULT_PATH):
    global SHOW_COUNTER
    file_name = f"{tmp_path}show_tmp_file_{SHOW_COUNTER}.svg"
    plt.savefig(file_name)
    os.system(f"open {file_name}")
    SHOW_COUNTER += 1
    plt.close()
