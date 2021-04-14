# %%
import numpy as np
import matplotlib.pyplot as plt
import easypyplot
import pandas as pd

# cache_flat_ratio
# prepare ordered workload list
cache_flat_ratio_csv = pd.read_csv('/scorpio/home/liyiwei/pom-research/plot-micro21/data-repo-micro21-baryon/3_sensitivity/cacheflatratio.csv')
low_wl = ['503', '508', '521', '523', '525', '526', '531', '544']
medium_wl = ['507', '510']
high_wl = ['502', '505', '519', '520', '549', '554', '557']
mix_wl = ['mix1', 'mix2', 'mix3', 'mix4']
cache_flat_ratio_2darr = []
hitrate_2darr = []
wl_list = []
for idx, workload in cache_flat_ratio_csv.tail(3).iterrows():
    wl_list.append(workload['Benchmark'])
    cache_flat_ratio_2darr.append([workload['Cache25% Flat75% Speedup_over_hybrid2'], workload['Cache50% Flat50% Speedup_over_hybrid2'], workload['Cache75% Flat25% Speedup_over_hybrid2']])
    hitrate_2darr.append([workload['Cache25% Flat75% Hitrate'], workload['Cache50% Flat50% Hitrate'], workload['Cache75% Flat25% Hitrate']])

group_name = ['Cache 25%', 'Cache 50%', 'Cache 75%']
fig_dims = (5, 2.5)
fig_name = '{}'.format("graph_cacheratio")
pp, fig = easypyplot.pdf.plot_setup(fig_name, fig_dims)
ax = fig.gca()
ax2 = ax.twinx()
easypyplot.format.turn_off_box(ax, twinx_axes=ax2)

# x ticks
group_xticks = []
all_xticks = []
xtick_beg = 0
color_item = [easypyplot.color.COLOR_SET[i] for i in [1, 5, 6]]
hdls = []
for idx, cache_flat_ratio in enumerate(cache_flat_ratio_2darr):
    group_xticks.append(xtick_beg)
    xticks = list(np.arange(xtick_beg, xtick_beg+len(cache_flat_ratio_2darr) * bar_width / 3, bar_width / 3) - bar_width / 3)
    all_xticks.append(xticks)
    xtick_beg += 1
    if idx == len(wl_list) - 4:
        xtick_beg += 0.5 # gap for geomean items

bar_width = 0.7
hdls = easypyplot.barchart.draw(ax, cache_flat_ratio_2darr, width=bar_width, breakdown=False, xticks=group_xticks, group_names=wl_list, colors=color_item)
ax.set_xticklabels([], fontsize=8)
ax.set_xlim([ax.get_xticks()[0] - 1, ax.get_xticks()[-1] + 1])
ax.xaxis.set_ticks_position('none')

# y axis
ax.yaxis.grid(True)
ax.set_ylabel('Normalized Speedup')
ax.set_ylim([0, 1.5])

# y text
tick_x_list = []
for group_id in range(len(cache_flat_ratio_2darr)):
    for entry_id in range(3):
        cache_flat_ratio = cache_flat_ratio_2darr[group_id][entry_id]
        x = ax.get_xticks()[group_id] + entry_id * bar_width / 3 - bar_width / 3
        tick_x_list.append(x)
        x += 0.03 # a little offset
        cache_flat_ratio_text = "%.03f" % cache_flat_ratio
        y_pos = min(cache_flat_ratio, 5)
        ax.text(x, y_pos, cache_flat_ratio_text, ha='center', va='top', fontsize=8, rotation=90)

plt.tight_layout()
easypyplot.format.resize_ax_box(ax, hratio=0.77)

# workload text
name_y_pos = -0.05
for idx, case in enumerate(wl_list):
    x = ax.get_xticks()[idx]
    ax.text(x, name_y_pos, case, ha='center', va='top', fontsize=9, rotation=90)

# hit rate plot
ax2.set_ylabel('Hit rate')
ax2.set_ylim([0.5, 1])
tick_x_2darr = np.reshape(all_xticks, (-1, 3))
print(tick_x_2darr)
print(hitrate_2darr)
for (group_x, group_y) in zip(tick_x_2darr, hitrate_2darr):
    ax2.plot(group_x, group_y, 'k', marker='^', markersize=7)
    
# Create legend
ax.legend(hdls, group_name, frameon=False, bbox_to_anchor=(0, 1.2), loc='upper left', ncol=3)

easypyplot.pdf.plot_teardown(pp)