import numpy as np 
import pandas as pd
import json
import plotly.graph_objects as go

file_count = 10

data_files = [pd.read_csv('../data/professor_data-'+str(file_index)+'-cleaned.csv',header=None,encoding='utf8') for file_index in range(file_count) ]

with open('../data/topic_and_paper_index_full.json') as f:
    index_dict = json.load(f)

def make_list(initial_string):
    return initial_string.lstrip('[\'').rstrip('\']').split('\', \'')

def compute_and_plot_statistics():
    data_df = pd.concat(data_files)
    stats = dict()
    stats['total_prof_count'] = data_df[1].size
    stats['unique_affiliation_count'] = data_df[3].nunique()
    stats['total_affiliation_count'] = data_df[3].count()
    stats['total_verified_count'] = data_df[4].count()
    stats['total_homepage_count'] = data_df[5].count()
    stats['unique_paper_count'] = (data_df[16].apply(make_list)).apply(pd.Series).stack().reset_index(drop=True).nunique()
    stats['total_paper_count'] = ((data_df[16].apply(make_list)).apply(len)).sum()
    stats['cit_mean'] = round(data_df[7].mean(), 2)
    stats['h_ind_mean'] = round(data_df[8].mean(), 2)
    stats['i_ind_mean'] = round(data_df[9].mean(), 2)
    stats['cit_median'] = int(data_df[7].median())
    stats['h_ind_median'] = int(data_df[8].median())
    stats['i_ind_median'] = int(data_df[9].median())
    stats['cit_5_mean'] = round(data_df[10].mean(), 2)
    stats['h_ind_5_mean'] = round(data_df[11].mean(), 2)
    stats['i_ind_5_mean'] = round(data_df[12].mean(), 2)
    stats['cit_5_median'] = int(data_df[10].median())
    stats['h_ind_5_median'] = int(data_df[11].median())
    stats['i_ind_5_median'] = int(data_df[12].median())

    word_frequencies = []
    for value in index_dict.values():
        word_frequencies.append(len(value))

    # frequency distribution histogram
    fig = go.Figure(data=[go.Histogram(x=word_frequencies)])
    fig.update_layout(title_text='No. of words with frequency k as a function of k', xaxis_title='k', yaxis_title='no. of words with frequency k')
    fig.show()

    # pie chart 1
    labels = ['Affiliation provided', 'Affiliation not provided']
    values = [stats['total_affiliation_count'], stats['total_prof_count']-stats['total_affiliation_count']]
    fig = go.Figure(data=[go.Pie(labels=labels, textinfo='value+percent', values=values, hole=.3)])
    fig.update_layout(title_text='Percentage of professors who provided affiliation')
    fig.show()

    # pie chart 2
    labels = ['Email verified', 'Email not verified']
    values = [stats['total_verified_count'], stats['total_prof_count']-stats['total_verified_count']]
    fig = go.Figure(data=[go.Pie(labels=labels, textinfo='value+percent', values=values, hole=.3)])
    fig.update_layout(title_text='Percentage of professors with email verified accounts')
    fig.show()

    # pie chart 3
    labels = ['Homepage provided', 'Homepage not provided']
    values = [stats['total_homepage_count'], stats['total_prof_count']-stats['total_homepage_count']]
    fig = go.Figure(data=[go.Pie(labels=labels, textinfo='value+percent', values=values, hole=.3)])
    fig.update_layout(title_text='Percentage of professors who provided homepage')
    fig.show()

    # bar chart 1
    statistic = ['mean', 'median']
    y_1 = [stats['cit_mean'], stats['cit_median']]
    y_2 = [stats['cit_5_mean'], stats['cit_5_median']]
    fig = go.Figure(data=
            [go.Bar(name='Overall', x=statistic, y=y_1, text=y_1, textposition='auto'),
            go.Bar(name='Last 5 years', x=statistic, y=y_2, text=y_2, textposition='auto')
            ])
    fig.update_layout(title_text='No. of citations', barmode='group')
    fig.show()

    # bar chart 2
    y_1 = [stats['h_ind_mean'], stats['h_ind_median']]
    y_2 = [stats['h_ind_5_mean'], stats['h_ind_5_median']]
    fig = go.Figure(data=
            [go.Bar(name='Overall', x=statistic, y=y_1, text=y_1, textposition='auto'),
            go.Bar(name='Last 5 years', x=statistic, y=y_2, text=y_2, textposition='auto')
            ])
    fig.update_layout(title_text='h-index', barmode='group')
    fig.show()

    # bar chart 3
    y_1 = [stats['i_ind_mean'], stats['i_ind_median']]
    y_2 = [stats['i_ind_5_mean'], stats['i_ind_5_median']]
    fig = go.Figure(data=
            [go.Bar(name='Overall', x=statistic, y=y_1, text=y_1, textposition='auto'),
            go.Bar(name='Last 5 years', x=statistic, y=y_2, text=y_2, textposition='auto')
            ])
    fig.update_layout(title_text='i10-index', barmode='group')
    fig.show()

    return stats
    
stats = compute_and_plot_statistics()
for key, value in stats.items():
    print(key, ':', value)

