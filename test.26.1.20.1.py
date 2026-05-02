high = int(input("请输入你的身高"))
if high > 120 :
   print("你的身高超过了限制")
   print("但你的VIP等级如果大于3级也可以免费")
   if int(input("请输入你的VIP等级")) > 3 :
       print("你的VIP等级足够可以免门票")
   else :
    print("你条件都不满足，需要付门票")
else:
    print("身高小于120直接免门票")
