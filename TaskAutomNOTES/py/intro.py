"""
Jeffrey Yau
NSSA 220
"""
func=print
print(type(func))
func("hello world")
def log(val):
    print("LOG: " + str(val))

func=log
func("Hello World")


string = "This is a String"
last_six = string[-6:]
print(last_six)
first_seven= string[:7]
print(first_seven)

middle=string[2:8] # 2-8

#!
# New hello script, you can also do shebang here

# print("hello world".split(" "))
# print("hello world".split(" "))
# L1 = [1,2,3]
# print(L1)
# del L1[3]
# print[L1]
# print(len("abc"))
# print(len("a,b,c".split(",")))
# # .join(iter)
# l2 = "a b c d e".split()
# print(l2)


a = 2.2
print(type(a))
