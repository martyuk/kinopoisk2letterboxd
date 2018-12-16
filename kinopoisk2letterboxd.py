import pandas as pd
import html

k_import_filename = ""
k_import = open(k_import_filename, "r", encoding='Windows-1251')
log = open("kinopoisk_log.txt", "w")

#Get rid of first intro part
for i in range(33):
	line = k_import.readline()

'''
0 - Title
1 - Year
2 - WatchedDate
3 - Rating10
'''
movie_list = []
movie_list.append(['Title', 'Year', 'WatchedDate', 'Rating10'])
line_number = 0
Title_flag = 0
Year_flag = 0
WatchedDate_flag = 0
Rating10_flag = 0

for line in k_import:

    line_number += 1
    movie_number = line_number//24 + 1

    #Title
    if (line_number%24)%4 == 0 and (line_number%24 != 0) and Title_flag < movie_number:
        Title_flag += 1
        
        #Is title in english or in russian?
        if line[32:-6]:
            movie_list.append([html.unescape(line[32:-6]),'','', ''])
        else:
            movie_list.append([html.unescape(previous_line[35:-10]),'','', ''])
    #Year
    elif (line_number%24)%5 == 0 and (line_number%24 != 0) and Year_flag < movie_number:
        Year_flag += 1
        movie_list[movie_number][1] = line[25:-6]
    #WatchedDate
    elif (line_number%24)%23 == 0 and (line_number%24 != 0) and WatchedDate_flag < movie_number:
        WatchedDate_flag += 1
        movie_list[movie_number][2] = line[47:51]+'-'+line[44:46]+'-'+line[41:43]
    #Rating10
    elif (line_number%24)%11 == 0 and (line_number%24 != 0) and Rating10_flag < movie_number:
        Rating10_flag += 1
        movie_list[movie_number][3] = line[32:-6]

    #If there's only russian title
    previous_line = line

del movie_list[-1]
movie_df = pd.DataFrame(movie_list)

movie_df.to_csv('k_export.csv', index=False, header=False)

k_import.close()
log.close()