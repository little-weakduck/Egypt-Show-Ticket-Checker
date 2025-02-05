# Egypt-Show-Ticket-Checker
上海博物馆埃及展检查是否有票的爬虫，并通过 Bark 发送通知到你的手机。

## 先决条件

在运行此脚本之前，请确保已安装以下软件：

- Python 3+

## 安装

1. 克隆此仓库到你的本地机器：

    ```bash
    git clone https://github.com/yourusername/egypt-show-ticket-checker.git
    cd egypt-show-ticket-checker
    ```

2. 安装所需的 Python 库：

## 配置

在运行脚本之前，请根据你的需求修改 [EgyptShowTicket.py](http://_vscodecontentref_/1) 文件中的以下配置：

- [dates](http://_vscodecontentref_/2): 想要蹲票的时间，按照 `YYYY-MM-DD` 的形式写。
- [device_codes](http://_vscodecontentref_/3): Bark 发送通知的设备号。
- [mpsessid](http://_vscodecontentref_/4): 用于鉴权的 [mpsessid](http://_vscodecontentref_/5)。
- [ticket_num](http://_vscodecontentref_/6): 需要的票的数量，小于这个数量的票，认为他没票。

## 运行

运行以下命令启动脚本：

```bash
python EgyptShowTicket.py
```

## 日志

脚本会输出日志信息到控制台，以便你监控脚本的运行情况。

## 许可证

此项目使用 MIT 许可证。详情请参阅 LICENSE 文件。

