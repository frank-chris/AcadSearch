def default_ranking_metric(data_for_a_prof):
    '''
    We have created a ranking metric that depends on the h-index, i-index and citations of a professor.

    Input:
    > data_for_a_prof - contains all the necessary data of a professor for creating the metric.

    Output:
    > score - a floating point number that is the score of the professor.
    '''
    h_ind = data_for_a_prof['h_ind']
    i_ind = data_for_a_prof['i_ind']
    h_ind5 = data_for_a_prof['h_ind5']
    i_ind5 = data_for_a_prof['i_ind5']
    cit = data_for_a_prof['cit']
    cit5 = data_for_a_prof['cit5']

    # We give 4 times more weightage to data that has been obtained in the last five years.
    parameters = [0.0875,0.0875,0.025,0.35,0.35,0.10]
    values = [h_ind, i_ind, cit, h_ind5, i_ind5, cit5]
    # these parameters can be made learnable for each user using machine learning.

    score = 0.0

    for i in range(len(values)):
        fraction = parameters[i]
        value = values[i]
        score += (fraction * value)

    return score
