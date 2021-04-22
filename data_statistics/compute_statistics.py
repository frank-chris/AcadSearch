import numpy as np 
import pandas as pd 
import sys

file_count = 10

data_files = [pd.read_csv('../cleaning/professor_data-'+str(file_index)+'-cleaned.csv',header=None,encoding='utf8') for file_index in range(file_count) ]

def make_list(initial_string):
    return initial_string.lstrip('[\'').rstrip('\']').split('\', \'')

def compute_and_plot_statistics():
    data_df = pd.concat(data_files)
    stats = dict()
    stats['total_prof_count'] = data_df[1].count()
    stats['unique_affiliation_count'] = data_df[3].nunique()
    stats['total_affiliation_count'] = data_df[3].count()
    stats['total_verified_count'] = data_df[4].count()
    stats['total_homepage_count'] = data_df[5].count()
    stats['unique_paper_count'] = (data_df[16].apply(make_list)).apply(pd.Series).stack().reset_index(drop=True).nunique()
    stats['total_paper_count'] = ((data_df[16].apply(make_list)).apply(len)).sum()
    stats['cit_mean'] = data_df[7].mean()
    stats['h_ind_mean'] = data_df[8].mean()
    stats['i_ind_mean'] = data_df[9].mean()
    stats['cit_median'] = data_df[7].median()
    stats['h_ind_median'] = data_df[8].median()
    stats['i_ind_median'] = data_df[9].median()
    stats['cit_5_mean'] = data_df[10].mean()
    stats['h_ind_5_mean'] = data_df[11].mean()
    stats['i_ind_5_mean'] = data_df[12].mean()
    stats['cit_5_median'] = data_df[10].median()
    stats['h_ind_5_median'] = data_df[11].median()
    stats['i_ind_5_median'] = data_df[12].median()

    return stats
    
stats = compute_and_plot_statistics()
for key, value in stats.items():
    print(key, ':', value)

