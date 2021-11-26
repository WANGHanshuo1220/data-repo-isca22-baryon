# %%
import numpy as np
import matplotlib.pyplot as plt
import easypyplot
import pandas as pd
low_wl = ['503', '508', '521', '523', '525', '526', '531', '544', 'Bellmanford', 'Freqmine', 'Fluidaminate', 'Blackscholes']
medium_wl = ['507', '510', 'Raytrace', 'Dedup']
high_wl = ['502', '505', '519', '520', '549', '554', '557']
mix_wl = ['mix1', 'mix2', 'mix3', 'mix4']

# superblock scope
# prepare ordered workload list
mpki_csv = pd.read_csv('./3_sensitivity/blksize.csv')
hitrate_2darr = []
wl_list = []
for idx, workload in mpki_csv.iterrows():
    wl_name = workload['Benchmark']
    if any(mix_id in wl_name for mix_id in mix_wl):
        wl_list.append(wl_name)
        hitrate_2darr.append([workload['1k_256_64 Hitrate'], workload['2k_256_64 Hitrate'], workload['4k_256_64 Hitrate'], workload['512_64_16 Hitrate']])

group_name = ['1kB-256B-64B', '2kB-256B-64B', '4kB-256B-64B', '512B-64B-16B']
fig_dims = (5, 1.8)
fig_name = '{}'.format("graph_blksize")
pp, fig = easypyplot.pdf.plot_setup(fig_name, fig_dims)
ax = fig.gca()
easypyplot.format.turn_off_box(ax)

# x ticks
group_xticks = []
xtick_beg = 0
color_item = [easypyplot.color.COLOR_SET[i] for i in [0, 1, 2, 3]]
hdls = []
for idx, mpki in enumerate(hitrate_2darr):
    group_xticks.append(xtick_beg)
    xtick_beg += 1

bar_width = 0.7
hdls = easypyplot.barchart.draw(ax, hitrate_2darr, width=bar_width, breakdown=False, xticks=group_xticks, group_names=wl_list, colors=color_item)
ax.set_xticklabels([], fontsize=8)
ax.set_xlim([ax.get_xticks()[0] - 1, ax.get_xticks()[-1] + 1])
ax.xaxis.set_ticks_position('none')
# y axis
ax.yaxis.grid(True)
ax.set_ylabel('Normalized Hitrate')
ax.set_ylim([0.8, 1.00])

fig.tight_layout()
easypyplot.format.resize_ax_box(ax, hratio=0.9)

# workload text
name_y_pos = 0.785
for idx, case in enumerate(wl_list):
    x = ax.get_xticks()[idx]
    ax.text(x, name_y_pos, case, ha='center', va='top', fontsize=9, rotation=0)

# mpki text
# for group_id in range(len(wl_list)):
#     for entry_id in range(2):
#         mpki = hitrate_2darr[group_id][entry_id]
#         if entry_id % 2 == 0:
#             x = ax.get_xticks()[group_id] - bar_width / 4
#         else:
#             x = ax.get_xticks()[group_id] + bar_width / 4
#         x += 0.05 # a little offset
#         mpki_text = str(mpki)[0:5]
#         ax.text(x, mpki, mpki_text, ha='center', va='top', fontsize=8, rotation=90)
    
# Create legend
ax.legend(hdls, group_name, frameon=False, bbox_to_anchor=(0, 1.1), loc='upper left', ncol=2)

easypyplot.pdf.plot_teardown(pp)