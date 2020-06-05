import pandas
from collections import Counter
import matplotlib.pyplot as plt


def isNaN(num):
    return num != num


def reading():
    table = pandas.read_csv('third_table.csv')
    return table


def reading_pl():
    pl_table = pandas.read_csv('places_table.csv')
    return pl_table


def top(table, min, column, q=True):
    everyone_else = 0
    top = []
    cnt = Counter(table[column])

    for el in cnt.keys():
        if q:
            if cnt[el] > min and not isNaN(el) and el:
                top.append((el, cnt[el]))
            else:
                everyone_else += cnt[el]
        else:
            if not isNaN(el):
                if cnt[el] > min:
                    top.append((el, cnt[el]))
                else:
                    everyone_else += cnt[el]

    top.append(('другое', everyone_else))
    return top


def do_plot(top, title, explode=False):
    labels = [i[0] for i in top]
    sizes = [i[1] for i in top]

    fig1, ax1 = plt.subplots()

    if explode:
        ax1.pie(sizes, labels=labels, labeldistance=1.2, autopct='%1.1f%%', explode=explode)
    else:
        ax1.pie(sizes, labels=labels, labeldistance=1.2, autopct='%1.1f%%')

    fig1.suptitle(title, fontsize = 14, ha='left')

    plt.show()


def lazy_statistics(table):
    number_of_all = len([el for el in table.gender])
    number_of_women = len([el for el in table.gender if el == 'F'])
    number_of_men = len([el for el in table.gender if el == 'M'])
    print('Всего людей: ', number_of_all)
    print('Из них женщин: ', number_of_women, ' (', round(number_of_women/number_of_all*100), '%)')
    print('Из них мужчин: ', number_of_men, ' (', 100-round(number_of_women/number_of_all*100), '%)')
    av_worked = int(table.worked.mean())
    mean_age = int(table.age.mean())
    median_started = int(table.start_year.median())
    print('Средний стаж: ', av_worked, 'лет')
    print('Средний возраст: ', mean_age, 'лет')
    print('Медианный год начала работы в НИУ ВШЭ: ', median_started)


def lazy_statistics_pl(table_pl):
    print('\nСамый большой факультет -', Counter(table_pl.faculty).most_common(1)[0][0], '. Там работают', Counter(table_pl.faculty).most_common(1)[0][1], 'человек.')
    print('Самая большой департамент -', Counter(table_pl.departament).most_common(2)[1][0], '. Там работают', Counter(table_pl.faculty).most_common(2)[1][1], 'человек.')


def incredible_thing(table, table_pl):
    new_table = table.merge(table_pl)
    moves_list = []
    for j in range(len(new_table)):
        hse_dep = new_table.loc[j, 'hse_dep']  # attended
        faculty = new_table.loc[j, 'faculty']  # works
        if not isNaN(hse_dep) and not isNaN(faculty):
            moves_list.append((hse_dep, faculty))
    moves_dict = {}
    moves_cnt = Counter(moves_list).most_common()
    print('\nСамые/ популярные переходы между факультетами/институтами')
    for el in moves_cnt[:30]:

        where_from = el[0][0].lower()
        where_to = el[0][1].lower()
        number = el[1]
        if where_from == 'факультет бизнеса и менеджмента' and where_to == 'факультет бизнеса и менеджмента':
            continue
        elif where_from == 'миэм' and where_to == 'московский институт электроники и математики им. а.н. тихонова':
            continue
        elif where_to != where_from:
            print('-', where_from, '->', where_to, '(', number, 'человек)')

    for el in moves_cnt:
        where_from = el[0][0].lower()
        where_to = el[0][1].lower()
        number = int(el[1])

        if not where_from in moves_dict.keys():
            moves_dict[where_from] = {'другое': 0}

        if number < 7:
            where_to = 'другое'
            moves_dict[where_from][where_to] += number
        else:
            moves_dict[where_from][where_to] = number
    print('\nКакой процент выпускников остается работать на каждом факультете?')
    for where_from in moves_dict:
        good = 0
        bad = 0
        for where_to in moves_dict[where_from]:
            if where_to == where_from or (where_from == 'факультет бизнеса и менеджмента' and where_to == 'факультет бизнеса и менеджмента') or where_from == 'миэм' and where_to == 'московский институт электроники и математики им. а.н. тихонова':
                good += moves_dict[where_from][where_to]
            else:
                bad += moves_dict[where_from][where_to]
        good_percent = round(good/(good+ bad)*100, 1)
        if good_percent:
            print('-', where_from, '-', good_percent, '%')


def main():
    table = reading()
    table_pl = reading_pl()
    lazy_statistics(table)
    lazy_statistics_pl(table_pl)
    incredible_thing(table, table_pl)
    do_plot(top(table, 150, 'first_edu_school'), 'Из каких университетов приходят работать в ВШЭ?', (0, 0, 0.3, 0, 0))
    do_plot(top(table, 150, 'highest_degree'), 'Какие ученые степени у работников?')
    do_plot(top(table, 19, 'hse_dep', False), 'Какой факультет ВШЭ закончили работники?')
    do_plot(top(table_pl, 380, 'faculty'), 'На каких факультетах работают в ВШЭ?')
    do_plot(top(table_pl, 250, 'position'), 'Какие позиции занимают работники в НИУ ВШЭ?')


if __name__ == '__main__':
    main()
