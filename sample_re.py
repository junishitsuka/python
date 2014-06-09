#! /usr/bin/python
# coding: UTF-8

import re

text ="https://twitter.com, facebook:http://facebook.com/control/event"

while re.search(r'(https?://[a-zA-Z0-9.-]*)', text):
    match = re.search(r'(https?://[a-zA-Z0-9.-]*)', text)
    if match:
        replace = match.group(1).split('://')
        text = text.replace(match.group(1), replace[1])
