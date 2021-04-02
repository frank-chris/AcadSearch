M = 5000

def get_file_index_and_prof_index(id):
    file_index = id%M
    prof_index = id//M
    return (file_index, prof_index)

def get_id(file_index, prof_index):
    return prof_index*M + file_index