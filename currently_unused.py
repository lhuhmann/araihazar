#%% compare binned data for subset vs all
fig, ax = plt.subplots(figsize=(8,6))
ax.set_ylabel(r'Urinary Arsenic ($\mu g/L$)', fontsize=18)
ax.set_xlabel(r'Primary Household Well Arsenic ($\mu g/L$)', fontsize=18)
ax.errorbar(all_binned_data['arsenic_ugl_mean'], all_binned_data['urine_as_mean'], 
            yerr=all_binned_data['urine_as_sem'], xerr=all_binned_data['arsenic_ugl_sem'],
            fmt='o', markersize=5, mfc='b', mec='none', ecolor='b', capsize=2)
ax.errorbar(subset_binned_data['arsenic_ugl_mean'], subset_binned_data['urine_as_mean'], 
            yerr=subset_binned_data['urine_as_sem'], xerr=subset_binned_data['arsenic_ugl_sem'],
            fmt='o', markersize=5, mfc='k', mec='none', ecolor='k', capsize=2)
# ax.set_xlim([0,xmax])
# ax.set_ylim([0,ymax])
ax.xaxis.set_ticks([0, 100, 200, 300, 400])
ax.yaxis.set_ticks([0, 100, 200, 300, 400])
ax.tick_params(axis='both', labelsize=16)
plt.savefig('plots/all_subset_comparison_binned.png')

# #%% add wells beyond family compound
# def three_slope_regress(data, group_name):
#     # need to add a column of ones to the x-data to get a constant term in the model
#     x = sm.add_constant(pd.concat([data.arsenic_ugl, data.other_as_50m, data.other_as_hyp_beyond_50], axis=1))

#     model = sm.OLS(data.urine_as, x)
#     results = model.fit()
#     print(results.summary())

#     urine_as_pred = results.params[1]*data.arsenic_ugl + \
#                     results.params[2]*data.other_as_50m + \
#                     results.params[2]*data.other_as_hyp_beyond_50 + \
#                     results.params[0]

#     fig, ax = plt.subplots(figsize=(8,6))
#     ax.plot(data.arsenic_ugl, data.urine_as)
#     ax.plot(data.arsenic_ugl, urine_as_pred, 'b-')
#     plt.savefig(group_name + '_three_slope_regression_primary_well.png')

#     fig, ax = plt.subplots(figsize=(8,6))
#     ax.plot(data.other_as_50m, data.urine_as, marker='o', s=5, c='k', alpha=.2, edgecolors='none')
#     ax.plot(data.other_as_50m, urine_as_pred, 'b-')
#     plt.savefig(group_name + '_three_slope_regression_compound_wells.png')

#     fig, ax = plt.subplots(figsize=(8,6))
#     ax.plot(data.other_as_hyp_beyond_50, data.urine_as, marker='o', s=5, c='k', alpha=.2, edgecolors='none')
#     ax.plot(data.other_as_hyp_beyond_50, urine_as_pred, 'b-')
#     plt.savefig(group_name + '_three_slope_regression_distant_wells.png')
