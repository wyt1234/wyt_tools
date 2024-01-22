import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# 假设您有几千个数据点，每个数据点有两个特征
n_samples = 3000  # 样本数量
n_classes = 20  # 类别数量

# 创建特征
# 第一个特征是0到1之间的随机小数
feature1 = torch.rand(n_samples, 1)
# 第二个特征是0或1的随机二进制标签
feature2 = torch.randint(0, 2, (n_samples, 1)).float()

# 将两个特征合并为一个特征矩阵
X_train = torch.cat((feature1, feature2), dim=1)

# 创建标签，这里是一个20分类的问题
Y_train = torch.randint(0, n_classes, (n_samples,))

# 创建数据集和数据加载器
train_dataset = TensorDataset(X_train, Y_train)
train_loader = DataLoader(dataset=train_dataset, batch_size=64, shuffle=True)


# 定义模型架构
class MultiClassNet(nn.Module):
    def __init__(self):
        super(MultiClassNet, self).__init__()
        self.fc1 = nn.Linear(2, 128)  # 输入层到隐藏层1
        self.fc2 = nn.Linear(128, 128)  # 隐藏层1到隐藏层2
        self.fc3 = nn.Linear(128, n_classes)  # 隐藏层2到输出层

    def forward(self, x):
        x = torch.relu(self.fc1(x))  # ReLU激活函数
        x = torch.relu(self.fc2(x))  # ReLU激活函数
        x = self.fc3(x)  # 没有激活函数，因为接下来要用CrossEntropyLoss
        return x


# 初始化模型
model = MultiClassNet()

# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()  # 多分类问题的损失函数
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam优化器

# 训练模型
for epoch in range(10):
    for inputs, labels in train_loader:
        optimizer.zero_grad()  # 清除梯度
        outputs = model(inputs)  # 前向传播
        loss = criterion(outputs, labels)  # 计算损失
        loss.backward()  # 反向传播
        optimizer.step()  # 更新权重

    print(f'Epoch {epoch + 1} / 10, Loss: {loss.item()}')

# 模型评估（示例）
# 实际情况中，您应该在一个独立的测试集上评估模型性能
with torch.no_grad():
    outputs = model(X_train)
    _, predictions = torch.max(outputs, 1)
    correct = (predictions == Y_train).float().sum()
    accuracy = correct / n_samples

print(f'Accuracy: {accuracy:.4f}')
