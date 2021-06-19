import urllib.request
import os
import requests
from bs4 import BeautifulSoup
import getopt
import sys


def download_from_url(URL, path, name, extension):
    download_path = f"{path}/{name}.{extension}"
    urllib.request.urlretrieve(URL, download_path)
    print(f"\nFileName:{name}\nPath:{download_path}\n")


def get_html_content(URL):
    res = requests.get(URL)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    return soup


def get_assignment(html_content):
    rows = html_content.find("table", {"class": "table"}).find(
        "tbody").find_all("tr")
    assignments = []
    for row in rows:
        cells = row.find_all("td")
        name = cells[0].get_text()
        id = name.split("_")[-1]
        url = cells[1].find("a", href=True)['href']
        assignment = {}
        assignment['id'] = int(id)
        assignment['name'] = name
        assignment['url'] = url
        assignments.append(assignment)
    assignments = sorted(assignments, key=lambda k: k['id'])
    return assignments


def get_video(html_content):
    rows = html_content.find("table", {"id": "request"}).find(
        "tbody").find_all("tr")
    videos = []
    for row in rows:
        cells = row.find_all("td")
        id = cells[0].get_text()
        name = cells[1].get_text()
        url = cells[2].find("a", href=True)['href']
        video = {}
        video['id'] = int(id)
        video['name'] = name
        video['url'] = "https://nptel.ac.in"+url
        videos.append(video)
    videos = sorted(videos, key=lambda k: k['id'])
    return videos


def download_course(URL, name):
    course_path = f"{ os.path.abspath(os.getcwd()) }/{name}"

    if(not os.path.exists(course_path)):
        os.makedirs(f"{course_path}/videos")
        os.makedirs(f"{course_path}/assignments")

    html = get_html_content(URL)

    # Assigments
    print("\nAssignements\n")
    assignments = get_assignment(html)
    for assignment in assignments:
        download_from_url(assignment["url"], f"{course_path}/assignments",
                          f"{assignment['id']}_{assignment['name']}", "pdf")

    # Videos
    print("\nVideos\n")
    videos = get_video(html)
    for video in videos:
        try:
            download_from_url(
                video["url"], f"{course_path}/videos", f"{video['id']}_{video['name']}", "mp4")
        except:
            print("URL not working !")


if __name__ == "__main__":
    URL = ""
    name = ""
    download_course(URL, name)
