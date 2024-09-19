import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pingouin as pg

# Pre Data
pre_groups = ['Combined 3-Day Unenriched', 'Combined 6-Day Enriched', 'Combined 6-Day Unenriched', 'Ortho 6-Day Unenriched', 'Ortho 6-Day Enriched','Retro 6-Day Unenriched', 'Retro 6-Day Enriched']
pre_paired_avg = [
    [10.25, 33.47, 37.72],
    [20.75, 17.76, 13.12, 15.08, 27.13],
    [24.95, 20.41, 26.58, 7.8, 14.2],
    [25.73, 33.56, 28.31, 30.88],
    [35.81, 29.17, 21.33, 39.2],
    [41.63, 18.50, 32.94, 25.30],
    [23.00, 18.16, 21.66, 21.33]
]
pre_unpaired_avg = [
    [17.83, 27.95, 9.15],
    [30.21, 29.57, 31.64, 31.24, 31.9],
    [27.79, 43.45, 43.08, 8.18, 9.46],
    [39.36, 27.69, 30.92, 24.25],
    [39.95, 33.11, 29.27, 37.05],
    [29.45, 29.87, 30.36, 27.3]
    [28.47, 13.33, 14.80, 25.70]
]

# Post Data
post_groups = ['Combined 3-Day Unenriched', 'Combined 6-Day Enriched', 'Combined 6-Day Unenriched', 'Ortho 6-Day Unenriched', 'Ortho 6-Day Enriched', 'Retro 6-Day Unenriched', 'Retro 6-Day Enriched']
post_paired_avg = [
    [19.95, 33.42, 39.81],
    [32.88, 26.18, 25.23, 36.88, 32.12],
    [31.15, 25.35, 30.81, 32.12, 37.14],
    [38.43, 39.95, 34.89, 36.64],
    [40.8, 28.06, 26.38, 34.76],
    [26.13, 30.75, 28.27,22.33],
    [28.80, 18.16, 25.05, 31.40]
    
]
post_unpaired_avg = [
    [26.75, 31.29, 27.38],
    [11.14, 22.79, 6.35, 28.56, 9.08],
    [23.41, 23.65, 30.13, 22.69, 21.14],
    [36.16, 37.81, 35.07, 35.60],
    [39.45, 32.94, 29, 32.06],
    [33.90, 30.44, 29.91, 21.11],
    [38.2, 13.33, 28.58, 19.50]
]

# Calculate standard deviations
pre_paired_std = [np.std(data) for data in pre_paired_avg]
pre_unpaired_std = [np.std(data) for data in pre_unpaired_avg]

post_paired_std = [np.std(data) for data in post_paired_avg]
post_unpaired_std = [np.std(data) for data in post_unpaired_avg]

# Grayscale color palette
gray_color = "#808080"  # Gray color
grayish_color = "#CCCCCC"

# Plotting Pre Data
fig, ax1 = plt.subplots(1, 2, figsize=(12, 6), dpi=100, sharey=True)  # Set DPI for high resolution

# Plotting paired averages (Pre)
for i, group in enumerate(pre_groups):
    ax1[0].bar(i - 0.2, np.mean(pre_paired_avg[i]), yerr=pre_paired_std[i], capsize=5, width=0.4, label=f'{group}', color=gray_color)

# Plotting unpaired averages (Pre)
for i, group in enumerate(pre_groups):
    ax1[0].bar(i + 0.2, np.mean(pre_unpaired_avg[i]), yerr=pre_unpaired_std[i], capsize=5, width=0.4, color=grayish_color)

# Plotting connecting lines between paired and unpaired averages (Pre)
for i in range(len(pre_groups)):
    for j in range(min(len(pre_paired_avg[i]), len(pre_unpaired_avg[i]))):
        ax1[0].plot([i - 0.2, i + 0.2], [pre_paired_avg[i][j], pre_unpaired_avg[i][j]], color= 'black', linestyle='-', linewidth=1)

# Plotting individual data points (Pre)
for i, group in enumerate(pre_groups):
    for j in range(len(pre_paired_avg[i])):
        ax1[0].scatter([i - 0.2], pre_paired_avg[i][j], color='black', zorder=5)
    for j in range(len(pre_unpaired_avg[i])):
        ax1[0].scatter([i + 0.2], pre_unpaired_avg[i][j], color='black', zorder=5)

ax1[0].set_xticks(range(len(pre_groups)))
ax1[0].set_xticklabels(pre_groups, rotation=45, ha='right')  # Rotate labels
ax1[0].set_ylabel('Average Licks')
ax1[0].set_title('Average Licks to Paired vs. Unpaired Odors Pre Test')

# Plotting Post Data
# Plotting paired averages (Post)
for i, group in enumerate(post_groups):
    ax1[1].bar(i - 0.2, np.mean(post_paired_avg[i]), yerr=post_paired_std[i], capsize=5, width=0.4, label=f'{group}', color=gray_color)

# Plotting unpaired averages (Post)
for i, group in enumerate(post_groups):
    ax1[1].bar(i + 0.2, np.mean(post_unpaired_avg[i]), yerr=post_unpaired_std[i], capsize=5, width=0.4, color=grayish_color)

# Plotting connecting lines between paired and unpaired averages (Post)
for i in range(len(post_groups)):
    for j in range(min(len(post_paired_avg[i]), len(post_unpaired_avg[i]))):
        ax1[1].plot([i - 0.2, i + 0.2], [post_paired_avg[i][j], post_unpaired_avg[i][j]], color='black', linestyle='-', linewidth=1)

# Plotting individual data points (Post)
for i, group in enumerate(post_groups):
    for j in range(len(post_paired_avg[i])):
        ax1[1].scatter([i - 0.2], post_paired_avg[i][j], color='black', zorder=5)
    for j in range(len(post_unpaired_avg[i])):
        ax1[1].scatter([i + 0.2], post_unpaired_avg[i][j], color='black', zorder=5)

ax1[1].set_xticks(range(len(post_groups)))
ax1[1].set_xticklabels(post_groups, rotation=45, ha='right')  # Rotate labels
ax1[1].set_title('Average Licks to Paired vs. Unpaired Odors Post Test')

# Add legend with custom handles
paired_patch = mpatches.Patch(color=gray_color, label='Paired')
unpaired_patch = mpatches.Patch(color=grayish_color, label='Unpaired')
fig.legend(handles=[paired_patch, unpaired_patch], loc='lower right')

plt.tight_layout()
plt.show()

