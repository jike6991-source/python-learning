#age =  int(input("请输入你的年龄"))
if 18 <= int(input("请输入你的年龄")) <= 30:
    print("你的年纪符合要求")
    if int(input("请输入你的工作时间")) >= 2 :
        print("你的工作时间符合")
    elif int(input("请输入你的级别")) > 3:
        print("你的级别符合")
    else :
         print("你的工作时间和级别都不符合")
else :
    print("你的年级不符合")
