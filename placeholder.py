company = "传智播客"
code = "003032"
equity1 = 19.99
gowing = 1.2
time = 7
equity2 = equity1 * gowing ** time
print(f"公司：{company}，股票代码：{code}，当前股价:{equity1}")
print("每日增长系数是：%.1f,经过%d天的增长后，股价来到了：%.2f" %(1.2,7,equity2))
