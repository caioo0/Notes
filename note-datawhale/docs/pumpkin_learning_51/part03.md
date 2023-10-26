# 三、详读西瓜书+南瓜书第4章

## 1 决策树基本流程

   决策树时一类常见的机器学习方法

- 概念：基于树结构，不断根据某属性划分来进行决策，体现人类在面临决策问题时一种很自然的处理机制。
- 学习的目的：为产生一颗泛化能力强，即 处理未见示例能力的决策树，遵循简单而直观的“分而治之”策略。

![image-20231026090128444](.\img\image-20231026090128444.png)

- 上述图例可以看出：
  1. 每个非叶节点表示一个特征属性测试
  2. 每个分支代表这个特征属性在某个值域上的输出
  3. 每个叶子节点存放一个类别
  4. 每个节点包含的样本集合通过属性测试被划分到子节点中，根节点包含样本全集
- 基本算法：  
  **输入：** 训练集$D=\{(x_1,y_1),(x_2,y_2),\cdot, (x_m,y_m)\}$;  
  &emsp;&emsp;&emsp;属性集$A={a_1,a_2,\cdot,a_d}$  
  **过程：** 函数TreeGenerate($D$,$A$)  
  (1) 生成结点node  
  (2) **if** $D$中样本全属于同一类别$C$ **then**  
  (3) &emsp;将node标记为$C$类叶节点; **return**  
  (4) **end if**  
  (5) **if** $A=\emptyset$ **OR** $D$中样本在$A$上取值相同 **then**  
  (6) &emsp;将node标记为叶结点，其类别标记为$D$中样本数最多的类；**return**  
  (7) **end if**  
  (8) 从$A$中选择最优化分属性$a_*$;  （优化问题是重点）
  (9) **for** $a_*$的每一个值$a_*^v$ **do**  
  (10) &emsp;为node生成一个分支；令$D_v$表示$D$中在$a_*$上取值为$a_*^v$的样本子集;  
  (11) &emsp; **if** $D_v$为空 **then**  
  (12) &emsp;&emsp; 将分支结点标记为叶结点，其类别标记为$D$中样本最多的类; **return**  
  (13) &emsp;**else**  
  (14) &emsp;&emsp; 以TreeGenerate($D_v$, $A \backslash \{ a_* \}$)为分支结点  
  (15) &emsp;**end if**  
  (16) **end for**  
  **输出：** 以node为根结点的一棵决策树
- 决策树是一个递归过程，有三种情况会导致递归返回：
  1. 当前结点包含的样本全部属于同一类，直接将该结点标记为叶结点，其类别设置该类
  2. 当属性集为空，或所有样本在所有属性上取值相同，无法进行划分，将该结点标记为叶结点，其类别设置为其父结点所含样本最多的类别
  3. 当前结点包含的样本集合为空，不能划分，将该结点标记为叶结点，其类别设置为其父结点所含样本最多的类别

## 2 划分选择

### 2.1 信息增益
- 信息熵：度量样本集合纯度最常用的一种指标， 信息熵越低，纯度越高

- 信息熵定义：  
  &emsp;&emsp;假定当前样本集合$D$中第$k$类样本所占的比例为$p_k(k=1,2,\dots,|\mathcal{Y}|)$，则$D$的信息熵表示为

  
  $$
  \text{Ent}(D)=-\sum_{k=1}^{|\mathcal{Y }| } p_{k} \log_2 p_k
  $$

  $\text{Ent}(D)$值越小，则$D$的纯度越高。若p =0,则$plog_2^p = 0$

- 信息增益定义：  
  &emsp;&emsp;假定使用属性$a$对样本集$D$进行划分，产生了$V$个分支节点，$v$表示其中第$v$个分支节点，易知：分支节点包含的样本数越多，表示该分支节点的影响力越大，可以计算出划分后相比原始数据集$D$获得的“信息增益”（information gain）。
  $$
  \text{Gain}(D, \alpha)=\text{Ent}(D)-\sum_{v=1}^{V} \frac{|D^{v}|}{|D|} \text{Ent}(D^v)
  $$
  信息增益越大，使用属性$a$划分样本集$D$的效果越好。

  信息增益越大，使用属性$a$划分样本集$D$的效果越好。

- ID3决策树学习算法是以信息增益为准则

### 2.2 增益率
- 作用：用于解决属性信息熵为0，或远高于其他属性的信息熵问题

- 定义：
  $$
  \text{Gain\_ratio}(D, \alpha) = \frac{\text{Gain}(D, \alpha)} { \text{IV} (\alpha) }
$$
  其中$$
  \text{IV}(\alpha)=-\sum_{v=1}^V \frac{|D^v|}{|D|} \log_2 \frac{|D^v|}{|D|}$$当$\alpha$属性的取值越多时，$\text{IV}(\alpha)$值越大
  
  其中$$
  \text{IV}(\alpha)=-\sum_{v=1}^V \frac{|D^v|}{|D|} \log_2 \frac{|D^v|}{|D|}$$当$\alpha$属性的取值越多时，$\text{IV}(\alpha)$值越大
  
- C4.5算法是以增益率为准则

### 2.3 基尼指数
- CART决策树使用“基尼指数”（Gini index）来选择划分属性
- 作用：表示从样本集$D$中随机抽取两个样本，其类别标记不一致的概率，因此$\text{Gini}(D)$越小越好
- 定义：$$\begin{aligned} \text{Gini}(D) 
&=\sum_{k=1}^{|\mathcal{Y}|} \sum_{k' \neq k} p_k p_{k'} \\
&=1-\sum_{k=1}^{|\mathcal{Y}|} p_k^2 
\end{aligned}$$
- 属性选择：  
使用属性$\alpha$划分后的基尼指数为：
$$\text { Gini\_index }(D, \alpha)=\sum_{v=1}^V \frac{|D^v|}{|D|} \text{Gini}(D^v)$$故选择基尼指数最小的划分属性。

## 3. 剪支处理



## 4. 代码实现

### CART:

```
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from utils import feature_split, calculate_gini

### 定义树结点
class TreeNode():
    def __init__(self, feature_i=None, threshold=None,
                 leaf_value=None, left_branch=None, right_branch=None):
        # 特征索引
        self.feature_i = feature_i          
        # 特征划分阈值
        self.threshold = threshold 
        # 叶子节点取值
        self.leaf_value = leaf_value   
        # 左子树
        self.left_branch = left_branch     
        # 右子树
        self.right_branch = right_branch    
        
       
```

```
### 定义二叉决策树
class BinaryDecisionTree(object):
    ### 决策树初始参数
    def __init__(self, min_samples_split=2, min_gini_impurity=999,
                 max_depth=float("inf"), loss=None):
        # 根结点
        self.root = None  
        # 节点最小分裂样本数
        self.min_samples_split = min_samples_split
        # 节点初始化基尼不纯度
        self.mini_gini_impurity = min_gini_impurity
        # 树最大深度
        self.max_depth = max_depth
        # 基尼不纯度计算函数
        self.gini_impurity_calculation = None
        # 叶子节点值预测函数
        self._leaf_value_calculation = None
        # 损失函数
        self.loss = loss

    ### 决策树拟合函数
    def fit(self, X, y, loss=None):
        # 递归构建决策树
        self.root = self._build_tree(X, y)
        self.loss=None

    ### 决策树构建函数
    def _build_tree(self, X, y, current_depth=0):
        # 初始化最小基尼不纯度
        init_gini_impurity = 999
        # 初始化最佳特征索引和阈值
        best_criteria = None    
        # 初始化数据子集
        best_sets = None        

        # 合并输入和标签
        Xy = np.concatenate((X, y), axis=1)
        # 获取样本数和特征数
        n_samples, n_features = X.shape
        # 设定决策树构建条件
        # 训练样本数量大于节点最小分裂样本数且当前树深度小于最大深度
        if n_samples >= self.min_samples_split and current_depth <= self.max_depth:
            # 遍历计算每个特征的基尼不纯度
            for feature_i in range(n_features):
                # 获取第i特征的所有取值
                feature_values = np.expand_dims(X[:, feature_i], axis=1)
                # 获取第i个特征的唯一取值
                unique_values = np.unique(feature_values)

                # 遍历取值并寻找最佳特征分裂阈值
                for threshold in unique_values:
                    # 特征节点二叉分裂
                    Xy1, Xy2 = feature_split(Xy, feature_i, threshold)
                    # 如果分裂后的子集大小都不为0
                    if len(Xy1) > 0 and len(Xy2) > 0:
                        # 获取两个子集的标签值
                        y1 = Xy1[:, n_features:]
                        y2 = Xy2[:, n_features:]

                        # 计算基尼不纯度
                        impurity = self.impurity_calculation(y, y1, y2)

                        # 获取最小基尼不纯度
                        # 最佳特征索引和分裂阈值
                        if impurity < init_gini_impurity:
                            init_gini_impurity = impurity
                            best_criteria = {"feature_i": feature_i, "threshold": threshold}
                            best_sets = {
                                "leftX": Xy1[:, :n_features],   
                                "lefty": Xy1[:, n_features:],   
                                "rightX": Xy2[:, :n_features],  
                                "righty": Xy2[:, n_features:]   
                                }
        
        # 如果计算的最小不纯度小于设定的最小不纯度
        if init_gini_impurity < self.mini_gini_impurity:
            # 分别构建左右子树
            left_branch = self._build_tree(best_sets["leftX"], best_sets["lefty"], current_depth + 1)
            right_branch = self._build_tree(best_sets["rightX"], best_sets["righty"], current_depth + 1)
            return TreeNode(feature_i=best_criteria["feature_i"], threshold=best_criteria[
                                "threshold"], left_branch=left_branch, right_branch=right_branch)

        # 计算叶子计算取值
        leaf_value = self._leaf_value_calculation(y)

        return TreeNode(leaf_value=leaf_value)

    ### 定义二叉树值预测函数
    def predict_value(self, x, tree=None):
        if tree is None:
            tree = self.root

        # 如果叶子节点已有值，则直接返回已有值
        if tree.leaf_value is not None:
            return tree.leaf_value

        # 选择特征并获取特征值
        feature_value = x[tree.feature_i]

        # 判断落入左子树还是右子树
        branch = tree.right_branch
        if isinstance(feature_value, int) or isinstance(feature_value, float):
            if feature_value >= tree.threshold:
                branch = tree.left_branch
        elif feature_value == tree.threshold:
            branch = tree.left_branch

        # 测试子集
        return self.predict_value(x, branch)

    ### 数据集预测函数
    def predict(self, X):
        y_pred = [self.predict_value(sample) for sample in X]
        return y_pred
```

```
### CART回归树
class RegressionTree(BinaryDecisionTree):
    def _calculate_variance_reduction(self, y, y1, y2):
        var_tot = np.var(y, axis=0)
        var_y1 = np.var(y1, axis=0)
        var_y2 = np.var(y2, axis=0)
        frac_1 = len(y1) / len(y)
        frac_2 = len(y2) / len(y)
        # 计算方差减少量
        variance_reduction = var_tot - (frac_1 * var_y1 + frac_2 * var_y2)
        
        return sum(variance_reduction)

    # 节点值取平均
    def _mean_of_y(self, y):
        value = np.mean(y, axis=0)
        return value if len(value) > 1 else value[0]

    def fit(self, X, y):
        self.impurity_calculation = self._calculate_variance_reduction
        self._leaf_value_calculation = self._mean_of_y
        super(RegressionTree, self).fit(X, y)
```

```
### CART决策树
class ClassificationTree(BinaryDecisionTree):
    ### 定义基尼不纯度计算过程
    def _calculate_gini_impurity(self, y, y1, y2):
        p = len(y1) / len(y)
        gini = calculate_gini(y)
        gini_impurity = p * calculate_gini(y1) + (1-p) * calculate_gini(y2)
        return gini_impurity
    
    ### 多数投票
    def _majority_vote(self, y):
        most_common = None
        max_count = 0
        for label in np.unique(y):
            # 统计多数
            count = len(y[y == label])
            if count > max_count:
                most_common = label
                max_count = count
        return most_common
    
    # 分类树拟合
    def fit(self, X, y):
        self.impurity_calculation = self._calculate_gini_impurity
        self._leaf_value_calculation = self._majority_vote
        super(ClassificationTree, self).fit(X, y)
```

```
from sklearn import datasets
data = datasets.load_iris()
X, y = data.data, data.target
# 注意！是否要对y进行reshape取决于numpy版本
y = y.reshape(-1,1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
clf = ClassificationTree()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print(accuracy_score(y_test, y_pred))
```

```
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print(accuracy_score(y_test, y_pred))
```

```
from sklearn.datasets import load_boston
X, y = load_boston(return_X_y=True)
y = y.reshape(-1,1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
model = RegressionTree()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print("Mean Squared Error:", mse)
```

```
from sklearn.datasets import load_boston
X, y = load_boston(return_X_y=True)
y = y.reshape(-1,1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
model = RegressionTree()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print("Mean Squared Error:", mse)
```

### ID3

```
import numpy as np
import pandas as pd
from math import log
```

```
df = pd.read_csv('./example_data.csv', dtype={'windy': 'str'})
df
```

example_data.csv内容：

```
humility,outlook,play,temp,windy
high,sunny,no,hot,false
high,sunny,no,hot,true
high,overcast,yes,hot,false
high,rainy,yes,mild,false
normal,rainy,yes,cool,false
normal,rainy,no,cool,true
normal,overcast,yes,cool,true
high,sunny,no,mild,false
normal,sunny,yes,cool,false
normal,rainy,yes,mild,false
normal,sunny,yes,mild,true
high,overcast,yes,mild,true
normal,overcast,yes,hot,false
high,rainy,no,mild,true
```

```
def entropy(ele):
    probs = [ele.count(i)/len(ele) for i in set(ele)]
    entropy = -sum([prob*log(prob, 2) for prob in probs])
    return entropy
```

```
entropy(df['play'].tolist())
```

```
def split_dataframe(data, col):
    unique_values = data[col].unique()
    result_dict = {elem : pd.DataFrame for elem in unique_values}
    for key in result_dict.keys():
        result_dict[key] = data[:][data[col] == key]
    return result_dict

split_example = split_dataframe(df, 'temp')
```

```
for item, value in split_example.items():
    print(item, value)
```

```
def choose_best_col(df, label):
    entropy_D = entropy(df[label].tolist())
    cols = [col for col in df.columns if col not in [label]]
    max_value, best_col = -999, None
    max_splited = None
    for col in cols:
        splited_set = split_dataframe(df, col)
        entropy_DA = 0
        for subset_col, subset in splited_set.items():
            entropy_Di = entropy(subset[label].tolist())
            entropy_DA += len(subset)/len(df) * entropy_Di
        info_gain = entropy_D - entropy_DA
        
        if info_gain > max_value:
            max_value, best_col = info_gain, col
            max_splited = splited_set
    return max_value, best_col, max_splited
    
choose_best_col(df, 'play')
```

```
class ID3Tree:
    class Node:
        def __init__(self, name):
            self.name = name
            self.connections = {}

        def connect(self, label, node):
            self.connections[label] = node
            
    def __init__(self, data, label):
        self.columns = data.columns
        self.data = data
        self.label = label
        self.root = self.Node("Root")
        
    def print_tree(self, node, tabs):
        print(tabs + node.name)
        for connection, child_node in node.connections.items():
            print(tabs + "\t" + "(" + connection + ")")
            self.print_tree(child_node, tabs + "\t\t")

    def construct_tree(self):
        self.construct(self.root, "", self.data, self.columns)
        
    def construct(self, parent_node, parent_connection_label, input_data, columns):
        max_value, best_col, max_splited = choose_best_col(input_data[columns], self.label)
        
        if not best_col:
            node = self.Node(input_data[self.label].iloc[0])
            parent_node.connect(parent_connection_label, node)
            return

        node = self.Node(best_col)
        parent_node.connect(parent_connection_label, node)
        
        new_columns = [col for col in columns if col != best_col]
        
        for splited_value, splited_data in max_splited.items():
            self.construct(node, splited_value, splited_data, new_columns)
```

```
tree1 = ID3Tree(df, 'play')
tree1.construct_tree()
```

```
tree1.print_tree(tree1.root, "")
```

```
from sklearn import tree
X = [[0, 0], [1, 1]]
Y = [0, 1]
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)
clf.predict([[2, 2]])
```

```
from sklearn.datasets import load_iris
from sklearn import tree

iris = load_iris()
clf = tree.DecisionTreeClassifier(criterion='entropy', splitter='best')
clf = clf.fit(iris.data, iris.target)
```

```
import graphviz
dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
graph.render('iris')
```

```
dot_data = tree.export_graphviz(clf, out_file=None,
                               feature_names=iris.feature_names,
                               class_names=iris.target_names,
                               filled=True, 
                               rounded=True,
                               special_characters=True)
graph = graphviz.Source(dot_data)
graph
```

