---
title: gin-中间件
date: 2021-06-23 15:03:27
categories: 
- golang
tags:
- gin
- 中间件
---

# 中间件 (middleWare)

- 中间件，对以后的路由全部生效。
  - 设置好中间件以后，所有的路由都会使用这个中间件。
  - 设置以前的路由，不生效。



## 什么是 “中间件”：

- 早期：
  - 用于 系统 和 应用之间。
  - 中间件： 内核 —— 中间件 ——  用户应用

- 现在：
  - 用于 两个模块之间的 功能 软件(模块)
  - 中间件：—— 承上启下。  前后台开发： 路由 ——> 中间件 (起过滤作用) ——> 控制器
  - 特性：对 “中间件”指定位置 ， 以下的路由起作用！以上的，作用不到。

### 中间件类型

- gin 框架规定：中间件类型为：gin.HandlerFunc 类型。

- gin.HandlerFunc 类型。就是 ：

  ```go
  func (c *gin.Context) { 
      
  }
  ```

  ```go
  // 示例：
  func Logger() gin.HandlerFunc {
      return func (c *gin.Context) {   
      }
  }
  r.Use(Logger())		// 传 “中间件” 做参数。
  ```

### 中间件测试

- 中间件使用的 3 个知识：

#### Next()

- 表示，跳过当前中间件剩余内容， 去执行下一个中间件。 当所有操作执行完之后，以出栈的执行顺序返回，执行剩余代码。

- ```go
    
  // 创建中间件
  func Test1(ctx *gin.Context)  {
  	fmt.Println("1111")
  	ctx.Next()
  	fmt.Println("4444")
  }
  // 创建 另外一种格式的中间件.
  func Test2() gin.HandlerFunc {
  	return func(context *gin.Context) {
  		fmt.Println("3333")
  		context.Next()
  		fmt.Println("5555")
  	}
  }
  func main()  {
  	router := gin.Default()
  
  	// 使用中间件
  	router.Use(Test1)
  	router.Use(Test2())
  
  	router.GET("/test", func(context *gin.Context) {
  		fmt.Println("2222")
  		context.Writer.WriteString("hello world!")
  	})
  
  	router.Run(":9999")
  }
  ```

#### return 

- 终止执行当前中间件剩余内容，执行下一个中间件。 当所有的函数执行结束后，以出栈的顺序执行返回，但，不执行return后的代码！

  ```go
  // 创建中间件
  func Test1(ctx *gin.Context)  {
  	fmt.Println("1111")
  	
  	ctx.Next()
  
  	fmt.Println("4444")
  }
  // 创建 另外一种格式的中间件.
  func Test2() gin.HandlerFunc {
  	return func(context *gin.Context) {
  		fmt.Println("3333")
  
  		return
  		context.Next()
  
  		fmt.Println("5555")
  	}
  }
  func main()  {
  	router := gin.Default()
  
  	// 使用中间件
  	router.Use(Test1)
  	router.Use(Test2())
  
  	router.GET("/test", func(context *gin.Context) {
  		fmt.Println("2222")
  		context.Writer.WriteString("hello world!")
  	})
  
  	router.Run(":9999")
  }
  ```

  

#### Abort()

- 只执行当前中间件， 操作完成后，以出栈的顺序，依次返回上一级中间件。

  ```go
  // 创建中间件
  func Test1(ctx *gin.Context)  {
  	fmt.Println("1111")
  
  	ctx.Next()
  
  	fmt.Println("4444")
  }
  // 创建 另外一种格式的中间件.
  func Test2() gin.HandlerFunc {
  	return func(context *gin.Context) {
  		fmt.Println("3333")
  
  		context.Abort()
  
  		fmt.Println("5555")
  	}
  }
  func main()  {
  	router := gin.Default()
  
  	// 使用中间件
  	router.Use(Test1)
  	router.Use(Test2())
  
  	router.GET("/test", func(context *gin.Context) {
  		fmt.Println("2222")
  		context.Writer.WriteString("hello world!")
  	})
  
  	router.Run(":9999")
  }
  
  ```

  

![01](gin-中间件/1582529575294.png)



![02](gin-中间件/1582529769290.png)

### 中间件测试业务时间：

```go
// 创建中间件
func Test1(ctx *gin.Context)  {
	fmt.Println("1111")

	t := time.Now()

	ctx.Next()

	fmt.Println(time.Now().Sub(t))
}

// 创建 另外一种格式的中间件.
func Test2() gin.HandlerFunc {
	return func(context *gin.Context) {
		fmt.Println("3333")
        context.Abort()		// 将 Abort() 替换成 Next()， 反复测试，获取时间差！
		fmt.Println("5555")
	}
}
func main()  {
	router := gin.Default()

	// 使用中间件
	router.Use(Test1)
	router.Use(Test2())

	router.GET("/test", func(context *gin.Context) {
		fmt.Println("2222")
		context.Writer.WriteString("hello world!")
	})

	router.Run(":9999")
}
```



## 小结

- 2种 书写格式：（见 前面笔记）
- 3个 操作函数/关键字： Next()、return、Abort()
- 作用域：作用域 以下 的路由。（ 对以上的 路由 无效！）



# 中间件实战使用

1. 在 web/main.go 中 创建 中间件。

   ```go
   func LoginFilter() gin.HandlerFunc {
   	return func(ctx *gin.Context) {
   		// 初始化 Session 对象
   		s := sessions.Default(ctx)
   		userName := s.Get("userName")
   
   		if userName == nil {
   			ctx.Abort()			// 从这里返回, 不必继续执行了
   		} else {
   			ctx.Next()			// 继续向下
   		}
   	}
   }
   ```

2. 在 所有需要进行 Session 校验操作之前， 添加、使用这个中间件。

   ```go
   // 添加路由分组
   r1 := router.Group("/api/v1.0")
   {
       r1.GET("/session", controller.GetSession)
       r1.GET("/imagecode/:uuid", controller.GetImageCd)
       r1.GET("/smscode/:phone", controller.GetSmscd)
       r1.POST("/users", controller.PostRet)
       r1.GET("/areas", controller.GetArea)
       r1.POST("/sessions", controller.PostLogin)
   
   r1.Use(LoginFilter())  //以后的路由,都不需要再校验 Session 了. 直接获取数据即可!
   
       r1.DELETE("/session", controller.DeleteSession)
       r1.GET("/user", controller.GetUserInfo)
       r1.PUT("/user/name", controller.PutUserInfo)
   }
   ```

