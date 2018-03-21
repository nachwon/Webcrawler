#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import crawler_restarter
from webtoon_crawler import NaverWebtoonCrawler
from utils import *


class BreakIt(Exception):
    def __str__(self):
        return '사용자에 의해 세션이 종료되었습니다.'

print('==============================================')
print('=            Naver_Webtoon_Crawler           =')
print('==============================================')
print('                             - Created by Che1')
print('')

while True:
    print("")
    print('==================명령어 목록=================')
    print('list : 요일별 웹툰 목록 확인')
    print('search : 웹툰 정보 검색')
    print('load : 저장된 웹툰 목록 확인')
    print('웹툰 ID (6자리 숫자) : 해당 ID 웹툰 불러오기')
    print('==============================================')
    print('')
    webtoon_id = input('명령 입력 >>> ')
    print("")

    collected_webtoon = None

    if webtoon_id == 'list':
        print('원하는 요일을 아래와 같이 입력해주세요.')
        print('월요일: mon')
        print('화요일: tue')
        print('수요일: wed')
        print('목요일: thr')
        print('금요일: fri')
        print('토요일: sat')
        print('일요일: sun')

        print('')
        day = input('요일 입력 >>> ')
        print("")
        webtoon_list = get_webtoon_id(day)
        list_index = 0
        for i in webtoon_list:
            print(f'{list_index}. ID : {i.Id}, Title : {i.Title}')
            list_index += 1
        print("")

        select_id = input('목록에서 선택 >>> ')
        print('')
        webtoon_id = webtoon_list[int(select_id)].Id
        print(f'웹툰 ID: {webtoon_id}')
        break

    elif webtoon_id == 'load':
        saved_list = os.listdir('./saved_list')
        if saved_list == []:
            print('저장된 파일이 없습니다.')
            continue

        saved_file_counter = 0
        for i in saved_list:
            print(f'{saved_file_counter}. ', i)
            saved_file_counter += 1
        print('')

        loadname = input('불러올 파일 이름 입력 >>> ')
        print('')
        if len(loadname) <= 3:
            loadname = saved_list[int(loadname)]
            print(f'{loadname} 파일 불러오는 중...', '\n')

            try:
                f = open(f'./saved_list/{loadname}', 'rb')
            except FileNotFoundError:
                print('파일 이름 또는 경로가 잘못되었습니다.')

        else:
            try:
                f = open(f'./saved_list/{loadname}', 'rb')
            except FileNotFoundError:
                print('파일 이름 또는 경로가 잘못되었습니다.')

        list_loaded = pickle.load(f)
        f.close()
        webtoon_id = list_loaded.pop()
        collected_webtoon = NaverWebtoonCrawler(webtoon_id)
        collected_webtoon.load(loadname)
        break

    elif webtoon_id == 'search':
        while True:
            print('웹툰을 검색합니다.')
            print('"검색어 -옵션"으로 검색 옵션을 지정할 수 있습니다. (지정하지 않으면 제목 검색)')
            print('')
            print('옵션 목록:')
            print('-a: 작가 검색')
            print('-t: 제목 검색')
            print('')
            search_keyword = input('검색어 입력 >>> ')
            print('')
            search_keyword = search_keyword.split(' -')

            if len(search_keyword) == 1:
                keyword = search_keyword[0]
                mode = 1
                print(f'{search_keyword[0]} 검색 결과:')
                print('')
                break

            elif len(search_keyword) == 2:
                keyword = search_keyword[0]
                mode = search_keyword[1]
                if mode == 'a':
                    print('-작가 검색-')
                    print('')
                elif mode == 't':
                    print('-제목 검색-')
                    print('')
                print(f'{search_keyword[0]} 검색 결과:')
                print('')
                break

            else:
                print('검색어 입력이 잘못되었습니다.')
                continue

        result_dict = webtoon_search(keyword, mode)
        list_number = 0

        for i in result_dict:
            print(f"{list_number}. ID : {i['Id']} Title : {i['Title']}")
            list_number += 1
        print('')

        if result_dict == []:
            print('결과 없음', '\n')
            continue
        elif result_dict != []:
            select_id = input('목록에서 선택 >>> ')
            print('')
            webtoon_id = result_dict[int(select_id)]['Id']
            break

    elif webtoon_id == 'q':
        raise BreakIt

    elif len(webtoon_id) == 6:
        webtoon_id = webtoon_id
        break

    else:
        print('웹툰 ID 혹은 명령어를 입력하세요.', '\n')
try:
    webtoon_id = int(webtoon_id)
    info_dic = get_webtoon_info(webtoon_id)
    print('')
    print('==============================================', '\n')
    print(f'  제목: {info_dic["Webtoon_title"]}   작가: {info_dic["Author"]}')

except ValueError:
    print('6자리의 숫자로 입력하세요.', '\n')
# except AttributeError:
#     print('잘못된 웹툰 ID 입니다. 요일별 웹툰 혹은 웹툰 검색기능을 활용하세요.', '\n')
except BreakIt as e:
    print(e)

if collected_webtoon is not None:
    pass
else:
    collected_webtoon = NaverWebtoonCrawler(webtoon_id)

while True:
    print('')
    print('===================functions==================')
    print('1. 에피소드 목록 불러오기')
    print('2. 전체 에피소드 개수 확인')
    print('3. 에피소드 목록 확인')
    print('4. 에피소드 목록이 최신인지 확인')
    print('5. 최신 에피소드 목록으로 업데이트')
    print('6. 에피소드 목록 삭제')
    print('7. 에피소드 목록 저장')
    print('8. 에피소드 목록 불러오기')
    print('==============================================')
    print('9. 에피소드 목록에서 웹툰 추출')
    print('r. 세션 재시작')
    print('q. 나가기')
    print('')
    selection = input('>>> ')
    print('')

    if selection == '1':
        collected_webtoon.clear_episode_list()
        print('한 자리 수를 입력하면 해당 페이지 목록을 가져옵니다.')
        print('i, j 의 형식으로 입력하면 i 페이지부터 j 페이지까지의 목록을 불러옵니다.')
        print("모든 에피소드를 가져오려면 'full' 을 입력하세요.", '\n')
        page_num = input('>>> ')
        print('')
        page_num = page_num.split(',')

        if page_num[0] == 'full':
            collected_webtoon.get_episode_list('full')
            print('모든 에피소드를 가져왔습니다.')
        elif len(page_num) == 1:
            collected_webtoon.get_episode_list(int(page_num[0]))
            print(f'웹툰 {webtoon_id}, {page_num[0]} 페이지의 에피소드 목록을 가져왔습니다!')
        elif len(page_num) == 2:
            collected_webtoon.get_episode_list(int(page_num[0]),
                                               int(page_num[1]))
            print(f'웹툰 {webtoon_id}, {page_num[0]} 페이지 부터 {page_num[1]}\
페이지 까지의 에피소드 목록을 가져왔습니다!')
        continue

    elif selection == '2':
        print(f'웹툰 {webtoon_id}는 총 {collected_webtoon.total_episode_count()}\
개의 에피소드가 있습니다.')

    elif selection == '3':
        if len(collected_webtoon.episode_list) == 0:
            print('에피소드 목록이 비어있습니다. 목록을 먼저 가져와주세요.')
        for i in collected_webtoon.episode_list:
            if type(i) == int:
                continue
            try:
                print(f'{i.Title} 평점: {i.Rating} 날짜: {i.Date}')
            except:
                print(i)
        continue

    elif selection == '4':
        collected_webtoon.up_to_date

    elif selection == '5':
        force_update_question = input('강제 업데이트 하시겠습니까? [y/n] ')
        print('')
        if force_update_question == 'y':
            collected_webtoon.update_episode_list(force_update=True)
        else:
            collected_webtoon.update_episode_list(force_update=False)

    elif selection == '6':
        make_sure = input('현재 에피소드 목록을 삭제합니다.진행하시겠습니까? [y/rf/n] \n[rf]: 저장 파일까지 삭제 \n>>> ')
        print('')
        if make_sure == 'rf':
            collected_webtoon.clear_episode_list(filename=loadname,
                                                 make_sure=make_sure)
        else:
            collected_webtoon.clear_episode_list(make_sure=make_sure)

    elif selection == '7':
        savename = input('파일 이름 입력 >>> ')
        filetype = input('파일 타입 입력 >>> ')
        print('')
        collected_webtoon.save(savename, filetype)

    elif selection == '8':
        saved_list = os.listdir('./saved_list')
        if saved_list == []:
            print('저장된 파일이 없습니다.')
            continue

        saved_file_counter = 0
        for i in saved_list:
            print(f'{saved_file_counter}. ', i)
            saved_file_counter += 1
        print('')

        loadname = input('불러올 파일 이름 입력 >>> ')
        print('')
        if len(loadname) <= 3:
            loadname = saved_list[int(loadname)]
            print(f'{loadname} 파일 불러오는 중...', '\n')

            try:
                f = open(f'./saved_list/{loadname}', 'rb')
            except FileNotFoundError:
                print('파일 이름 또는 경로가 잘못되었습니다.')

        else:
            try:
                f = open(f'./saved_list/{loadname}', 'rb')
            except FileNotFoundError:
                print('파일 이름 또는 경로가 잘못되었습니다.')

        list_loaded = pickle.load(f)
        f.close()
        webtoon_id = list_loaded.pop()
        collected_webtoon = NaverWebtoonCrawler(webtoon_id)
        collected_webtoon.load(loadname)
        info_dic = get_webtoon_info(webtoon_id)
        print('')
        print('==============================================', '\n')
        print(f'  제목: {info_dic["Webtoon_title"]}   작가: {info_dic["Author"]}')
        continue

    elif selection == '9':
        if len(collected_webtoon.episode_list) == 0:
            print('에피소드 목록이 비어있습니다. 목록을 먼저 가져와주세요.')
        else:
            collected_webtoon.get_contents()

    elif selection == 'r':
        print('세션을 다시 시작합니다...', '\n')
        crawler_restarter
        break

    elif selection == 'q':
        print('사용자에 의해 세션이 종료되었습니다.')
        raise BreakIt

    else:
        print('잘못된 입력')
