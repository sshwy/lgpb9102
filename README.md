# Luogu冬日绘板2019自动化脚本

[更多介绍](https://sshwy.gitee.io/2018/12/30/42654/)

# 使用

请在`cookies.txt`中用以下格式存放cookie
``` plain
UM_id client_id _uid
UM_id client_id _uid
...

```
在源码中可以指定图片的左上角坐标，修改`base_x base_y`即可
# 关于图片

请首先将图片转换为`ppm`格式，然后可以参考`ppm2Luogupaint.cpp`的代码，将PPM转化为luoguPaintBoard友好的格式（记得删除PPM的注释），**建议使用GIMP**

然后修改源码中的文件名就好了

请使用`python3`，并确保安装`requests`库

# 支持

透明背景