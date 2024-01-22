import numpy as np
import xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 使用 sklearn 的 make_classification 方法生成数据
X, Y = make_classification(n_samples=3000, n_features=20, n_informative=20,
                           n_redundant=0, n_repeated=0, n_classes=20, n_clusters_per_class=1,
                           class_sep=2, flip_y=0, weights=None, random_state=1)

# 划分训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# 参数设置
param = {
    'max_depth': 3,  # 树的最大深度
    'eta': 0.3,  # 学习率
    'objective': 'multi:softmax',  # 多类别分类问题
    'num_class': 20  # 类别数量
}

# 转换为DMatrix数据格式
dtrain = xgb.DMatrix(X_train, label=Y_train)
dtest = xgb.DMatrix(X_test, label=Y_test)

# 使用xgb.cv寻找最优的迭代次数
cv_result = xgb.cv(param, dtrain, num_boost_round=1000, nfold=5, early_stopping_rounds=50, metrics='merror', seed=0)
num_round_best = cv_result['test-merror-mean'].idxmin() + 1

# 训练模型
bst = xgb.train(param, dtrain, num_round_best)

# 预测
preds = bst.predict(dtest)

# 计算并打印准确率
accuracy = accuracy_score(Y_test, preds)
print('Test Accuracy: ', accuracy)
