

1. 启动server

```
uvicorn calculate-bmi-server:app --host localhost --port 9000
```

启动命令里是的calculate-bmi-server就是py文件名，app就是代码里的 app = Starlette这一段。


2. 使用浏览器访问，ip:端口/sse



3. 在cherry studio配置sse接口

![img.png](img.png)

4. 对话
![img_1.png](img_1.png)

server日志打印
![img_2.png](img_2.png)


# 参考资料：
https://zhuanlan.zhihu.com/p/1890120742873568319