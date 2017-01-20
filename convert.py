#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import html
from lxml.etree import tostring
import HTMLParser
import re

f = open('bsm.hhk', 'r')
contents = f.read()
lessons = []
for m in re.finditer('LESSON_ID_\d+\.htm', contents):
    lessons.append(m.group(0))
f.close()

head = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
	<html>
	<head>
	<title></title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<meta http-equiv="Content-Language" content="ru">
	<!--<sty le>@import url(do / cstyle.css);</style>-->
	<link href="docstyle.css" type="text/css" rel="stylesheet" />
	</head>
	<body>''';

f = open('book.html', 'w')
f.write(head)

parser = html.HTMLParser(encoding="utf8")
for lesson in lessons:
    page = html.parse('lessons/'+lesson, parser=parser) 
    for body in page.getroot().cssselect('body'):
        for bad in body.cssselect('#page-title-numbers, sys[name="feedbackform"], #topicfooter, b.r0, b.r1, b.r2, b.r3, b.r4, br, .video_learning, div.hint, .learning-spoiler'):
            bad.getparent().remove(bad)
        for child in body.getchildren():
            f.write(tostring(child)\
                .replace('<b/>','')\
                .replace('/images/','images/'))

f.write('</body></html>')
f.close()
