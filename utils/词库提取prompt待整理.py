#苏泊尔水壶的
##这种prompt是能够得到统一格式的
main_product="水壶Kettle"
category="地点、装饰风格、氛围、光强、光源方向、主体产品视角、主体产品位置、主体产品细节、其他物品、背景、背景清晰度、窗外风景"
eg="""
office scenario地点  
bedroom地点  
minimalistic modern home style装饰风格  
warm tone氛围  
light color氛围  
evening ambiance氛围  
bright atmosphere光强  
light from the left side光源方向  
eye-level view主体产品视角  
side view主体产品视角  
Kettle on a side table主体产品位置  
Kettle on kitchen countertop主体产品位置  
white ribbed electric kettle with silver accents and white plastic handle主体产品细节  
grey electric kettle主体产品细节  
two glass mugs with drinks on beige plate其他物品  
porcelain teacup with saucer其他物品  
cream-colored coffee maker in the background背景  
blurred background背景清晰度  
scenic outdoor view through window窗外风景  
"""

prompt=f"""
主体产品是{main_product}。
每行的英文词组————tag是需要判断分类的的内容，请输出一种类别（{category}）在英文词组的后面。中间用一个tab制表符隔开。
输出的格式：
Engligh tag   对应的类别
尝试根据"```"包围的文字中，归纳分类标准，并进行分类。
一些分类案例如下：
```
{eg}
```
"""
##对应的excel文件表头：
categories = {
        '其他物品': [],
        '主体产品细节': [],
        '主体产品位置': [],
        '窗外风景': [],
        '背景': [],
        '氛围': [],
        '地点': [],
        '装饰风格': [],
        '光源方向': [],
        '背景清晰度': [],
        '主体产品视角': [],
        '光强': []
    }

#####乐屋
purpose="房间布置分析"
category="风格，地点，产品主体，产品位置，装饰物，其它物品，地面物品，挂件，墙壁地面，窗外风景，范围"
eg="""
Dopamine-style风格  
kitchen地点  
Kettle on a side table主体产品位置  
Kettle on kitchen countertop主体产品位置  
white ribbed electric kettle with silver accents and white plastic handle主体产品细节  
grey electric kettle主体产品细节  
two glass mugs with drinks on beige plate其他物品  
porcelain teacup with saucer其他物品  
"""
