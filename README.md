# visitopia-dl

## 关于

一个用于下载 `看理想` 网站免费栏目音频文件的脚本.

## 功能实现

- 单线程下载音频文件
- 检索新内容并下载
- 使用命令行运行脚本

## 使用方法

### 使用

    python visitopia-dl.py [options]

### 参数

    -h | --help 获取帮助
    -u | --url=<节目链接>

### 举例

短参数:

```
$ python visitopia-dl.py -u https://shop.vistopia.com.cn/detail?id=TwTtq
```

长参数:

```
$ python visitopia-dl.py --url=https://shop.vistopia.com.cn/detail?id=TwTtq
```

## Todo

- [x] 单线程下载对应免费栏目音频文件
- [x] 下载新内容
- [x] 命令行参数
- [ ] 断点继续下载
