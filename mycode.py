import gurobipy as gp
from gurobipy import GRB

# 参数
m = 18  # 公主数量
n = 31  # 王子数量
k=5
# 需求量
demand_100 = 10 * m  # 公主需要 10*m 个 100 cm 的布料
demand_60 = 15 * n   # 王子需要 15*n 个 60 cm 的布料

# 创建模型
model = gp.Model("cutting_stock")

# 添加决策变量 X_i1, X_i2 和 Y_i
X1 = model.addVars(k, vtype=GRB.INTEGER, name="X1", lb=0)  # X_i1: 100cm的布料数
X2 = model.addVars(k, vtype=GRB.INTEGER, name="X2", lb=0)  # X_i2: 60cm的布料数
Y = model.addVars(k, vtype=GRB.INTEGER, name="Y", lb=0)    # Y_i: 第i种裁剪方案的执行次数

# 目标函数：最小化浪费布料的长度
model.setObjective(
    gp.quicksum((400 * Y[i])for i in range(k) )- (100 * demand_100 + 60 * demand_60) ,
    GRB.MINIMIZE
)

# 添加约束：每个裁剪方案的布料总长度不能超过 400
for i in range(k):
    model.addConstr(100 * X1[i] + 60 * X2[i] <= 400, name=f"LengthConstraint_{i}")
# 添加约束：满足需求
model.addConstr(gp.quicksum((X1[i] * Y[i])for i in range(k)) >= demand_100, name="Demand100")
model.addConstr(gp.quicksum((X2[i] * Y[i])for i in range(k)) >= demand_60, name="Demand60")
model.update()
model.write("result/cutting_stock.lp")

# 求解模型

model.optimize()

# 输出结果
if model.status == GRB.OPTIMAL:
    print("最优解:")
    for i in range(k):
        print(f"裁剪方案 {i + 1}: {Y[i].x} 次, 100cm裁剪 {X1[i].x} 次, 60cm裁剪 {X2[i].x} 次")
    print(f"最小浪费布料总长度：{model.objVal}")
else:
    print("没有找到最优解")