import requests
import re
import pickle
from operator import attrgetter
from utils import Episode, get_webtoon_list
from bs4 import BeautifulSoup

class NaverWebtoonCrawler:

    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        self.episode_list = list()
        self.is_up_to_date = None

    def get_episode_list(self, *args):
        if args[0] == 'full':
            item = get_webtoon_list(self.webtoon_id, 1, 60)
        elif len(args) == 2:
            item = get_webtoon_list(self.webtoon_id, args[0], args[1])
        elif len(args) == 1:
            item = get_webtoon_list(self.webtoon_id, args[0])
        for i in item:
            self.episode_list.append(i)
        return self.episode_list


    def total_episode_count(self):
        # 가장 최근화 글번호 리턴
        item = get_webtoon_list(self.webtoon_id, 1)
        return item[0].No
        
    @property
    def up_to_date(self):
        # get_episode_list로 가져온 리스트 첫 요소와 가장 최신화의 첫 요소 No 비교
        item = get_webtoon_list(self.webtoon_id, 1)
        try:
            if item[0].No == self.episode_list[0].No:
                # print(item[0].No, self.episode_list[0].No)
                print('episode_list is UP TO DATE.')
                self.is_up_to_date = True
                # return True
            else:
                # print(item[0].No, self.episode_list[0].No)
                print('episode_list is NOT up to date.')
                self.is_up_to_date = False
                # return False
        except IndexError:
            print('episode list is empty')

    def update_episode_list(self, force_update=False):
        """
        self.episode_list에 존재하지 않는 episode들을 self.episode_list에 추가
        :param force_update: 이미 존재하는 episode도 강제로 업데이트
        :return: 추가된 episode의 수 (int)
        """
        content_no_list = []
        count = 0
        class BreakIt(Exception):
            pass
            
        for i in self.episode_list:
            content_no_list.append(i.No)
        # 강제 업데이트가 꺼져있으면
        if force_update == False:
            # 최신글과 목록 최상위 글이 같으면
            if self.is_up_to_date == True:
                print('episode_list is already up to date!')
                print(count, 'episodes were added')
            # 최신글과 목록 최상위 글이 다르면
            elif not self.is_up_to_date:
                dummy = []
                try:
                    for item in range(1, 100):
                        update_list = get_webtoon_list(self.webtoon_id, item)  # 1번 페이지부터 글목록을 가져오고
                        for content in update_list:  # 글목록을 하나씩 돌면서
                            
                            if content.No not in content_no_list:  # 글 번호가 가지고 있는 글 번호 목록에 없으면
                                dummy.append(content)
                                print(f'episode {content.Title} added')
                                count += 1  # 카운터 올려주고
                                continue
                            elif content.No in content_no_list:  # 글 번호가 가지고 있는 글 번호 목록에 있는 순간
                                dummy.extend(self.episode_list)
                                self.episode_list = dummy
                                del dummy
                                print('update finished!')
                                print(count, 'episodes were added to the list')
                                print('episode list is UP TO DATE')
                                raise BreakIt  # 에러 일으키면서 안쪽 루프 깨고
                        

                except BreakIt:  # 에러 받으면서 바깥쪽 루프 깬다.
                    pass
            
        elif force_update == True:  # 강제 업데이트 켜져있으면
            print('force updating...')
            if self.is_up_to_date == True:  # 최신글이랑 가지고 있는 글 최상위랑 비교
                print('episode_list is already up to date!')
                print(count, 'episodes were added')

            elif not self.is_up_to_date:  # 목록이 최신이 아니면
                try:
                    for item in range(1, 100):

                        update_list = get_webtoon_list(self.webtoon_id, item)  # 1번 페이지부터 글목록 가져오고
                        for content in update_list:  # 글목록의 글 하나씩 돌면서
                            if content.No not in content_no_list:  # 글번호가 가지고 있는 글번호 목록에 없으면
                                self.episode_list.insert(0, content)  # 계속 추가함
                                count += 1  # 카운터도 계속 올려주다가
                                print(f'episode {content.Title} added')
                                continue

                            elif content.No in content_no_list:  # 글번호가 가지고 있는 글번호 목록에 있으면
                                self.episode_list.remove(content)  # 원래꺼 지우고
                                self.episode_list.insert(0, content)  # 해당 글번호 글 추가해주고
                                print(f'episode {content.Title} added')
                                count += 1  # 카운터도 올려주고
                                if content.No == content_no_list[-1]:
                                    self.episode_list.reverse()
                                    print('update finished!')
                                    print(count, 'episodes were added to the list')
                                    print('episode list is now UP TO DATE')
                                    raise BreakIt  # 끝냄
                                else:
                                    continue
                except BreakIt:
                    pass

    def clear_episode_list(self):
        self.episode_list = []
        return 'episode list has been cleared!'

    def save(self, path=None):
        f = open(f'{path}', 'wb')
        pickle.dump(self.episode_list, f)
        f.close()
        print(f'episode list successfully saved to {path}')

    def load(self, path=None):
        f = open(f'{path}', 'rb')
        self.episode_list = pickle.load(f)
        f.close()
        print(f'{path} successfully loaded to episode list')

# yumi = NaverWebtoonCrawler('557672')
# yumi.get_episode_list(4)
# print(yumi.episode_list)
# yumi.up_to_date
# yumi.total_episode_count()
# yumi.update_episode_list(force_update=False)
# yumi.update_episode_list()
# print(yumi.episode_list)
# yumi.up_to_date

# yumi.save('./python/list1.txt')
# yumi.clear_episode_list()
# print(yumi.episode_list)
# yumi.load('test.txt')
# print(yumi.episode_list)
