import csv

file_count = 10
output_file = open('professor_data_combined.csv', 'w+',newline ='',encoding="utf8")

for i in range(file_count):
    input_file = open('professor_data-'+str(i)+'.csv','r',encoding="utf8",errors="ignore")
    for line in input_file:        
        output_file.write(line)        
