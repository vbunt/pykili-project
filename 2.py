import pandas, re


def get_table():
    table = pandas.read_csv('big_table1.csv')
    return table


def isNaN(num): # sometimes theres nan which is not None but we still can't work with it, so we often check if what we are working with is nan
    return num != num


def get_started_worked(table): # this is where we do things with a column 'started_worked'

    table[['started', 'worked']] = table.started_worked.str.split("&", expand=True)
    table = table.drop(columns=['started_worked'])

    table[['gender', 'start_year']] = table.started.str.split("работать в НИУ ВШЭ в ", expand=True)
    table = table.drop(columns=['started'])

    for i in range(7879): # get a gender depending on the 'started' column where possible
        if table.loc[i, 'gender'] == 'Начала ':
            table.loc[i, 'gender'] = 'F'
        elif table.loc[i, 'gender'] == 'Начал ':
            table.loc[i, 'gender'] = 'M'

    for i in range(7879): # get a start year
        year = ''

        if not isNaN(table.loc[i, 'start_year']):
            year = re.findall('\d{4}', table.loc[i, 'start_year'])

        if year:
            table.loc[i, 'start_year'] = year[0] # get the only year from the list
        else:
            table.loc[i, 'start_year'] = year # year = ''

    for j in range(7879): # get length of service
        time = table.loc[j, 'worked']

        if time and not isNaN(time):

            time = re.findall('(?:\d+ \w+ *)+', time)[0].split() # find number + years/months

            if time[-1][:3] == 'мес': # they write 'n months' or '1 year n months' but never 'n years m months'
                time = ['1'] # so i just rounded every number where 'month' occurs to 1 year

            time = time[0] # get the only number from the list
            table.loc[j, 'worked'] = time

    return table


def get_education(table): # this is where  we do things with 'education' column
    for j in range(7879): # for every person in the table
        edu = {} # {'year': ['degree', 'alma-mater']
        age, first_edu_year, first_edu_degree, first_edu_school, last_edu_year, highest_degree = '', '', '', '', '', '' # interesting things
        raw = table.loc[j, 'education'] # everything about this person's education

        if not isNaN(raw):

            line = raw.split('&')[1:]  # everything about this person's education but now a list

            for i in range(len(line)):

                if i % 2 == 0 and line[i].isnumeric(): # we check that el is a year, after year they always have the degree and institution

                    good_stuff = line[i + 1]
                    degree = re.search('(Ученое звание: [А-Яа-я]+)|(?:[\w\- ]+)', good_stuff).group() # find a degree they graduated with

                    alma_mater = re.findall(': ([^,]+),', good_stuff) # find an institution they graduated from
                    if alma_mater:
                        alma_mater = alma_mater[0] # get the only alma-mater from list

                    edu[line[i]] = [degree, alma_mater]

            if edu: # get interesting stiff
                first_edu_year = sorted(edu.keys())[0]
                first_edu_degree = edu[first_edu_year][0]
                first_edu_school = edu[first_edu_year][1]
                last_edu_year = sorted(edu.keys())[-1]
                highest_degree = edu[last_edu_year][0]

                if first_edu_degree == 'Бакалавриат': # this is how we count their age
                    age = 2020 - int(first_edu_year) + 22
                elif first_edu_degree == 'Специалитет':
                    age = 2020 - int(first_edu_year) + 23

        table.loc[j, 'age'] = age # get interesting stuff into the table
        table.loc[j, 'first_edu_year'] = first_edu_year
        table.loc[j, 'first_edu_degree'] = first_edu_degree
        table.loc[j, 'first_edu_school'] = first_edu_school
        table.loc[j, 'highest_degree'] = highest_degree

    table = table.drop(columns=['education'])

    return table


def get_places(table): # this is where we do things with 'place' column

    big_dict = {'name': [], 'position': [], 'faculty': [], 'departament': [], 'kafedra': []}

    for j in range(7879):

        places = {}  # {who: [where]}
        raw = table.loc[j, 'place'] # get places where the person works
        name = table.loc[j, 'name']
        indexes = [] # indexes of 'positions' ('professor:', 'headmaster:', etc) in 'line' list

        if not isNaN(raw):

            line = raw.split('&') # places but in a list

            for i in range(len(line)): # find where in list positions are mentioned ('professor:', 'headmaster:', etc)
                if re.findall('^[^:]+:$', line[i]):
                    indexes.append(i)

            indexes.append(len(line)) # here we append the last possible index so the next peace of code works better

            if len(indexes) > 1: # i think this line is useless but im scared of deleting it
                for k in range(len(indexes) - 1): # witchcraft # here we go through every 'position' we found
                    new_line = line[indexes[k]].split(', ') # this is for cases like 'professor, headmaster:': i split them in two separate 'positions' with the same 'place'
                    for el in new_line: # fill up 'places' dict with 'position' ('professor') and 'place' ('faculty of computer science')
                        places[el] = line[indexes[k] + 1:indexes[k + 1]] # 'place' is everything in between two 'positions' in 'line' list

            for place in places.keys(): # here place actually means 'position'
                # fill dict with info about one position: this position, person, faculty, department, ~kafedra

                big_dict['name'].append(name)
                big_dict['position'].append(place.lower().rstrip(':'))

                if len(places[place]) == 1: # in most cases the actual place consists of faculty, department, cafedra (in this order)
                    big_dict['faculty'].append(places[place][0]) # sometimes only faculty is mentioned
                    big_dict['departament'].append('')
                    big_dict['kafedra'].append('')
                elif len(places[place]) == 3: # sometimes ~kafedra is not mentioned
                    big_dict['faculty'].append(places[place][0])
                    big_dict['departament'].append(places[place][2])
                    big_dict['kafedra'].append('')
                else:
                    big_dict['faculty'].append(places[place][0])
                    big_dict['departament'].append(places[place][2])
                    big_dict['kafedra'].append(places[place][4])
                #there are cases that do not have this structure but i chose to ignore them
                #they do not affect the end result too much

    places_table = pandas.DataFrame(big_dict) # put everything into the other table
    table = table.drop(columns=['place'])
    return places_table, table


def main():
    table = get_table()
    table = get_started_worked(table)
    table = get_education(table)
    places_table, table = get_places(table)
    table.to_csv('/home/valeria/PycharmProjects/freshman_pr/kind_of_table.csv')
    places_table.to_csv('/home/valeria/PycharmProjects/freshman_pr/kind_of_places_table.csv')


if __name__ == '__main__':
    main()
