## 一、判断题



1、在Column和Row容器组件中，justifyContent用于设置子组件在主轴方向上的对齐格式，alignItems用于设置子组件在交叉轴方向上的对齐格式。**（正确）**

2、所有使用@Component修饰的自定义组件都支持onPageShow，onBackPress和onPageHide生命周期函数。**（错误）**

3、使用http模块发起网络请求时，必须要使用on(‘headersReceive’）订阅请求头，请求才会成功。**（错误）**

4、Video组件可以支持本地视频路径和网络路径播放。播放网络视频时，需要申请权限ohos.permission.INTERNET。**（正确）**

5、Ability是系统调度应用的最小单元，是能够完成一个独立功能的组件。一个应用可以包含一个或多个Ability。**（正确）**

6、Tabs组件仅可包含子组件TabsContent，每一个页签对应一个内容视图即TabContet组件。**（正确）**

7、@CustomDialog装饰器用于装饰自定义弹窗组件，使得弹窗可以动态设置内容及样式。**（正确）**

8、每调用一次router.pushUrl()方法，默认情况下，页面栈数量会加1，页面栈支持的最大页面数量为32。**（正确）**

9、首选项preferences是以Key-Value形式存储数据，其中Key是可以重复。**（错误）**

10、Web组件对于所有的网页都可以使用zoom(factor: number)方法进行缩放。**（错误）**

11、每一个自定义组件都有自己的生命周期。**（正确）**

## 二、单选题

12、下面哪一个事件方法可以获取到List滑动的偏移量**（A）**

**A. onScroll**

B. onScrollIndex

C. onReachStart

D. onReachEnd

13、发起网络数据请求需要导入以下哪个模块**（A）**

**A. import http from ‘@ohos.net.http’**

B. import http from ‘@ohos.net.https’

C. import request from ‘@ohos.request’

D. import request from ‘@ohos.net.request’

14、Row组件中有两个Text组件，如果使用justifyContent对齐方式，下面哪个属性可以实现左右两端对齐**（D）**

A. FlexAlign.Start

B. FlexAlign.SpaceEvenly

C. FlexAlign.End

**D. FlexAlign.SpaceBetween**

15、下面哪个方法，可以跳转到一个新页面，并销毁当前页面**（B）**

A. router.pushUrl()

**B. router.replaceUrl()**

C. router.back()

D. router.clear()

16、例如现在要实现一个广告弹窗，包含图片和文本等信息，使用下面那种弹窗可以实现**（B）**

A. AlertDialog

**B. @CustomDialog**

C. TextPickerDialog

D. TimePickerDialog

17、使用Image组件加载网络图片需要如下哪种权限**（B）**

A. ohos.permission.READ_MEDIA

**B. ohos.permission.INTERNET**

C. ohos.permission.GET_NETWORK_INFO

D. ohos.permission.DISTRIBUTED_DATASYNC

18、在下面哪个文件中可以设置页面的路径配置信息**（A）**

**A. main_pages.json**

B. module.json5

C. app.json5

D. package.json

19、首选项key的最大长度限制大小为（）字节**（C）**

A. 60

B. 70

**C. 80**

D. 90

20、关于Button组件，下面哪个样式是胶囊型按钮**（A）**

**A. ButtonType.Capsule**

B. ButtonType.Normal

C. ButtonType.Circle

D. 以上都不是

21、下列哪种组合方式不能实现子组件从父子组件之间双向数据同步**（D）**

A. @State和@Link

B. @Provide和@Consume

C. @Observed和@ObjectLink

**D. @State和@Prop**

22、关于Resource是资源引用类型描述错误的是**（C）**

A. Resource是资源引用类型，用于设置组件属性的值。

B. 通过"$r(‘app.type.name’)"的形式引用应用资源，app代表是应用内resources目录中定义的资源，type代表资源类型（或资源的存放位置）。

**C. Resource支持所有的数据类型。**

D. 系统可以根据当前配置加载合适的Resource资源，例如，开发者可以根据屏幕尺寸呈现不同的布局效果，或根据语言设置提供不同的字符串。

23、首选项preferences值的存储支持哪些数据类型**（D）**

A. 数字型

B. 字符型

C. 布尔型

**D. 数字型、字符型、布尔型以及这3种类型的数组类型。**

24、下面哪个组件不能包含子组件**（D）**

A. Row

B. Button

C. Text

**D. LoadingProgress**

25、用哪一种装饰器修饰的组件可作为页面入口组件（B）

A. @Component

B. @Entry

C. @Preview

D. @Builder

26、关于Video组件的回调事件，下列说法错误的是（A）

A. onStart视频播放时触发该事件，可以在这里获取视频时长。

B. onFinish视频播放结束时触发该事件。

C. onPrepared视频准备完成时触发该事件。

D. onUpdate播放进度变化时触发该事件，单位为s，更新时间间隔为250ms。

27、关于@State状态数据特征，下列描述错误的是（C）

A. @State装饰的变量是组件内部的状态数据，当这些状态数据被修改时，将会调用所在组件的build方法进行UI刷新。

B. 标记为@State的属性是私有变量，只能在组件内访问。

C. @State变量可以不用给定初始值。

D. 子组件@Link装饰的变量可以和父组件的@State变量建立双向数据绑定。

28、关于Tabs组件页签的位置设置，下面描述错误的是（D）

A.当barPosition为Start（默认值），vertical属性为false时（默认值），页签位于容器顶部。

B.当barPosition为Start（默认值） ，vertical属性为true时，页签位于容器左侧。

C.当barPosition为End ，vertical属性为false（默认值）时，页签位于容器底部。

D.当barPosition为End ，vertical属性为true时，页签位于容器底部。

29、关于UIAbility的启动模式，下列说法错误的是（C）

A. UIAbility支持单实例、标准模式和指定实例3种启动模式，在module.json中通过launchType配置。

B. singleton为单实例模式，系统中只存在唯一一个实例，startAbility时，如果已存在，则复用系统中的唯一一个实例。

C. standard为标准模式，每次startAbility都会启动一个新的实例，系统默认为standard模式。

D. specified为指定实例模式，运行时由Ability内部业务决定是否创建多实例。

30、关于Web组件，下面描述错误的是（D）

A.WebController控制器可以控制Web组件各种行为，比如forward、backward、runJavaScript等。

B.Web组件支持fileAccess、javaScriptAccess等多种属性的设置，例如 .javaScriptAccess(true)表示允许执行JavaScript脚本。

C.Web组件支持onConfirm、onConsole等多种事件，例如网页调用confirm()告警时触发onConfirm回调。

D.使用Web组件访问在线和离线网页都需要添加ohos.permission.INTERNET权限。

31、关于容器组件Row和Column，下面说法错误的是（D）

A. Column容器的主轴是垂直方向，交叉轴是水平方向；Row容器的主轴是水平方向，交叉轴是垂直方向。

B. 主轴和交叉轴始终是相互垂直的，Row和Column主轴的方向不一样。

C. Column的子组件在主轴方向上的对齐使用justifyContent属性来设置，其参数类型是FlexAlign。

D. Row的子组件在交叉轴方向上的对齐方式使用alignItems属性来设置，其参数类型为HorizontalAlign。

32、页面路由需要导入以下哪个模块（B）

A. import prompt from ‘@ohos.prompt’

B. import router from ‘@ohos.router’

C. import Notification from ‘@ohos.notification’

D. import window from ‘@ohos.window’


## 三、多选题

33、下面哪些容器组件是可以滚动的

A. Scroll

B. List

C. Row

D. Grid

E. Column

34、下面哪些是Ability的生命周期回调函数（ABEF）

A. onCreate

B. onDestroy

C. onPageShow

D. onPageHide

E. onForeground

F. onBackground

35、entry下的module.json5中包含以下哪些信息（BCD）

A. 应用包名和版本号信息

B. Ability的配置信息

C. 设备类型信息

D. 应用权限申请列表

36、以下关于ArkTS声明式开发范式的基本组成说明正确的是（ABCDEF）

A. 装饰器：用来装饰类、结构体、方法以及变量，赋予其特殊的含义，例如@Entry表示这是个入口组件。

B. 自定义组件：可复用的 UI 单元，可组合其它组件。

C. UI描述：声明式的方法来描述UI的结构，例如build()方法中的代码块。

D. 内置组件：ArkTS中默认内置的基本组件和布局组件，开发者可以直接调用，如Column、Text、Divider、Button等。

E. 属性方法：用于组件属性的配置，统一通过属性方法进行设置，如fontSize()、width()、height()、color() 等。

F. 事件方法：用于添加组件对事件的响应逻辑，统一通过事件方法进行设置，如跟随在Button后面的onClick()。

37、关于Tabs组件和TabContent组件，下列描述正确的是（ABCD）

A. TabContent组件不支持设置通用宽度属性，其宽度等于Tabs组件的barWidth属性。

B. TabContent组件不支持设置通用高度属性，其高度由父组件Tabs高度与TabBar组件高度决定。

C. TabsController用于控制Tabs组件进行页签切换，不支持一个TabsController控制多个Tabs组件。

D. TabContent组件的tabBar属性支持使用@Builder构造器生成的组件。

38、关于ForEach(arr, itemGenerator, index)组件的描述正确的是（BCD）

A. ForEach中可以循环遍历逻辑代码，例如console.info(‘hello’)

B. 第一个参数必须是数组，提供循环渲染的数据源。

C. 第二个参数生成子组件的lambda函数，为数据源中的每个数组项生成子组件。

D. 第三个参数为匿名函数，用于给定数组项生成唯一且稳定的键值。

39、针对包含文本元素的组件，例如Text、Button、TextInput等，可以使用下列哪些属性（ABCDE）

A. fontColor

B. fontSize

C. fontStyle

D. fontWeight

E. fontFamily

40、下面哪些组件层次结构是正确的（ABE）

A. Text>Span

B. Button>Column>Image

C. Button>Image>Text

D. Image>Text>Span

E. Column>Row>Button
