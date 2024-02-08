import random


my_list = [1, 3, 10, "ahoj", 30,70, (1, 2)]
random_element = random.choice(my_list)
print(my_list)
print(random_element)
print("co to je za index")





user_choice = input()


if my_list[int(user_choice)] == random_element:

    print("good")
else:
    print("bad")




