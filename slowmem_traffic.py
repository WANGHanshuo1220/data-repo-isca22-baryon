# %%
import numpy as np
import matplotlib.pyplot as plt
import easypyplot
import pandas as pd

# slowtraffic
# prepare ordered workload list
slowtraffic_csv = pd.read_csv('/scorpio/home/liyiwei/pom-research/plot-micro21/data-repo-micro21-baryon/2_energycost/slowtraffic.csv')
low_wl = ['503', '508', '521', '523', '525', '526', '531', '544']
medium_wl = ['507', '510']
high_wl = ['502', '505', '519', '520', '549', '554', '557']
mix_wl = ['mix1', 'mix2', 'mix3', 'mix4']
slowtraffic_2darr = []
wl_list = []
for idx, workload in slowtraffic_csv.tail(3).iterrows():
    wl_list.append(workload['Benchmark'])
    slowtraffic_2darr.append([1, workload['Normalized Traffic']])
    

group_name = ['Hybrid2', 'Baryon']
fig_dims = (5, 2.5)
fig_name = '{}'.format("graph_slow_traffic")
pp, fig = easypyplot.pdf.plot_setup(fig_name, fig_dims)
ax = fig.gca()
easypyplot.format.turn_off_box(ax, twinx_axes=ax2)

# x ticks
group_xticks = []
all_xticks = []
xtick_beg = 0
color_item = [easypyplot.color.COLOR_SET[i] for i in [0, 1]]
hdls = []
for idx, slowtraffic in enumerate(slowtraffic_2darr):
    group_xticks.append(xtick_beg)
    xticks = list(np.arange(xtick_beg, xtick_beg+len(slowtraffic_2darr) * bar_width, bar_width))
    all_xticks.append(xticks)
    xtick_beg += 1
    if idx == len(wl_list) - 4:
        xtick_beg += 0.5 # gap for geomean items

bar_width = 0.6
hdls = easypyplot.barchart.draw(ax, slowtraffic_2darr, width=bar_width, breakdown=False, xticks=group_xticks, group_names=wl_list, colors=color_item)
ax.set_xticklabels([], fontsize=8)
ax.set_xlim([ax.get_xticks()[0] - 1, ax.get_xticks()[-1] + 1])
ax.xaxis.set_ticks_position('none')

# y axis
ax.yaxis.grid(True)
ax.set_ylabel('Normalized Slow Memory Traffic')
ax.set_ylim([0, 1.5])

# y text
tick_x_list = []
for group_id in range(len(slowtraffic_2darr)):
    for entry_id in range(2):
        slowtraffic = slowtraffic_2darr[group_id][entry_id]
        x = ax.get_xticks()[group_id] + entry_id * bar_width / 2 - bar_width / 4
        tick_x_list.append(x)
        x += 0.03 # a little offset
        slowtraffic_text = "%.03f" % slowtraffic
        y_pos = min(slowtraffic, 5)
        ax.text(x, y_pos, slowtraffic_text, ha='center', va='top', fontsize=8, rotation=90)

plt.tight_layout()
easypyplot.format.resize_ax_box(ax, hratio=0.77)

# workload text
name_y_pos = -0.05
for idx, case in enumerate(wl_list):
    x = ax.get_xticks()[idx]
    ax.text(x, name_y_pos, case, ha='center', va='top', fontsize=9, rotation=90)

# Create legend
ax.legend(hdls, group_name, frameon=False, bbox_to_anchor=(0, 1.2), loc='upper left', ncol=3)

easypyplot.pdf.plot_teardown(pp)