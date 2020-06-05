import pandas # here we make a table more consistent


def isNaN(num):
    return num != num


def get_table():
    table = pandas.read_csv('new_kind_of_table.csv')
    return table


def school(table):
    for j in range(7879):
        school = table.loc[j, 'first_edu_school']

        if isNaN(school):
            school = ''
        elif school == '[]':
            school = ''
        elif 'Высшая школа экономики' in school:
            school = 'Высшая школа экономики'

        table.loc[j, 'first_edu_school'] = school
    return table


def highest_degree(table):
    for j in range(7879):
        degree = table.loc[j, 'highest_degree']

        if not isNaN(degree) and 'Кандидат' in degree:
            degree = 'Кандидат наук'
        elif not isNaN(degree) and 'Доктор' in degree:
            degree = 'Доктор наук'
        elif not isNaN(degree) and 'РАН' in degree:
            degree = 'Член РАН'
        elif not isNaN(degree):
            degree = degree.rstrip(' ')

        table.loc[j, 'highest_degree'] = degree
    return table


def hse_spec(table):
    for j in range(7879):
        spec = table.loc[j, 'hse_spec']

        if isNaN(spec):
            spec = ''
        elif spec == '[]':
            spec = ''
        else:
            spec = spec.lower().rstrip(' ')

        table.loc[j, 'hse_spec'] = spec
    return table


def main():
    table = get_table()
    table = school(table)
    table = highest_degree(table)
    table = hse_spec(table)
    table.to_csv('/home/valeria/PycharmProjects/freshman_pr/second_kind_of_table.csv')


if __name__ == '__main__':
    main()

# after that I manually added 'hse_fac' column which contains HSE faculties people have graduated from
# this is called third_kind_of_table.csv
