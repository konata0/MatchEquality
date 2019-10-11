# MatchEquality
移动火柴使等式成立的小游戏

## 环境
本程序采用Python3.6编写，使用的UI界面为Pyqt5，使用到的包为：sys，Pyqt5，json  
其中Pyqt5需要单独安装，其余两个包均可直接导入  
直接运行MatchEquality.exe即可，运行时确保MatchEquality.exe与data文件夹在同一目录下且data文件夹内容完整  

## UI说明
左上方大部分区域用于显示题目和答案的图片  
右侧为题库，根据移动1根或是2根火柴，是否为等式，两两组合，一共四个题库，点击题目即可选择题目  
下方为各编辑框和按钮：  
作答：  
	验证输入的等式是否为当前题目的答案之一  
添加到当前题库：  
	对输入的题目进行验证，符合要求则添加进当前题库  
由等式生成题目：  
	由当前等式反向生成符合题库要求的题目，此后可选择是否将其添加进题库  
显示解答/上一解答/下一解答：  
	显示当前题目的答案，多解问题可点击“上一解答”“下一解答”进行查看  
清除题库：  
	清除题库内容（不可恢复！！！）  
移动1根火柴/移动2根火柴/非等式/等式：  
	对题库进行选择的按钮  

## 输入
要求输入两位数以内的两个非负数的加减乘法，结果也限制为两位数的非负数，乘法符号使用“```*```”，如：  
5+9=11  
3```*```3=15  
6-9=11  

## 规则说明
为了程序和算术表达式的规范性，本程序对数字和火柴的移动规则作了如下规定：  
1.等式中各个数字限定为0到99的非负正整数  
2.数字之前不可添0，如“06”为非法数字  
3.移动两根火柴不包含无意义的操作（如A移一根火柴至B，B移一根火柴至C，而B最后未改变，将此视为无意义的操作，等效于将A一根火柴移到C的一根火柴移动操作）  
4.“=”和“-”的横高度不一致，禁止将“=”减少一根火柴视为“-”  

## 文件说明
MatchEquality.py：Python源文件  
MatchEquality.exe：打包发布的可执行程序  
data/img：显示火柴使用的图片  
data/move.json：有关火柴移动规则的数据文件  
data/rule.json：有关火柴移动规则的数据文件  
data/question.json：题库数据文件  
data/getMove.js：生成火柴移动规则的相关js代码






