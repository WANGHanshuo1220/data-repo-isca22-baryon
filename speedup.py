# %%
import numpy as np
import matplotlib.pyplot as plt
import easypyplot
import pandas as pd

# speedup
# prepare ordered workload list
speedup_csv = pd.read_csv('/scorpio/home/liyiwei/pom-research/plot-micro21/data-repo-micro21-baryon/1_performance/speedup.csv')
low_wl = ['503', '508', '521', '523', '525', '526', '531', '544']
medium_wl = ['507', '510']
high_wl = ['502', '505', '519', '520', '549', '554', '557']
mix_wl = ['mix1', 'mix2', 'mix3', 'mix4']
speedup_2darr = []
wl_list = []
for idx, workload in speedup_csv.iterrows():
    wl_name = workload['Benchmark']
    if any(low_id in wl_name for low_id in low_wl):
        wl_list.append(wl_name)
        speedup_2darr.append([workload['AllSlow Speedup'], workload['Hybrid2 Speedup'], workload['Baryon Speedup']])
for idx, workload in speedup_csv.iterrows():
    wl_name = workload['Benchmark']
    if any(medium_id in wl_name for medium_id in medium_wl):
        wl_list.append(wl_name)
        speedup_2darr.append([workload['AllSlow Speedup'], workload['Hybrid2 Speedup'], workload['Baryon Speedup']])
for idx, workload in speedup_csv.iterrows():
    wl_name = workload['Benchmark']
    if any(high_id in wl_name for high_id in high_wl):
        wl_list.append(wl_name)
        speedup_2darr.append([workload['AllSlow Speedup'], workload['Hybrid2 Speedup'], workload['Baryon Speedup']])
for idx, workload in speedup_csv.iterrows():
    wl_name = workload['Benchmark']
    if any(mix_id in wl_name for mix_id in mix_wl):
        wl_list.append(wl_name)
        speedup_2darr.append([workload['AllSlow Speedup'], workload['Hybrid2 Speedup'], workload['Baryon Speedup']])
for idx, workload in speedup_csv.tail(3).iterrows():
    wl_list.append(workload['Benchmark'])
    speedup_2darr.append([workload['AllSlow Speedup'], workload['Hybrid2 Speedup'], workload['Baryon Speedup']])

group_name = ['SlowMem', 'Hybrid2', 'Baryon']
fig_dims = (10, 2.5)
fig_name = '{}'.format("graph_speedup")
pp, fig = easypyplot.pdf.plot_setup(fig_name, fig_dims)
ax = fig.gca()
easypyplot.format.turn_off_box(ax)

# x ticks
group_xticks = []
xtick_beg = 0
color_item = [easypyplot.color.COLOR_SET[i] for i in [2, 0, 1]]
hdls = []
for idx, speedup in enumerate(speedup_2darr):
    group_xticks.append(xtick_beg)
    xtick_beg += 1
    if idx == len(wl_list) - 4:
        xtick_beg += 0.5 # gap for geomean items

bar_width = 0.7
hdls = easypyplot.barchart.draw(ax, speedup_2darr, width=bar_width, breakdown=False, xticks=group_xticks, group_names=wl_list, colors=color_item)
ax.set_xticklabels([], fontsize=8)
ax.set_xlim([ax.get_xticks()[0] - 1, ax.get_xticks()[-1] + 1])
ax.xaxis.set_ticks_position('none')

# y axis
ax.yaxis.grid(True)
ax.set_ylabel('Speedup over Hybrid2')
ax.set_ylim([0, 1.25])

plt.tight_layout()
easypyplot.format.resize_ax_box(ax, hratio=0.77)

# workload text
name_y_pos = -0.05
for idx, case in enumerate(wl_list):
    x = ax.get_xticks()[idx]
    ax.text(x, name_y_pos, case, ha='center', va='top', fontsize=9, rotation=90)

# speedup text
# for group_id in range(len(wl_list)):
#     for entry_id in range(2):
#         speedup = speedup_2darr[group_id][entry_id]
#         if entry_id % 2 == 0:
#             x = ax.get_xticks()[group_id] - bar_width / 4
#         else:
#             x = ax.get_xticks()[group_id] + bar_width / 4
#         x += 0.05 # a little offset
#         speedup_text = str(speedup)[0:5]
#         ax.text(x, speedup, speedup_text, ha='center', va='top', fontsize=8, rotation=90)
    
# Create legend
ax.legend(hdls, group_name, frameon=False, bbox_to_anchor=(0, 1.2), loc='upper left', ncol=3)

easypyplot.pdf.plot_teardown(pp)