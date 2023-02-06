#### 学习资料
1. [centos 8 下安装nginx 1.9.8](https://www.91mszl.com/zhangwuji/article/details/1289)
2. [Markdown 语法手册](https://blog.csdn.net/witnessai1/article/details/52551362)


Git global setup
```md
git config --global user.name "Administrator"
git config --global user.email "297495363@qq.com"
```


Create a new repository
```md
git clone ssh://git@120.77.223.72:222/root/docsify.git
cd docsify
git switch -c main
touch README.md
git add README.md
git commit -m "add README"
git push -u origin main
```
Push an existing folder
```md
cd existing_folder
git init --initial-branch=main
git remote add origin ssh://git@120.77.223.72:222/root/docsify.git
git add .
git commit -m "Initial commit"
git push -u origin main
```
Push an existing Git repository
```md
cd existing_repo
git remote rename origin old-origin
git remote add origin ssh://git@120.77.223.72:222/root/docsify.git
git push -u origin --all
git push -u origin --tags
```

