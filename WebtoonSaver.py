from webtoon_crawler import NaverWebtoonCrawler
from utils import *

class BreakIt(Exception):
    def __str__(self):
        return 'Session Terminated by user'

print('==================================')
print('=      Naver_Webtoon_Crawler     =')
print('==================================')
while True:
    print('type "list" for webtoon id lists')
    print('type "search" to search webtoon id online')
    webtoon_id = input('input webtoon id >>> ')
    print("")

    if webtoon_id == 'list':
        print('type only 3 letters')
        print('Ex: monday: mon')
        day = input('which day? >>> ')
        print("")
        webtoon_list = get_webtoon_id(day)
        list_index = 0
        for i in webtoon_list:
            print(f'{list_index}. ID : {i.Id}, Title : {i.Title}')
            list_index += 1
        print("")

        select_id = input('Select from list >>> ')
        print('')
        webtoon_id = webtoon_list[int(select_id)].Id
        break

    elif webtoon_id == 'search':

        search_keyword = input('search >>> ')
        print('')
        result_dict = webtoon_search(search_keyword)
        list_number = 0

        for i in result_dict:
            print(f"{list_number}. ID : {i['Id']} Title : {i['Title']}")
            list_number += 1
        print('')
        
        if result_dict == []:
            print('No result', '\n')
            continue
        elif result_dict != []:
            select_id = input('Select from list >>> ')
            print('')
            webtoon_id = result_dict[int(select_id)]['Id']
            break

    elif webtoon_id == 'q':
        raise BreakIt
        
    elif len(webtoon_id) == 6:
        webtoon_id = webtoon_id
        break
try:
    webtoon_id = int(webtoon_id)
    collected_webtoon = NaverWebtoonCrawler(webtoon_id)
    info_dic = get_webtoon_info(webtoon_id)
    print('==================================', '\n')
    print(f'제목: {info_dic["Webtoon_title"]}   작가: {info_dic["Author"]}')

except ValueError:
    print('type only 6 digit numbers', '\n')
except BreakIt as e:
    print(e)
    
    
    

while True:
    print('')
    print('=============functions============')
    print('1. get episodes')
    print('2. number of total episodes')
    print('3. show list')
    print('4. check update')
    print('5. update list')
    print('6. clear page list')
    print('7. save list')
    print('8. load list')
    print('q. exit')
    print('')
    selection = input('>>> ')
    print('')

    if selection == '1':
        collected_webtoon.clear_episode_list()
        print('if 1 number is given: gets that page')
        print('if 2 numbers are given: gets pages from i to j')
        print("type 'full' to get all the pages", '\n')
        page_num = input('>>> ')
        print('')
        page_num = page_num.split(',')

        if page_num[0] == 'full':
            collected_webtoon.get_episode_list('full')
            print('all pages have been collected')
        elif len(page_num) == 1:
            collected_webtoon.get_episode_list(int(page_num[0]))
            print(f'{webtoon_id}, page {page_num[0]} collected!')
        elif len(page_num) == 2:
            collected_webtoon.get_episode_list(int(page_num[0]), int(page_num[1]))
            print(f'{webtoon_id}, pages from {page_num[0]} to {page_num[1]} collected!')
        continue

    elif selection == '2':
        print(f'there are total {collected_webtoon.total_episode_count()} episodes in this webtoon')

    elif selection == '3':
        if len(collected_webtoon.episode_list) == 0:
            print('episode list is empty')
        for i in collected_webtoon.episode_list:
            print(f'{i.No}. {i.Title}')
        continue

    elif selection == '4':
        collected_webtoon.up_to_date

    elif selection == '5':
        force_update_question = input('force update? [y/n] ')
        print('')
        if force_update_question == 'y':
            collected_webtoon.update_episode_list(force_update=True)
        else:
            collected_webtoon.update_episode_list(force_update=False)

    elif selection == '6':
        print(collected_webtoon.clear_episode_list())

    elif selection == '7':
        savename = input('filename? >>> ')
        filetype = input('filetype? >>> ')
        print('')
        collected_webtoon.save(savename, filetype)

    elif selection == '8':
        try:
            loadname = input('filename? >>> ')
            print('')
            collected_webtoon.load(loadname)
        except FileNotFoundError:
            print('Wrong filename or directory!')
            continue


    elif selection == 'q':
        print('Session Terminated by user')
        break
    else:
        print('wrong input')