import requests
import re
import pickle
import time
import progressbar
from operator import attrgetter
from utils import *
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
                print('에피소드 목록이 최신상태입니다.')
                self.is_up_to_date = True
                # return True
            else:
                # print(item[0].No, self.episode_list[0].No)
                print('에피소드 목록이 최신상태가 아닙니다.')
                self.is_up_to_date = False
                # return False
        except IndexError:
            print('에피소드 목록이 비어있습니다.')

    def update_episode_list(self, force_update=False):
        content_no_list = []
        count = 0

        class BreakIt(Exception):
            pass

        for i in self.episode_list:
            content_no_list.append(i.No)

        # 강제 업데이트가 꺼져있으면
        if force_update is False:
            if content_no_list == []:
                print('에피소드 목록이 비어있습니다.')
            # 최신글과 목록 최상위 글이 같으면
            elif self.is_up_to_date is True:
                print('에피소드 목록이 이미 최신상태입니다!')
                print(count, '개의 에피소드가 추가되었습니다.')
            # 최신글과 목록 최상위 글이 다르면
            elif not self.is_up_to_date:
                dummy = []
                try:
                    for item in range(1, 100):
                        update_list = get_webtoon_list(self.webtoon_id, item)
                        # 1번 페이지부터 글목록을 가져오고
                        for content in update_list:
                            # 글목록을 하나씩 돌면서
                            if content.No not in content_no_list:
                                # 글 번호가 가지고 있는 글 번호 목록에 없으면
                                dummy.append(content)
                                print(f'episode {content.Title} added')
                                count += 1  # 카운터 올려주고
                                continue
                            elif content.No in content_no_list:
                                # 글 번호가 가지고 있는 글 번호 목록에 있는 순간
                                dummy.extend(self.episode_list)
                                self.episode_list = dummy
                                del dummy
                                print('에피소드 목록 업데이트 완료!')
                                print(count, '개의 에피소드가 목록에 추가되었습니다.')
                                print('이제 에피소드 목록이 최신상태입니다.')
                                raise BreakIt  # 에러 일으키면서 안쪽 루프 깨고

                except BreakIt:  # 에러 받으면서 바깥쪽 루프 깬다.
                    pass

        elif force_update is True:  # 강제 업데이트 켜져있으면
            print('강제 업데이트를 시작합니다...', '\n')

            if content_no_list == []:
                print('에피소드 목록이 비어있습니다.')

            elif self.is_up_to_date is True:  # 최신글이랑 가지고 있는 글 최상위랑 비교
                print('에피소드 목록이 이미 최신상태입니다.')
                print(count, '개의 에피소드가 추가되었습니다.')

            elif not self.is_up_to_date:  # 목록이 최신이 아니면
                try:
                    for item in range(1, 100):

                        update_list = get_webtoon_list(self.webtoon_id, item)
                        # 1번 페이지부터 글목록 가져오고
                        for content in update_list:
                            # 글목록의 글 하나씩 돌면서
                            if content.No not in content_no_list:
                                # 글번호가 가지고 있는 글번호 목록에 없으면
                                self.episode_list.insert(0, content)
                                # 계속 추가함
                                count += 1
                                # 카운터도 계속 올려주다가
                                print(f'에피소드 {content.Title} 추가됨.')
                                continue

                            elif content.No in content_no_list:
                                # 글번호가 가지고 있는 글번호 목록에 있으면
                                self.episode_list.remove(content)
                                # 원래꺼 지우고
                                self.episode_list.insert(0, content)
                                # 해당 글번호 글 추가해주고
                                print(f'에피소드 {content.Title} 추가됨.')
                                count += 1  # 카운터도 올려주고
                                if content.No == content_no_list[-1]:
                                    self.episode_list.reverse()
                                    print('에피소드 목록 업데이트 완료!')
                                    print(count, '개의 에피소드가 추가되었습니다.')
                                    print('이제 에피소드 목록이 최신상태입니다.')
                                    raise BreakIt  # 끝냄
                                else:
                                    continue

                except BreakIt:
                    pass

    def clear_episode_list(self, filename=None, make_sure='bypass'):
        if make_sure == 'y':
            self.episode_list = []
            print('에피소드 목록을 비웠습니다!')
        elif make_sure == 'bypass':
            self.episode_list = []
        elif make_sure == 'rf':
            self.episode_list = []
            os.remove(f'./saved_list/{filename}')
        else:
            print('에피소드 목록을 삭제하지 않았습니다.')

    def save(self, path=None, file_type='txt'):
        if self.episode_list == []:
            print('에피소드 목록이 비어있습니다.')

        elif file_type == 'html':
            f = open(f'./saved_webtoons/{path}.{file_type}', 'wt')
            f.write(HTML_HEAD)
            for i in self.episode_list:
                if type(i) == int:
                    continue
                f.write(HTML_BODY.format(img=i.Img_url,
                        title=i.Title,
                        rating=i.Rating,
                        date=i.Date,
                        webtoon_id=self.webtoon_id,
                        No=i.No,
                        ))
            f.write(HTML_TAIL)

            f.close()
            print(f'에피소드 목록을 ./saved_list/{path}.{file_type} 에 성공적으로 저장하였습니다.')

        elif file_type == 'txt':
            f = open(f'./saved_list/{path}.{file_type}', 'wb')
            if type(self.episode_list[-1]) == int:
                pass
            else:
                self.episode_list.append(self.webtoon_id)
            pickle.dump(self.episode_list, f)
            f.close()
            print(f'에피소드 목록을 ./saved_list/{path}.{file_type} 에 성공적으로 저장하였습니다.')
        else:
            print('txt와 html 타입만 지원합니다.')

    def load(self, path=None):
        f = open(f'./saved_list/{path}', 'rb')
        self.episode_list = pickle.load(f)
        f.close()
        print(f'에피소드 목록을 ./saved_list/{path} 에서 성공적으로 불러왔습니다.')
        if type(self.episode_list[-1]) == int:
            return self.episode_list.pop()
        else:
            pass

    def get_contents(self):

        # 에피소드 리스트에서 에피소드 내용 이미지 리스트 추출
        for episode in self.episode_list:
            content_list = []
            try:
                content_info = {'titleId': self.webtoon_id, 'no': episode.No}
            except AttributeError:
                continue
            url = requests.get('http://comic.naver.com/webtoon/detail.nhn?',
                               params=content_info)
            content_data = url.text
            content_bs = BeautifulSoup(content_data, 'lxml')
            content_data_div = content_bs.find_all('div', class_='wt_viewer')
            try:
                content_img = content_data_div[0].find_all('img')
            except IndexError:
                print('성인 웹툰입니다. 성인 웹툰 다운로드는 아직 지원되지 않습니다.')
                print('')
                break
            for i in content_img:
                content_list.append(i.get('src'))
            count = 1

            os.makedirs(f'webtoon/{self.webtoon_id}/{episode.No}_{episode.Title}',
                        exist_ok=True)
            

            print(f'{episode.Title} 다운로드 시작')
            referer_url = f'http://comic.naver.com/webtoon/list.nhn?titleId={self.webtoon_id}'
            user_agent = {'Referer': referer_url}

            # 폴더 생성
            HTML_CONTENT = open(f'webtoon/{self.webtoon_id}/{episode.No}_{episode.Title}/{episode.No}.html', 'wt')
            HTML_CONTENT.write(HTML_HEAD_CONTENT)
            for i in content_list:
                img = requests.get(i, headers=user_agent)
                f = open(f'webtoon/{self.webtoon_id}/{episode.No}_{episode.Title}/{episode.No}_{count}.jpg', 'wb')
                f.write(img.content)
                f.close()
                filedirection = f'./{episode.No}_{count}.jpg'
                HTML_CONTENT.write(HTML_BODY_CONTENT.format(
                                   filedirection=filedirection))
                print(f'{count}.jpg 다운로드 완료', end='\r')
                count += 1
            # 경로 이미 존재할 경우 스킵
            # if os.path.exists(filepath):
                # continue
            HTML_CONTENT.write(HTML_TAIL_CONTENT)
            HTML_CONTENT.close()
            print('다운로드 완료              ')
        print('전체 목록 다운로드 완료')

    # print(content_list)
# yumi = NaverWebtoonCrawler('694131')
# yumi.get_episode_list(1)
# print(yumi.episode_list)
# yumi.up_to_date
# yumi.total_episode_count()
# yumi.update_episode_list(force_update=False)
# yumi.update_episode_list()
# print(yumi.episode_list)
# yumi.up_to_date

# yumi.get_contents()
# yumi.clear_episode_list()
# print(yumi.episode_list)
# yumi.load('test.txt')
# print(yumi.episode_list)
