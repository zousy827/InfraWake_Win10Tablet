# InfraWake_Win10Tablet
windows 10  tablet  install infrared sensor  to wake backlight  

需求

1.解决红外识别寄存器的对应关系
2.单步实现程序控制电脑息屏、亮屏、读取红外状态
3.整合成一个独立程序
4.添加开机启动

关键点：
整合过程要解决python程序只能在windows前台运行的问题
python程序的小窗口不美观 不能干掉影响用户体验
将python程序转为windows程序，注册表开机自启
红外亮屏和触摸事件的冲突，红外亮屏不能很短的时间就息屏
要有日志记录和调试方法 部署版本日志不能太详细
不同主机的红外识别的寄存器值不一样，要做特征识别
优化CPU占用率和识别速度

部署：

BIOS按照文档将GPIO77设置为INPUT

在平板电脑上按照TODESK

远程将python安装包和程序test压缩包拷贝到平板电脑

安装python 全部勾选并以管理员

将test解压到C盘根目录

regedit 进入注册表

路径：
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run

增加参数：
ScreenControlService

参数值：
"C:\Windows\System32\cmd.exe" /c start "" "C:\test\dist\test.exe"



