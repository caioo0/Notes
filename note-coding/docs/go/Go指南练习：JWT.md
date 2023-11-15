# JWT 认证框架

- jwt-go
- [gino-jwt]()
- [hertz-jwt](https://juejin.cn/post/7166600531434012679) 

## jWT的概念

JSON Web Token(JWT)是一种开放标准（RFC 7519）,用于在各方之间作为JSON对象安全地传输信息。

JWT是一个字符串，包含：**头部、载荷和签名**。

JWT在web中是基于令牌的轻量级认证模式。

### **实现逻辑**

1  客户端提交用户凭证（用户名和密码），服务器认证后会生成一个签名的token令牌，并且返回给客户端

2 用户拿着这个令牌请求服务器的资源，每次请求，服务器会解析token是否正确（比如token失效、token合法）

### JWT的基本原理

颁发token时，把自定义信息嵌入token,使用toKen登录服务器验证之后，得到原始用户自定义信息Json.

```
{
    "user_id": "xxxxxx",
    "username": "xxxxxx",
    "role": "xxxxxx",
    "refresh_token": "xxxxx"
}

```

## jwt-go框架的使用



### 引入jwt-go包，并import

```go
go get -u github.com/golang-jwt/jwt/v5

# 代码处加入

import github.com/golang-jwt/jwt/v5
```

### 定义参数结构体

```go
type Myclaims struct{
	Username string 'json:"username"'
	Userid   string 'json:"userid"'
	jwt.StandardClaims // jwt.StandardClaims包含了官方定义的字段
}
```

### 然后我们定义JWT的过期时间，比如2小时

```go
const TokenExpireDuration = time.Hour*2
```

### 定义加密密钥

```go
var MySecret = []byte("bytedance")
```

### 定义GenToken方法 - 登录后生成token

```go

func GenToken(username string, id int64) (string, error) {
   c := Myclaims{
      Username: username, //携带的自定义字段
      ID:       id,//携带的自定义字段
      StandardClaims: jwt.StandardClaims{
         ExpiresAt: time.Now().Add(TokenExpireDuration).Unix(), //过期时间
         IssuedAt:  time.Now().Unix(),//签发时间
         Issuer:    "bytedance",//签发人
      },
   }
   // 用指定的哈希方法创建签名对象
   token := jwt.NewWithClaims(jwt.SigningMethodHS256, c)
   return token.SignedString(Secret)
}

```

### ParseToken方法- 解析token--登陆后携带，每次访问都解析token

```go
func ParseToken(tokenString string) (*Myclaims, error) {
   token, err := jwt.ParseWithClaims(tokenString, &Myclaims{}, func(token *jwt.Token) (interface{}, error) {
      return Secret, nil
   })
   if err != nil {
      return nil, err
   }
   if claims, ok := token.Claims.(*Myclaims); ok && token.Valid {
      return claims, nil
   }
   return nil, errors.New("invalid token")
}

```

## RefreshToken方法--更新token

```go
func RefreshToken(tokenString string) (string, error) {
   jwt.TimeFunc = func() time.Time {
      return time.Unix(0, 0)
   }
   token, err := jwt.ParseWithClaims(tokenString, &Myclaims{}, func(token *jwt.Token) (interface{}, error) {
      return Secret, nil
   })
   if err != nil {
      return "", err
   }
   if claims, ok := token.Claims.(*Myclaims); ok && token.Valid {  //*Myclaims带指针
      jwt.TimeFunc = time.Now
      claims.StandardClaims.ExpiresAt = time.Now().Add(1 * time.Hour).Unix() //设定增加的时间
      return GenToken(claims.Username, claims.ID)
   }
   return "", errors.New("Couldn't handle this token")
}

```

### JWTAuthMiddleware方法-拦截的认证中间件，每次访问都经过它，并检查携带的token

```go

func JWTAuthMiddleware() func(ctx *gin.Context) {
   return func(ctx *gin.Context) {
      // 根据实际情况取TOKEN,可以从header\query\form等。
      // 客户端携带Token有三种方式 1.放在请求头 2.放在请求体 3.放在URI 。具体实现方式要依据你的实际业务情况决定
      //tokenStr := ctx.Request.Header.Get("Authorization")//这里假设Token放在Header的Authorization中
      tokenStr := ctx.Query("token")//这里假设从query取
      if tokenStr == "" {
         ctx.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{
            "code": -1,
            "msg":  "Have not token",
         })
         return
      }
      claims, err := ParseToken(tokenStr)
      if err != nil {
         ctx.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{
            "code": -1,
            "msg":  "ERR_AUTH_INVALID",//token无效
         })
         return
      } else if time.Now().Unix() > claims.ExpiresAt {
         ctx.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{
            "code": -1,
            "msg":  "ERR_AUTH_EXPIRED",//token超市
         })
         return
      }
      // 此处已经通过了, 可以把Claims中的有效信息拿出来放入上下文使用
      ctx.Set("username", claims.Username)
      ctx.Set("id", claims.ID)
      ctx.Next()
   }
}

```

### 指定任意路由使用中间件

```go
func main() {
	r := gin.Default()
	r.POST("/login", router.Login) //
	authorized := r.Group("/auth") //设定组路由
	authorized.Use(jwt.JWTAuthMiddleware())//部分路由使用中间件
	{
		authorized.GET("/getUserInfo", router.GetUserInfo)
	}
	r.Run(":8080")
}
```

