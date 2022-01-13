'''Input = ["jack","And","jack", "jill","jack","jill"] No of Occurrence of Each string in the Array
output: {"jack": 3, "jill": 2,’And’:1}'''


# my_list=["jack","And","jack", "jill","jack","jill"]
# final_dict={}
# for i in my_list:
#     if i not in final_dict:
#         final_dict[i]=0
#     if i in final_dict:
#         final_dict.update({i:final_dict[i]+1})
# print(final_dict)
#
# dec_list=[[1,2,3],10,2,3,4,'Kongu Engg College',34]
# dec_list[1:]
#
# [10,2,3,4,'Kongu Engg College',34]
#
# dict_two={'key1':'Selvam','key2':'Porchelvi','key3':10.8,'key4':[2,3],'key5':dict_one}
# print(dict_two['key2'])Porchelvi
#
# import re
# txt = "The rain in Spain"
# x = re.findall("ai", txt)
# print(x)

'''
Input : This is a typical sentence. 
Reverse the Order of Words with Five Letters or More
Output : This is a lacipyt .ecnetnes
'''
# str1='This is a typical sentence'
# my_list=str1.split()
# final_list=[]
# for i in my_list:
#     if len(i)>5:
#         final_list.append(i[::-1])
#     else:
#         final_list.append(i)
# print(" ".join(final_list))


# from django.db import models
#
# class User(models.Model):
#     name=models.CharField(max_length=255)
#     age=models.IntegerField(max_length=3,null=True)
#     gender=models.CharField(max_length=10)
#
#     def __str__(self):
#         return self.name




'''Writing Program  to Count the Number of Capital Letters from a File'''

'''who are all the employees  drawing the second  largest  salary for each city'''


# select max(salary) from employee where salary<(select max(salary) from employee) where city



