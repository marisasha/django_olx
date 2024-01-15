from django.test import TestCase

num = '523532545'
for i in range(len(num)-3,-1,-3):
    num = num[:i] +' '+num[i:]
print(num)
