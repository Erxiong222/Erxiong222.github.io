---
title: redis基本操作
date: 2021-06-20 14:51:43
categories: 
- golang
tags:
- redis
---

## Redis 基本使用

1. 修改 配置文件。 /etc/redis/redis.conf . 
   - bind 地址。修改成当前主机地址。 —— 192.168.6.108 
2. port：
   - 6379
3. 开启 redis：
   - sudo  redis-server  /etc/redis/redis.conf
   - 验证 ： ps xua | grep redis  —— iP 和 port
4. 连接 redis ：
   - redis-cli -h 192.168.6.108 -p 6379
5. 查看所有：
   - keys *
6. 删除所有：
   - flushall
7. 添加一条：
   - set key  value  ——   set  hello  world
8. 获取一条：
   - get key 



## go语言操作 Redis

- 从 redis.cn —— 客户端 —— go语言 —— 选择 redigo —— https://godoc.org/github.com/gomodule/redigo/redis#pkg-examples  查看 API

- 主要分为 3 类：

  1.  连接数据库。   
      - API文档中，所有以 Dial 开头。
  2.  操作数据库。   
      - Do() 函数【推荐】;  Send()函数, 需要配合Flush()、Receive() 3 个函数使用。
  3.  返回helper。   
      - 相当于 “类型断言”。根据使用的具体数据类型，选择调用。

- 添加测试案例：

  ```go
  package main
  
  import (
  	"github.com/gomodule/redigo/redis"
  	"fmt"
  )
  
  func main()  {
  	// 1. 链接数据库
  	conn, err := redis.Dial("tcp", "192.168.6.108:6379")
  	if err != nil {
  		fmt.Println("redis Dial err:", err)
  		return
  	}
  	defer conn.Close()
  
  	// 2. 操作数据库
  	reply, err := conn.Do("set", "itcast", "itheima")
  
  	// 3. 类型断言类函数. ---- 确定成具体的数据类型
  	r, e := redis.String(reply, err)
  
  	fmt.Println(r, e)
  }
  ```

  