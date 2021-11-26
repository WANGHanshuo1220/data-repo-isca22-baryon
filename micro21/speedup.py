# %%
import numpy as np
import matplotlib.pyplot as plt
import easypyplot
import pandas as pd
low_wl = ['503', '508', '521', '523', '525', '526', '531', '544', 'Freqmine', 'Fluidaminate', 'Blackscholes', '507', '510', 'Raytrace', 'Dedup']
high_wl = ['502', '505', '519', '520', '549', '554', '557', 'Canneal']
mix_wl = ['mix1', 'mix2', 'mix3', 'mix4']

# speedup
# prepare ordered workload list
speedup_csv = pd.read_csv('./1_performance/speedup.csv')
speedup_2darr = []
wl_list = []
for idx, workload in speedup_csv.iterrows():
    wl_name = workload['Benchmark']
    if any(low_id in wl_name for low_id in low_wl):
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
for idx, workload in speedup_csv.tail(2).iterrows():
    wl_list.append(workload['Benchmark'])
    speedup_2darr.append([workload['AllSlow Speedup'], workload['Hybrid2 Speedup'], workload['Baryon Speedup']])

group_name = ['Slow-Only', 'Hybrid2', 'Baryon']
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
    if idx == len(low_wl) - 1:
        xtick_beg += 0.5 # gap between categories
    if idx == len(wl_list) - 3:
        xtick_beg += 0.5 # gap for geomean items

bar_width = 0.7
hdls = easypyplot.barchart.draw(ax, speedup_2darr, width=bar_width, breakdown=False, xticks=group_xticks, group_names=wl_list, colors=color_item)
ax.set_xticklabels([], fontsize=8)
ax.set_xlim([ax.get_xticks()[0] - 1, ax.get_xticks()[-1] + 1])
ax.xaxis.set_ticks_position('none')

# y axis
ax.yaxis.grid(True)
ax.set_ylabel('Normalized Performance')
ax.set_ylim([0, 1.25])

fig.tight_layout()
easypyplot.format.resize_ax_box(ax, hratio=0.77)

# workload text
name_y_pos = -0.05
for idx, case in enumerate(wl_list):
    x = ax.get_xticks()[idx]
    ax.text(x, name_y_pos, case, ha='right', va='top', fontsize=9, rotation=30)

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
ax.legend(hdls, group_name, frameon=False, bbox_to_anchor=(0, 1.1), loc='upper left', ncol=3)

easypyplot.pdf.plot_teardown(pp)
