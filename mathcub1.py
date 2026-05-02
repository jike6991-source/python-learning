"""
MathorCup 2026 C题 问题一 代码实现
方案：LASSO回归筛选特征 + 多因素Logistic回归评估体质贡献度
作者：基于建模老师指导
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LassoCV, LogisticRegressionCV
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

# ==================== 1. 数据读取与预处理 ====================
# 请根据实际文件路径修改
df = pd.read_excel("附件1：样例数据.xlsx", sheet_name='Sheet1', engine='openpyxl')
# 定义特征列
# 血常规相关指标
blood_features = ['HDL-C（高密度脂蛋白）', 'LDL-C（低密度脂蛋白）', 'TG（甘油三酯）',
                  'TC（总胆固醇）', '空腹血糖', '血尿酸', 'BMI']
# 活动能力评分
activity_features = ['ADL总分', 'IADL总分', '活动量表总分（ADL总分+IADL总分）']
# 九种体质积分（注意列名在数据中是中文）
tizhi_features = ['平和质', '气虚质', '阳虚质', '阴虚质', '痰湿质', '湿热质', '血瘀质', '气郁质', '特禀质']
# 协变量（用于体质贡献度分析时控制混杂）
covariates = ['年龄组', '性别', '吸烟史', '饮酒史']

# 目标变量
y_tanshi = df['痰湿质']                # 痰湿积分（连续值）
y_gao = df['高血脂症二分类标签']       # 高血脂症二分类标签 (0/1)

# 合并待筛选特征
X_features = blood_features + activity_features

# 检查缺失值
print("\n缺失值统计:")
print(df[X_features + [y_tanshi.name, y_gao.name]].isnull().sum())

# 通常数据较干净，若有缺失可酌情填充（本数据未发现缺失）
df = df.dropna(subset=X_features + [y_tanshi.name, y_gao.name])

# ==================== 2. LASSO特征筛选 ====================
# 对连续特征进行标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[X_features])

# ---- 2.1 针对痰湿积分的LASSO回归 ----
print("\n=== 开始 LASSO 回归 (目标：痰湿积分) ===")
lasso_tanshi = LassoCV(cv=5, random_state=2026, max_iter=5000)
lasso_tanshi.fit(X_scaled, y_tanshi)

# 获取非零系数特征
coef_tanshi = pd.Series(lasso_tanshi.coef_, index=X_features)
selected_tanshi = coef_tanshi[coef_tanshi != 0].index.tolist()
print(f"LASSO 选中的最优 alpha: {lasso_tanshi.alpha_:.4f}")
print("对痰湿积分有显著影响的指标 (系数非零):")
for feat, coef in coef_tanshi[coef_tanshi != 0].items():
    print(f"  {feat}: {coef:.4f}")

# ---- 2.2 针对高血脂症二分类的LASSO逻辑回归 ----
print("\n=== 开始 LASSO 逻辑回归 (目标：高血脂症) ===")
lasso_gao = LogisticRegressionCV(cv=5, penalty='l1', solver='saga',
                                  max_iter=5000, random_state=2026)
lasso_gao.fit(X_scaled, y_gao)

# 获取非零系数特征
coef_gao = pd.Series(lasso_gao.coef_[0], index=X_features)
selected_gao = coef_gao[coef_gao != 0].index.tolist()
print(f"LASSO 逻辑回归选中的最优 C: {lasso_gao.C_[0]:.4f}")
print("对高血脂症有显著影响的指标 (系数非零):")
for feat, coef in coef_gao[coef_gao != 0].items():
    print(f"  {feat}: {coef:.4f}")

# ---- 2.3 取交集作为最终关键指标 ----
final_key_features = list(set(selected_tanshi) & set(selected_gao))
print("\n=== 最终筛选出的关键指标 (交集) ===")
print(final_key_features)

# 如果交集为空，可放宽策略，取并集或根据系数绝对值大小手动补充
if len(final_key_features) == 0:
    print("注意：交集为空，建议检查数据或考虑取并集。")
    final_key_features = list(set(selected_tanshi) | set(selected_gao))
    print("当前采用并集作为关键指标：", final_key_features)

# ==================== 3. 九种体质对高血脂发病风险的贡献度分析 ====================
print("\n=== 九种体质贡献度分析 (多因素 Logistic 回归) ===")

# 构建特征矩阵：九种体质积分 + 协变量
X_tizhi = df[tizhi_features + covariates]
X_tizhi = sm.add_constant(X_tizhi)  # 添加截距项

# 拟合逻辑回归模型
logit_model = sm.Logit(y_gao, X_tizhi.astype(float))
result = logit_model.fit(disp=0)  # disp=0 不打印迭代过程

# 输出模型摘要（可选）
# print(result.summary())

# 计算 OR 值 (优势比) 和 置信区间
params = result.params
conf = result.conf_int()
conf['OR'] = np.exp(params)  # OR = exp(系数)
conf.columns = ['2.5%', '97.5%', 'OR']
conf['P>|z|'] = result.pvalues

# 只提取九种体质的结果
or_table = conf.loc[tizhi_features].sort_values('OR', ascending=False)
print("\n九种体质对高血脂发病风险的 OR 值及显著性：")
print(or_table.round(3))

# 找出贡献度最高的体质
top_tizhi = or_table.index[0]
print(f"\n贡献度最高的体质是：{top_tizhi} (OR = {or_table.loc[top_tizhi, 'OR']:.3f})")

# ==================== 4. 结果汇总输出 ====================
print("\n" + "="*50)
print("问题一 结论汇总")
print("="*50)
print(f"1. 关键预警指标 (共{len(final_key_features)}个): {final_key_features}")
print("2. 九种体质对高血脂发病风险的贡献度排名 (按 OR 降序):")
for idx, row in or_table.iterrows():
    sig = "***" if row['P>|z|'] < 0.001 else ("**" if row['P>|z|'] < 0.01 else ("*" if row['P>|z|'] < 0.05 else ""))
    print(f"   {idx}: OR={row['OR']:.3f} (95%CI: {row['2.5%']:.3f}-{row['97.5%']:.3f}), p={row['P>|z|']:.4f} {sig}")