import requests
import urllib
import sys
import re
import io

p = re.compile("javascript: player\('(\d+)', '(\d+)', '(\d+)'")

urls = []

for line in sys.stdin:
    m = p.search(line)
    if m:
        tblChapterLecIdx = m.group(1)
        tblUnitIdx = m.group(2)
        tblLecturePermissionIdx = m.group(3)
        urls.append(
            f"https://www.mastertopik.com/player/pLecture/player_mobile.asp?tblChapterLecIdx={tblChapterLecIdx}&tblUnitIdx={tblUnitIdx}&tblLecturePermissionIdx={tblLecturePermissionIdx}&mediaType=ML"
        )

print("<html><body><h1>MasterTopik Lessons</h1><ul>")
lesson = 0
for url in urls:
    lesson += 1
    page = requests.get(url)

    licenseRe = re.compile('license = "([^"]+)"')
    strCidRe = re.compile('strCid = "([^"]+)"')
    infoUrlRe = re.compile('info_url = "([^;]+)";')

    license = None
    strCid = None
    info_url = None

    for line in io.StringIO(str(page.content)):
        l = licenseRe.search(line)
        if l:
            license = l.group(1)
            m = strCidRe.search(line)
        if m:
            strCid = m.group(1)
        n = infoUrlRe.search(line)
        if n:
            info_url = re.sub('" \+ StarPlayerApp\.license \+ "', license, n.group(1))
            info_url = re.sub('" \+ strCid \+ "', strCid, info_url)

    print(
        '<li><a href="starplayerplus://?'
        + urllib.parse.urlencode(
            {
                "license": license,
                "url": info_url,
                "debug": "false",
                "version": "1.0.0",
                "pmp": "true",
                "offline_check": "false",
                "referer": url,
                "from": "safari",
                "referer_return": "true",
            }
        )
        + '">Lesson '
        + str(lesson)
        + "</a></li>"
    )

print("</ul></body></html>")
