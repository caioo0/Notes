# next.js

## 实战案例

###  1. 环境要求

node版本 18.11.0

```
npm install @nestjs/cli  
```

 版本不兼容通过 `nvm` 切换匹配的node版本 

### 2. 初始化项目

```
E:\code\react>npm install -g @nestjs/cli

added 254 packages in 19s

E:\code\react>nest new react-hello
⚡  We will scaffold your app in a few seconds..

? Which package manager would you ❤️  to use? npm
CREATE react-hello/.eslintrc.js (663 bytes)
CREATE react-hello/.prettierrc (51 bytes)
CREATE react-hello/nest-cli.json (171 bytes)
CREATE react-hello/package.json (1942 bytes)
CREATE react-hello/README.md (3340 bytes)
CREATE react-hello/tsconfig.build.json (97 bytes)
CREATE react-hello/tsconfig.json (546 bytes)
CREATE react-hello/src/app.controller.spec.ts (617 bytes)
CREATE react-hello/src/app.controller.ts (274 bytes)
CREATE react-hello/src/app.module.ts (249 bytes)
CREATE react-hello/src/app.service.ts (142 bytes)
CREATE react-hello/src/main.ts (208 bytes)
CREATE react-hello/test/app.e2e-spec.ts (630 bytes)
...
√ Installation in progress... ☕

🚀  Successfully created project react-hello
👉  Get started with the following commands:

$ cd react-hello
$ npm run start


                          Thanks for installing Nest 🙏
                 Please consider donating to our open collective
                        to help us maintain this package.


               🍷  Donate: https://opencollective.com/nest

```

然后生成某个 Module 的代码

```
E:\code\react\react-hello>nest g resource xxx
? What transport layer do you use? REST API
? Would you like to generate CRUD entry points? Yes
CREATE src/xxx/xxx.controller.ts (862 bytes)
CREATE src/xxx/xxx.controller.spec.ts (546 bytes)
CREATE src/xxx/xxx.module.ts (233 bytes)
CREATE src/xxx/xxx.service.ts (593 bytes)
CREATE src/xxx/xxx.service.spec.ts (439 bytes)
CREATE src/xxx/dto/create-xxx.dto.ts (29 bytes)
CREATE src/xxx/dto/update-xxx.dto.ts (165 bytes)
CREATE src/xxx/entities/xxx.entity.ts (20 bytes)
UPDATE package.json (1975 bytes)
UPDATE src/app.module.ts (304 bytes)
√ Packages installed successfully.
```



## 报错处理



**1. 错误**
Error: Invalid <Link> with <a> child. Please remove <a> or use <Link legacyBehavior>. Learn more: https://nextjs.org/docs/messages/invalid-new-link-with-extra-anchor

**解决方法**  

`next.config.js` 添加expermental 

```
/** @type {import('next').NextConfig} */
module.exports = {
  reactStrictMode: true,
  experimental: {
    newNextLinkBehavior: false,
  },
}


```

或者您可以简单地删除`<a>`并确保属性移到`<link>`标记。