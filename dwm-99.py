#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

print('for循环版本：')
for i in range(1, 10):
    for j in range(1, i+1):
        print('%d*%d=%d' % (j, i, j*i), end='    ')
    print("\r\n")

print('while循环版本')
i = 1
while i < 10:
    j = 1
    while j < i+1:
        print('%d*%d=%d' % (j, i, j*i), end='    ')
        j += 1
    i += 1
    print("\r\n")