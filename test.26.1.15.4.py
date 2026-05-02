ag = int(input("请输入你的年龄："))
lv = int(input("请输入你的vip等级（1-5）："))
high = int(input("请输入你的身高(cm)："))

if ag <= 18 :
    print("你是未成年，所以不需要支付门票")
elif lv >= 3 :
    print("你的vip等级在3级及三级以上，所以不需要需要支付门票")
elif high <= 120 :
    print ("你的身高在120以下，所以不需要需要支付门票")
else :
    print ("抱歉您什么都不满足只能当付费牛马")
print("欢迎来到牛马之家")
print("祝你成为一个小牛马")