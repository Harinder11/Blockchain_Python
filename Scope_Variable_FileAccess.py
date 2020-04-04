
#With Global keyword

# name = "HSK"

# def get_name():
#     global name
#     name = input('Your name please')

# get_name()
# print(name)


# #Without global keyword
# name = "HSK"

# def get_name():
#     #name = input('Your name please')
#     name = "koranga"
#     print(name)
# get_name()
# print(name)

# #Write only to a file and creating if file does not exists
# f = open('test.txt', mode='w')
# f.write('Hi this is Harinder')
# f.close()

# # #Read only from a file, to read complete file f1.read(), to read some characters use f1.read(10)
# # f1 = open('test.txt', mode = 'r')
# # print(f1.read(12))
# # f1.close()

# #Write at the end if file exists
# f2 = open('test.txt', mode = 'a')
# f2.write('\nand I am Great')
# f2.close()

#Readline and readlines. Readline will return just 1 line (str), readlines returns a list and each ele is a line
f3 = open('test.txt', mode = 'r')
file_read = f3.readline()
while file_read:
    print(file_read)
    file_read = f3.readline()
f3.close()


#with block, we can use with which closes the file as soon as the block executution gets over
with open('test.txt', mode = 'w') as f4:
    f4.write('HSK is Great')
input('Enter something...')
