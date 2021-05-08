import numpy as np 
import pandas as pd
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# number of cleaned files
file_count = 10

# read the cleaned csv files 
data_files = [pd.read_csv('../data/professor_data-'+str(file_index)+'-cleaned.csv',header=None,encoding='utf8') for file_index in range(file_count) ]

# load topic_and_paper inverted_index
with open('../data/topic_and_paper_index_full.json') as f:
    index_dict = json.load(f)

def make_list(initial_string):
    '''
    Function to convert str(list) to list

    Input:
    > initial_string - a list type-casted as str

    Output:
    > list of items from the str-type-casted list
    '''
    return initial_string.lstrip('[\'').rstrip('\']').split('\', \'')

def compute_and_plot_statistics():
    '''
    Function to compute and plot several statistics of the cleaned data

    Input:
    > None

    Output:
    > dictionary containing statistics about the cleaned data
    '''

    # combine all csv files
    data_df = pd.concat(data_files)
    # dictionary to store statistics
    stats = dict()

    # total number of professors
    stats['total_prof_count'] = data_df[1].size

    # number of unique affiliations/institutes
    stats['unique_affiliation_count'] = data_df[3].nunique()

    # total number of professors who provided affiliation
    stats['total_affiliation_count'] = data_df[3].count()

    # total number of professors with verified email
    stats['total_verified_count'] = data_df[4].count()

    # total number of professors who provided homepage
    stats['total_homepage_count'] = data_df[5].count()

    # number of unique papers in dataset
    stats['unique_paper_count'] = (data_df[16].apply(make_list)).apply(pd.Series).stack().reset_index(drop=True).nunique()
    
    # sum of number of papers of all professors in dataset
    stats['total_paper_count'] = ((data_df[16].apply(make_list)).apply(len)).sum()
    
    # mean number of citations overall
    stats['cit_mean'] = round(data_df[7].mean(), 2)

    # mean h-index overall
    stats['h_ind_mean'] = round(data_df[8].mean(), 2)
    
    # mean i10-index overall
    stats['i_ind_mean'] = round(data_df[9].mean(), 2)
    
    # median number of citations overall
    stats['cit_median'] = int(data_df[7].median())
    
    # median h-index overall
    stats['h_ind_median'] = int(data_df[8].median())
    
    # median i10-index overall
    stats['i_ind_median'] = int(data_df[9].median())
    
    # mean number of citations - last 5 years
    stats['cit_5_mean'] = round(data_df[10].mean(), 2)
    
    # mean h-index - last 5 years
    stats['h_ind_5_mean'] = round(data_df[11].mean(), 2)
    
    # mean i10-index - last 5 years
    stats['i_ind_5_mean'] = round(data_df[12].mean(), 2)
    
    # median number of citations - last 5 years
    stats['cit_5_median'] = int(data_df[10].median())

    # median h-index - last 5 years
    stats['h_ind_5_median'] = int(data_df[11].median())

    # median i10-index - last 5 years
    stats['i_ind_5_median'] = int(data_df[12].median())

    # frequency of each word
    word_frequencies = []
    for value in index_dict.values():
        word_frequencies.append(len(value))

    colors = ['#394fe1', '#010038']
    # frequency distribution histogram - no. of words with frequency k vs k
    fig = go.Figure(data=[go.Histogram(x=word_frequencies, marker_color=colors[0])])
    fig.update_layout(title_text='No. of words with frequency k as a function of k', xaxis_title='k', yaxis_title='no. of words with frequency k')
    fig.show()

    # pie charts
    fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]], 
                        subplot_titles=['Affiliation provided?', 'Email verified?', 'Homepage provided?'])
    labels = ['Yes', 'No']
    # pie 1
    values = [stats['total_affiliation_count'], stats['total_prof_count']-stats['total_affiliation_count']]
    fig.add_trace(go.Pie(labels=labels, textinfo='value+percent', values=values, hole=.3, marker_colors=colors, name='Affiliation provided?'), 1, 1)
    # pie 2
    values = [stats['total_verified_count'], stats['total_prof_count']-stats['total_verified_count']]
    fig.add_trace(go.Pie(labels=labels, textinfo='value+percent', values=values, hole=.3, marker_colors=colors, name='Email verified?'), 1, 2)
    # pie 3
    values = [stats['total_homepage_count'], stats['total_prof_count']-stats['total_homepage_count']]
    fig.add_trace(go.Pie(labels=labels, textinfo='value+percent', values=values, hole=.3, marker_colors=colors, name='Homepage provided?'), 1, 3)
    fig.show()

    # bar chart 1
    statistic = ['mean', 'median']
    y_1 = [stats['cit_mean'], stats['cit_median']]
    y_2 = [stats['cit_5_mean'], stats['cit_5_median']]
    fig = go.Figure(data=
            [go.Bar(name='Overall', x=statistic, y=y_1, text=y_1, textposition='auto', marker_color=colors[0]),
            go.Bar(name='Last 5 years', x=statistic, y=y_2, text=y_2, textposition='auto', marker_color=colors[1])
            ])
    fig.update_layout(title_text='No. of citations', barmode='group')
    fig.show()

    # bar chart 2
    y_1 = [stats['h_ind_mean'], stats['h_ind_median']]
    y_2 = [stats['h_ind_5_mean'], stats['h_ind_5_median']]
    fig = go.Figure(data=
            [go.Bar(name='Overall', x=statistic, y=y_1, text=y_1, textposition='auto', marker_color=colors[0]),
            go.Bar(name='Last 5 years', x=statistic, y=y_2, text=y_2, textposition='auto', marker_color=colors[1])
            ])
    fig.update_layout(title_text='h-index', barmode='group')
    fig.show()

    # bar chart 3
    y_1 = [stats['i_ind_mean'], stats['i_ind_median']]
    y_2 = [stats['i_ind_5_mean'], stats['i_ind_5_median']]
    fig = go.Figure(data=
            [go.Bar(name='Overall', x=statistic, y=y_1, text=y_1, textposition='auto', marker_color=colors[0]),
            go.Bar(name='Last 5 years', x=statistic, y=y_2, text=y_2, textposition='auto', marker_color=colors[1])
            ])
    fig.update_layout(title_text='i10-index', barmode='group')
    fig.show()

    return stats
    
stats = compute_and_plot_statistics()
# print computed statistics
for key, value in stats.items():
    print(key, ':', value)

