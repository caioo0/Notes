from CART import DecisionTreeRegressor
from sklearn.tree import DecisionTreeRegressor as dt
from sklearn.datasets import make_regression

if __name__ == "__main__":

    """
    url: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_regression.html 
    n_samples：样本数
    n_features：特征数(自变量个数)
    n_informative：参与建模特征数
    n_targets：因变量个数
    noise：噪音
    bias：偏差(截距)
    coef：是否输出coef标识
    random_state：随机状态若为固定值则每次产生的数据都一样
    """

    # 模拟回归数据集
    X, y = make_regression(
        n_samples=200, n_features=10, n_informative=5, random_state=40,noise=0.2
    )


    my_cart = DecisionTreeRegressor(max_depth=2)
    my_cart.fit(X, y)
    res1 = my_cart.predict(X)
    importance1 = my_cart.feature_importances_

    sklearn_cart = dt(max_depth=2)
    sklearn_cart.fit(X, y)
    res2 = sklearn_cart.predict(X)
    importance2 = sklearn_cart.feature_importances_

    # 预测一致的比例
    print(((res1-res2)<1e-8).mean())

    # 特征重要性一致的比例
    print(((importance1-importance2)<1e-8).mean())