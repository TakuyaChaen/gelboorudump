#!/usr/bin/env python
#    Copyright (C) 2018  Takuya Chaen
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib.request
import sys
import re
import time

class Gelbooru():

    site_url = "gelbooru.com"
    id_per_page = 24
    posts_prefix ="index.php?page=post&s=list&tags="
    page_prefix = "&pid="
    post_regex = 'a.*?href=\"(.*?)\"'
    postdir = "posts/"
    headers = { "User-Agent" :  "Mozilla/4.0" }
    image_regex = 'src=\"(.*)\".+id=\"image'

    def __init__(self,page,tag):
        self.tag = tag
        self.page = page

    def get_post_url(self):
        return_list = []
        pid_num = (self.page * self.id_per_page) - self.id_per_page
        get_url = "http://" +  self.site_url + "/" + self.posts_prefix
        get_url += self.tag + self.page_prefix + str(pid_num)
        req = urllib.request.Request(get_url, None, self.headers)
        response = urllib.request.urlopen(req)
        charset = response.headers.get_content_charset()
        if charset==None:
            charset = "utf-8"
        html = response.read().decode('utf-8')
        post_url_list = re.findall(self.post_regex,html)
        for posts in post_url_list:
            if posts.find('//gelbooru.com/index.php') > -1:
                add_url = posts.replace("amp;","")
                return_list.append(add_url)
        return return_list

    def get_image_link_and(self,get_url):
        return_url_list = []
        req = urllib.request.Request("https:" + get_url, None, self.headers)
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        image_url_list = re.findall(self.image_regex,html)
        for image_url in image_url_list:
            if image_url.find('https') != -1:
                return_url_list.append(image_url)
            else:
                return_url_list.append(self.http +  self.site + image_url)
        return return_url_list

if __name__ == '__main__':
    args = sys.argv
    if len(args) > 3:
        get_tag = str(args[1])
        start_num = args[2]
        end_num = args[3]
        start_num = int(start_num)
        end_num = int(end_num)
        for number in range(start_num,end_num):
            time.sleep(1)
            gelbooru = Gelbooru(number,get_tag)
            ret_list = gelbooru.get_post_url()
            if len(ret_list) == 0:
                exit()
            for post_url in ret_list:
                image_url_list = gelbooru.get_image_link_and(post_url)
                for urls in image_url_list:
                    print(urls)
    else:
        print("usage: python3 gelbooru.py tag start end ")
        print("   ex: python3 gelbooru.py 2girl 1 3 ")
        print("   ex: python3 gelbooru.py 2girl 1 3 > url.txt")
