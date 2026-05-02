import random
num = random.randint(1,10)
a=int(input("请输入你猜的数字"))
if a== num :
    print("恭喜你第一次就猜对了")
else:
    if a > num :
        print("猜大了")
    else :
            print("猜小了")
    a = int(input("请再次输入你猜的数字"))
    if a == num :
            print("祝贺你第二次猜对了")
    else :
            if a > num:
              print("猜大了")
            else :
              print("猜小了")

            a = int(input("请再次输入你猜的数字"))
            if a == num :
                print("你终于猜对了")
            else :
                print("猜三次都没猜到还是回家吧孩子")



