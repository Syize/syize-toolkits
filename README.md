# syize/一个简单好用的工具箱

里面包含了我在做写代码、画图、处理数据、写论文等等事情的时候用到的脚本，为了方便打包成了 Python 包。

## 安装

通过`pip`或`pip3`安装即可

```
pip3 install syize
```

## 功能

以下功能可以直接在命令行使用。

### `pydiff`

对多个文件计算md5值，并进行对比，检查它们是否相同。写这个功能是因为我在下载高知大学卫星数据时发现每天都需要下载查找表，但是实际上它们是完全一样的。

```bash
# 打印帮助
pydiff -h / --help
# 对比当前文件夹下所有的文件
pydiff --dir .
# 对比多个txt
pydiff 1.txt 2.txt 3.txt
```

### `picture`

将`PDF`文件拆分成图片，以及提取图片中的文字。

```bash
# 将PDF拆分成图片
picture --pdf -i test.pdf -o folder_name
# 还可以指定起始、终止页数，以及图片的dpi
picture --pdf -i test.pdf -o folder_name --pdf-start 3 --pdf-stop 9 --pdf-dpi 1000
# 从图片中提取英文(OCR)，输出到终端
picture --ocr -i test.png
# 也可以提取中文
picture --ocr -i test.png --ocr-text cn
# 将结果输出到文件中
picture --ocr -i test.png -o test.txt
```

### `string`

将一段文字格式化，去除多于的换行符。用来格式化从论文中复制的英文段落，方便粘贴进翻译软件，但是并不好用

```bash
string -i "这是大段的文字" --format
# 也可以输出到文件
string -i "这是大段的文字" --format -o test.txt
```

---

以下是包中包含的其他函数或类，用来在其他代码中导入使用

### `OnResize`

`matplotlib`绘图回调类，用来在改变绘图窗口大小的时候重新设置`colorbar`的宽度和位置。一般你用不到，用函数`prepare_colorbar`。

### `prepare_colorbar`

根据你传入的`fig`和`ax`或者`position`创建一个`colorbar`，并设置好回调函数。用法如下

```python
import numpy as np
import matplotlib.pyplot as plt
from syize import prepare_colorbar

if __name__ == '__main__':
    # prepare figure and axes
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    # generate 30 * 30 data
    data = np.random.randint(0, 10000, 900).reshape(30, 30)
    # plot
    im = ax.imshow(data)
    # create colorbar
    # 你可以通过pad和width设置colorbar距离图片的宽度和自身的宽度
    cax = prepare_colorbar(fig, ax, vertical=True, pad=0.02, width=0.02)
    fig.colorbar(mappable=im, cax=cax)

    plt.show()
```

完美的`colorbar`就此诞生\~

![image-20230907171219539](./pic/image-20230907171219539.png)

你还可以随意调整图像大小，`colorbar`始终会贴合的很好。


https://github.com/Syize/syize-toolkits/assets/44666294/25fc0096-6556-4711-8b3d-942716cbc795


你也可以为多张图片添加共同的`colorbar`

```bash
import numpy as np
import matplotlib.pyplot as plt
from syize import prepare_colorbar

if __name__ == '__main__':
    # prepare figure and axes
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)
    # generate 30 * 30 data
    data = np.random.randint(0, 10000, 900).reshape(30, 30)
    data2 = np.random.randint(0, 10000, 900).reshape(30, 30)
    data3 = np.random.randint(0, 10000, 900).reshape(30, 30)
    data4 = np.random.randint(0, 10000, 900).reshape(30, 30)
    # plot
    im = ax.imshow(data)
    ax2.imshow(data2)
    ax3.imshow(data3)
    ax4.imshow(data4)
    # create colorbar
    # colorbar的创建是基于axes的位置创建的，将所有的ax合起来视作一个整的矩形区域
    # 将该矩形区域四个点的位置以[x0, y0, x1, y1]的顺序传给position参数即可
    cax = prepare_colorbar(fig, position=(ax3.get_position().x0,
                                          ax3.get_position().y0,
                                          ax2.get_position().x1,
                                          ax2.get_position().y1),
                           vertical=True, pad=0.02, width=0.02)
    fig.colorbar(mappable=im, cax=cax)

    plt.show()
```



![image-20230907195214925](./pic/image-20230907195214925.png)
