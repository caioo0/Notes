【习题】运行Hello World工程
判断题

1.DevEco Studio是开发HarmonyOS应用的一站式集成开发环境。 （正确）

2.main_pages.json存放页面page路径配置信息。（正确）

单选题

1.在stage模型中，下列配置文件属于AppScope文件夹的是？（C）

A. main_pages.json

B. module.json5

C. app.json5

D. package.json

多选题

1.如何在DevEco Studio中创建新项目？（B C）

A. 在计算机上创建一个新文件，并将其命名为“new harmonyOS项目”

B. 如果已打开项目，从DevEco Studio菜单选择’file>new>Create Project’

C. 如果第一次打开DevEco Studio，在欢迎页点击“Create new Project”

2.module.json5配置文件中，包含了以下哪些信息？（A B D）

A. ability的相关配置信息

B. 模块名

C. 应用的版本号

D. 模块类型

【习题】ArkTS基础知识
判断题

1.循环渲染ForEach可以从数据源中迭代获取数据，并为每个数组项创建相应的组件。（正确）

2.@Link变量不能在组件内部进行初始化。（正确）

单选题

1.用哪一种装饰器修饰的struct表示该结构体具有组件化能力？（A）

A. @Component

B. @Entry

C. @Builder

D. @Preview

2.用哪一种装饰器修饰的自定义组件可作为页面入口组件？（B）

A. @Component

B. @Entry

C. @Builder

D. @Preview

多选题

1.下面哪些函数是自定义组件的生命周期函数？（A B C D E）

A. aboutToAppear

B. aboutToDisappear

C. onPageShow

D. onPageHide

E. onBackPress

2.下面哪些装饰器可以用于管理自定义组件中变量的状态？（C D）

A. @Component

B. @Entry

C. @State

D. @Link

【习题】应用程序框架
判断题

1.一个应用只能有一个UIAbility。（错误）

2.创建的Empty Ability模板工程，初始会生成一个UIAbility文件。（正确）

3.每调用一次router.pushUrl()方法，页面路由栈数量均会加1。（错误）

单选题

1.API9及以上，router.pushUrl()方法，默认的跳转页面使用的模式是哪一种？（A）

A. standard

B. Single

C. Specified

2.UIAbility启动模式需要在module.json5文件中配置哪个字段？（C）

A. module

B. skills

C. launchType

D. abilities

多选题

1.API9及以上，router.pushUrl()方法的mode参数可以配置为以下哪几种跳转页面使用的模式？（A B）

A. Standard

B. Single

C. Specified

2.UIAbility的生命周期有哪几个状态？（A C D F）

A. Create

B. WindowStageCreate

C. Foreground

D. Background

E. WindowStageDestroy

F. Destroy

3.UIAbility有哪几种的启动模式？（A B C）

A. multiton

B. singleton

C. specified

【习题】构建漂亮的页面
判断题

1.在Column容器中的子组件默认是按照从上到下的垂直方向布局的，其主轴的方向是垂直方向，在Row容器中的组件默认是按照从左到右的水平方向布局的，其主轴的方向是水平方向。（正确）

2.List容器可以沿水平方向排列，也可以沿垂直方向排列。（正确）

3.当Tabs组件的参数barPosition为BarPosition.End时，页签位于页面底部。（错误）

4.Resource是资源引用类型，用于设置组件属性的值，可以定义组件的颜色、文本大小、组件大小等属性。（正确）

单选题

1.使用TextInput完成一个密码输入框，推荐设置type属性为下面哪个值？（B）

A. InputType.Normal

B. InputType.Password

C. InputType.Email

D. InputType.Number

2.使用Image加载网络图片，需要以下那种权限？（B）

A. ohos.permission.USE_BLUETOOTH

B. ohos.permission.INTERNET

C. ohos.permission.REQUIRE_FORM

D. ohos.permission.LOCATION

3.下面哪个组件层次结构是错误的？（C）

A. List>ListItem>Column

B. Column>List>ListItem

C. Grid>Row>GridItem

D. Grid>GridItem

多选题

1.Row容器的主轴是水平方向，交叉轴是垂直方向，其参数类型为VerticalAlign （垂直对齐），VerticalAlign 定义了以下几种类型？（A B E）

A. Top

B. Bottom

C. Start

D. End

E. Center

2.下面哪些组件是容器组件？（B C）

A. Button

B. Row

C. Column

D. Image

E. TextInput

3.关于Tabs组件页签的位置设置，下面描述正确的是？（A B C D）

A. 当barPosition为Start（默认值），vertical属性为false时（默认值），页签位于容器顶部。

B. 当barPosition为Start（默认值） ，vertical属性为true时，页签位于容器左侧。

C. 当barPosition为End ，vertical属性为false（默认值）时，页签位于容器底部。

D. 当barPosition为End ，vertical属性为true时，页签位于容器右侧。

【习题】构建更加丰富的页面
判断题

1.@State修饰的属性不允许在本地进行初始化。（错误）

2.@CustomDialog装饰器用于装饰自定义弹窗组件，使得弹窗可以自定义内容及样式。（正确）

3.将Video组件的controls属性设置为false时，不会显示控制视频播放的控制栏。（正确）

4.@Prop修饰的属性值发生变化时，此状态变化不会传递到其父组件。（正确）

单选题

1.使用Video组件播放网络视频时，需要以下哪种权限？（B）

A. ohos.permission.READ_MEDIA

B. ohos.permission.INTERNET

C. ohos.permission.WRITE_MEDIA

D. ohos.permission.LOCATION

2.下列哪种组合方式可以实现子组件从父子组件单向状态同步。（C）

A. @State和@Link

B. @Provide和@Consume

C. @State和@Prop

D. @Observed和@ObjectLink

多选题

1.下列哪些状态装饰器修饰的属性必须在本地进行初始化。（A D）

A. @State

B. @Prop

C. @Link

D. @Provide

E. @Consume

2.ArkUI提供了下面哪些弹窗功能。（A B C D E）

A. AlertDialog

B. TextPickerDialog

C. DatePickerDialog

D. @CustomDialog

E. TimePickerDialog

【习题】属性动画
判断题

1.属性动画中产生动画的属性可以在任意位置声明。（错误）

2.属性动画中改变属性时需触发UI状态更新。（正确）

单选题

1.属性animation可以在哪些组件中使用？（C）

A. 只能基础组件

B. 只能容器组件

C. 基础组件和容器组件

D. 以上都不对

2.属性动画中如何设置反向播放？（D）

A. PlayMode.Normal

B. PlayMode.Alternate

C. PlayMode.AlternateReverse

D. PlayMode.Reverse

3.下面哪种情况不会回调onFinish函数？（C）

A. delay设置为 0

B. tempo设置为 1

C. iterations设置为 -1

D. playMode设置为 PlayMode.Reverse

4.属性动画中关于animation参数说法错误的是？（B）

A. 参数tempo默认值为1.0

B. 参数delay不能大于duration

C. 参数curve可以不设置

D. 参数iterations可以不设置

多选题

1.属性动画支持哪些属性？（A B C D）

A. width

B. rotate

C. opacity

D. scale

2.属性动画中animation的参数有哪些？（A B C D）

A. playMode

B. curve

C. delay

D. onFinish

【习题】从网络获取数据
判断题

1.在http模块中，多个请求可以使用同一个httpRequest对象，httpRequest对象可以复用。（错误）

2.使用http模块发起网络请求后，可以使用destroy方法中断网络请求。（正确）

3.Web组件onConfirm(callback: (event?: { url: string; message: string; result: JsResult }) => boolean)事件，返回false时候触发网页默认弹窗。（正确）

单选题

1.使用http发起网络请求，需要以下哪种权限？（B）

A. ohos.permission.USE_BLUETOOTH

B. ohos.permission.INTERNET

C. ohos.permission.REQUIRE_FORM

D. ohos.permission.LOCATION

2.向服务器提交表单数据，以下哪种请求方式比较合适？（B）

A. RequestMethod.GET

B. RequestMethod.POST

C. RequestMethod.PUT

D. RequestMethod.DELETE

3.下列关于Web组件的属性，描述错误的是？（C）

A. 设置是否开启应用中文件系统的访问，默认启用。$rawfile(filepath/filename)中rawfile路径的文件不受该属性影响而限制访问。

B. imageAccess设置是否允许自动加载图片资源，默认允许。

C. javaScriptAccess设置是否允许执行JavaScript脚本，默认不允许执行。

D. zoomAccess设置是否支持手势缩放，默认允许执行缩放。

4.关于请求返回的响应码ResponseCode，下列描述错误的是？（D）

A. ResponseCode.OK的值为200，表示请求成功。一般用于GET与POST请求。

B. ResponseCode.NOT_FOUND的值为404，表示服务器无法根据客户端的请求找到资源（网页）。

C. ResponseCode.INTERNAL_ERROR的值为500，表示服务器内部错误，无法完成请求。

D. ResponseCode.GONE的值为404，表示客户端请求的资源已经不存在。

多选题

1.Web组件支持下列哪些属性或事件？（A B D）

A. fileAccess(fileAccess: boolean)

B. javaScriptAccess(javaScriptAccess: boolean)

C. on(type: ‘headerReceive’, callback: AsyncCallback): void

D. onConfirm(callback: (event?: { url: string; message: string; result: JsResult }) => boolean)

E. destroy(): void

2.关于http模块描述正确的是？（A B C D）

A. http请求支持get、post、put等常用的请求方式。

B. 可以使用on(‘headersReceive’)订阅请求响应头。

C. post请求的参数可以在extraData中指定。

D. 执行createHttp成功后，返回一个httpRequest对象，里面包括request、destroy、on和off方法。

3.关于Web组件描述正确的是？（A B C D）

A. Web组件是提供具有网页显示能力的一种组件。

B. Web组件传入的地址可以是本地资源也可以是网络资源。

C. WebController可以控制Web组件的各种行为，例如网页的前进、后退等功能。

D. 当访问在线网页时，需添加网络权限。

【习题】保存应用数据
判断题

1.首选项是关系型数据库。（错误）

2.应用中涉及到Student信息，如包含姓名，性别，年龄，身高等信息可以用首选项来存储。（错误）

3.同一应用或进程中每个文件仅存在一个Preferences实例。（正确）

单选题

1.使用首选项要导入的包是哪个？（B）

A. @ohos.data.rdb

B. @ohos.data.preferences

C. @ohos.router

D. @ohos.data.storage

2.首选项的数据持久化后是放在哪里？（C）

A. 内存中

B. 数据库表中

C. 文件中

D. 云端

3.下面哪个接口不是首选项提供的API接口？（B）

A. get()

B. update()

C. put()

D. flush()

多选题

1.HarmonyOS提供的数据管理的方式都有哪些？（A B C D）

A. 首选项

B. 分布式数据服务

C. 关系数据库

D. 分布式数据对象

2.下面说法正确的有？（B C D）

A. 首选项遵循ACID特性

B. 首选项以Key-Value形式存取数据

C. 首选项存储数据数量建议不超过1万条

D. 首选项的key为String类型

【习题】给应用添加通知和提醒
判断题

1.构造进度条模板通知，name字段当前需要固定配置为downloadTemplate。（正确）

2.给通知设置分发时间，需要设置showDeliveryTime为false。（错误）

3.OpenHarmony提供后台代理提醒功能，在应用退居后台或退出后，计时和提醒通知功能被系统后台代理接管。（正确）

单选题

1.将通道设置为下面哪个类型，可以显示横幅通知？（A）

A. SlotType.SOCIAL_COMMUNICATION

B. SlotType.SERVICE_INFORMATION

C. SlotType.CONTENT_INFORMATION

D. SlotType.OTHER_TYPES

2.下列哪个是从API 9 开始支持的后台代理提醒功能模块。（A）

A. @ohos.reminderAgentManager

B. @ohos.reminderManager

C. @ohos.reminderAgent

D. @ohos.notificationManager

多选题

1.下面哪些方法可以移除通知？（A B）

A. cancel

B. cancelAll

C. removeSlot

2.后台代理提醒业务分为哪几种类型。（A B C）

A. 倒计时类

B. 日历类

C. 闹钟类

D. 日程类

【习题】HarmonyOS应用/元服务上架
判断题

1.元服务发布的国家与地区仅限于“中国大陆” （正确）

2.编译打包的软件包存放在项目目录build > outputs > default下 （正确）

单选题

1.创建应用时，应用包名需要和app.json5或者config.json文件中哪个字段保持一致？ （C）

A. package

B. name

C. bundleName

2.发布应用时需要创建证书，证书类型选择什么类型？（B）

A. 调试证书

B. 发布证书

3.发布应用时需要创建Profile时，类型选择什么类型？ （B）

A. 调试

B. 发布

4.上传发布软件包时，软件包的格式是什么？（B）

A. .zip

B. .app

C. .apk

D. .hap

5.发布后的应用可以在哪里获取？（A）

A. 华为应用市场

B. 华为服务中心

C. 华为生态市场

【习题】使用DevEco Studio高效开发
单选题

1.用哪一种装饰器修饰的组件可作为页面入口组件？（B）

A. @Component

B. @Entry

C. @Preview

D. @Builder

2.ArkTS Stage模型支持API Version 9，关于其工程目录结构说法正确的是？（C）

A. oh-package.json5用于存放应用级配置信息，包括签名、产品配置等

B. build-profile.json5用于配置三方包声明文件的入口及包名

C. module.json5包含HAP的配置信息、应用在具体设备上的配置信息以及应用的全局配置信息

D. app.json5用于编写应用级编译构建任务脚本

3.DevEco Studio提供模拟器供开发者运行和调试HarmonyOS应用/服务，以下说法错误的是？（A）

A. 本地模拟器是创建和运行在本地计算机上的，需要登录授权

B. 本地模拟器支持音量大小调节、电池电量调节、屏幕旋转等功能

C. 向本地模拟器安装应用/服务的时候，不需要给应用签名

D. DevEco Studio会启动应用/服务的编译构建，完成后应用/服务即可运行在本地模拟器上

多选题

1.DevEco Studio支持使用多种语言进行应用/服务的开发，包括ArkTS、JS和C/C++。在编写应用/服务阶段，可以通过以下哪些方法提升编码效率？（A B C D）

A. 提供代码的智能补齐能力，编辑器工具会分析上下文并理解项目内容，并根据输入的内容，提示可补齐的类、方法、字段和关键字的名称等

B. 在编辑器中调用ArkTS API接口或ArkTS/JS组件时，支持在编辑器中快速、精准调取出对应的参考文档

C. 代码格式化功能可以帮助您快速的调整和规范代码格式，提升代码的美观度和可读性

D. 如果输入的语法不符合编码规范，或者出现语义语法错误，编辑器会显示错误或警告

2.关于预览器的使用，以下哪些说法是正确的？（A B C D）

A. 在开发界面UI代码过程中，如果添加或删除了UI组件，您只需Ctrl+S进行保存，然后预览器就会立即刷新预览结果

B. 在预览器界面，可以在预览器中操作应用/服务的界面交互动作，如单击、跳转、滑动等，与应用/服务运行在真机设备上的界面交互体验一致

C. 组件预览通过在组件前添加注解@Preview实现

D. 页面预览通过在工程的ets文件头部添加注解@Entry实现

【习题】三方库
判断题

1.三方组件是开发者在系统能力的基础上进行了一层具体功能的封装，对其能力进行拓展的工具 。（正确）

2.可以通过ohpm uninstall 指令下载指定的三方库（错误）

3.lottie使用loadAnimation方法加载动画。（正确）

单选题

1.通过ohpm安装lottie后，在哪个文件中会生成相关的配置信息？（B）

A. module.json5

B. oh-package.json5

C. app.json5

D. main_page.json

2.lottie订阅事件的API为？（C）

A. lottie.setSpeed()

B. lottie.setDirection()

C. animationItem.addEventListener()

D. animationItem.removeEventListener()

多选题

1.下列属于lottie提供的动画控制API的是？（A B C D）

A. lottie.play()

B. lottie.pause()

C. lottie.stop()

D. lottie.goToAndPlay()

【习题】HarmonyOS云开发
判断题

1.HarmonyOS云开发可以在一个项目中同时实现端侧和云侧功能的开发。（正确）

2.进行端云一体开发时，开发者需要精通前端、后端不同的开发语言。（错误）

单选题

1.开发者在DevEco Studio中，可以通过什么形式进行HarmonyOS云开发？（B）

A. IDE插件

B. 工程模板

C. 命令行工具

D. 可视化工具

2.HarmonyOS云开发当前支持最低API版本是多少？（D）

A. API 6

B. API 7

C. API 8

D. API 9

多选题

1.HarmonyOS云开发工程结构分哪些部分？（A B C）

A. 端开发工程（Application）

B. 云开发工程（CloudProgram）

C. 端侧公共库（External Libraries）

D. 公共资源库（Resource）

2.HarmonyOS云开发工程创建后，会自动开通哪些服务？（A B C D）

A. 云函数

B. 云数据库

C. 云存储

D. 认证服务
