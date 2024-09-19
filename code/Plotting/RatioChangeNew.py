import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Pre Data
pre_groups = ['Combinded 3-Day Unenriched', 'Combined 6-Day Enriched', 'Combined 6-Day Unenriched', 'Ortho 6-Day Unenriched', 'Ortho 6-Day Enriched']
pre_paired_avg = [
    [10.25, 33.47, 37.72],
    [20.75, 17.76, 13.12, 15.08, 27.13],
    [24.95, 20.41, 26.58, 7.8, 14.2],
    [25.73, 33.56, 28.31, 30.88],
    [35.81, 29.17, 21.33, 39.2]
]
pre_unpaired_avg = [
    [17.83, 27.95, 9.15],
    [30.21, 29.57, 31.64, 31.24, 31.9],
    [27.79, 43.45, 43.08, 8.18, 9.46],
    [39.36, 27.69, 30.92, 24.25],
    [39.95, 33.11, 29.27, 37.05]
]

# Post Data
post_groups = ['Combined 3-Day Unenriched', 'Combined 6-Day Enriched', 'Combined 6-Day Unenriched', 'Ortho 6-Day Unenriched', 'Ortho 6-Day Enriched']
post_paired_avg = [
    [19.95, 33.42, 39.81],
    [32.88, 26.18, 25.23, 36.88, 32.12],
    [31.15, 25.35, 30.81, 32.12, 37.14],
    [38.43, 39.95, 34.89, 36.64],
    [40.8, 28.06, 26.38, 34.76]
]
post_unpaired_avg = [
    [26.75, 31.29, 27.38],
    [11.14, 22.79, 6.35, 28.56, 9.08],
    [23.41, 23.65, 30.13, 22.69, 21.14],
    [36.16, 37.81, 35.07, 35.60],
    [39.45, 32.94, 29, 32.06]
]

# Calculate mean of each group in post and pre datasets for paired and unpaired separately
post_paired_means = [np.mean(data) for data in post_paired_avg]
pre_paired_means = [np.mean(data) for data in pre_paired_avg]

post_unpaired_means = [np.mean(data) for data in post_unpaired_avg]
pre_unpaired_means = [np.mean(data) for data in pre_unpaired_avg]

# Calculate ratio of change for paired and unpaired separately
paired_ratio_of_change = [post_paired_means[i] / pre_paired_means[i] for i in range(len(post_paired_means))]
unpaired_ratio_of_change = [post_unpaired_means[i] / pre_unpaired_means[i] for i in range(len(post_unpaired_means))]

# Perform t-tests for significance
paired_p_values = [stats.ttest_rel(post_paired_avg[i], pre_paired_avg[i]).pvalue for i in range(len(post_paired_avg))]
unpaired_p_values = [stats.ttest_ind(post_unpaired_avg[i], pre_unpaired_avg[i]).pvalue for i in range(len(post_unpaired_avg))]

# Significance level
alpha = 0.05

fig, ax = plt.subplots(figsize=(10, 6), dpi=600) 

# Define colors
paired_color = '#888888'  # Gray for paired data
unpaired_color = '#CCCCCC'  # Light gray for unpaired data
significant_color = 'black'  # Black for significant bars

# Bar width
bar_width = 0.35

# X positions for the bars
x = np.arange(len(post_groups))

# Plotting paired data
ax.bar(x - bar_width/2, paired_ratio_of_change, bar_width, label='Paired', color=paired_color)

# Plotting unpaired data
ax.bar(x + bar_width/2, unpaired_ratio_of_change, bar_width, label='Unpaired', color=unpaired_color)

# Adding asterisks and printing p-values for significance
for i, p_value in enumerate(paired_p_values):
    if p_value < alpha:
        ax.text(x[i] - bar_width/2, paired_ratio_of_change[i] + 0.02, f'* p={p_value:.4f}', ha='center', va='bottom', color=significant_color)

for i, p_value in enumerate(unpaired_p_values):
    if p_value < alpha:
        ax.text(x[i] + bar_width/2, unpaired_ratio_of_change[i] + 0.02, f'* p={p_value:.4f}', ha='center', va='bottom', color=significant_color)

ax.set_xlabel('Group')
ax.set_ylabel('Ratio of Change (Post Mean Licks / Pre Mean Licks)')
ax.set_title('Ratio of Change of Each Solution from Pre to Post Training')
ax.set_xticks(x)
ax.set_xticklabels(post_groups)
ax.legend()

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
