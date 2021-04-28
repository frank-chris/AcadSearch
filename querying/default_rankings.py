def default_ranking_metric(data_for_a_prof):
    h_ind = data_for_a_prof['h_ind']
    i_ind = data_for_a_prof['i_ind']
    h_ind5 = data_for_a_prof['h_ind5']
    i_ind5 = data_for_a_prof['i_ind5']
    cit = data_for_a_prof['cit']
    cit5 = data_for_a_prof['cit5']

    # these parameters can be made learnable for each user using machine learning
    parameters = [0.0875,0.0875,0.025,0.35,0.35,0.10]
    values = [h_ind, i_ind, cit, h_ind5, i_ind5, cit5]

    score = 0.0

    for i in range(len(values)):
        fraction = parameters[i]
        value = values[i]
        score+=fraction*value
    return score