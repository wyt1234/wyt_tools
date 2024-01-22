import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# 定义模型
class Net(nn.Module):
    def __init__(self, n_features):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(n_features, 100)
        self.fc2 = nn.Linear(100, 20)

    def forward(self, x):
        x = F.relu(self.fc1(x))  # 使用ReLU激活函数，其他常用的激活函数：sigmoid, tanh, LeakyReLU
        x = self.fc2(x)
        return x


# 设置随机数生成种子以获得可重复的结果
torch.manual_seed(1)

# 使用 sklearn 的 make_classification 方法生成数据
X, Y = make_classification(n_samples=3000, n_features=20, n_informative=20,
                           n_redundant=0, n_repeated=0, n_classes=20, n_clusters_per_class=1,
                           class_sep=2, flip_y=0, weights=None, random_state=1)

# 将X和Y转换为torch.tensor
X = torch.from_numpy(X).float()
Y = torch.from_numpy(Y).long()

# 划分训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# 创建模型并设置超参数
model = Net(20)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# 训练模型
for epoch in range(500):
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, Y_train)
    loss.backward()
    optimizer.step()

# 对模型进行测试
model.eval()
with torch.no_grad():
    test_outputs = model(X_test)
    _, predicted = torch.max(test_outputs.data, 1)
    accuracy = accuracy_score(Y_test, predicted)
    print('Test Accuracy: ', accuracy)
