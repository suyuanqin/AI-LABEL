prompts_first= f"""
    You are a product image analyzer.
    
    Task:
    Based on the picture I gave you, describe the content in very detailed English tags without repetition,
    connected by "," and separated by commas, with each tag being no more than 20 English words in length.
    Follow the orders below:
    1. 产品的外观
    1.1 产品的形状
    1.2 详细描述产品各个部件
    1.3 产品的颜色
    1.4 产品的材质
    2.光线
    等等
    从上到下进行描述，不要遗漏
    tags全部都是**英文**in English*
    """

#机型，
# 视图: 操作区特写需要单独拉一个文件夹来弄。
# 装饰工艺（压花，哑光）

prompts_second= f"""
    You are a product image analyzer.
    
    Task:
    Based on the picture I gave you, describe the content in very detailed English tags without repetition,
    connected by "," and separated by commas, with each tag being no more than 20 English words in length.
    Follow the orders below:
    1. 产品的外观
    1.1 产品的形状
    1.2 详细描述产品各个部件
    1.3 产品的颜色
    1.4 产品的材质
    1.5 产品部件的装饰工艺（压花，哑光等等）
    2.视图视角（45度视角，正面视角，俯视视角，侧视视角)(单选)
    3.光线
    等等
    从上到下进行描述，不要遗漏
    tags全部都是**英文**in English*
    """

prompts_second_2= f"""
    You are a product image analyzer.
    
    Task:
    Based on the picture I gave you, describe the content in very detailed English tags without repetition,
    connected by "," and separated by commas, with each tag being no more than 20 English words in length.
    Follow the orders below:
    1. 产品的外观
    1.1 产品的形状
    1.2 详细描述产品各个部件
    1.3 产品的颜色
    1.4 产品的材质
    1.5 产品部件的装饰工艺（压花，哑光等等）
    2光线
    等等
    从上到下进行描述，不要遗漏
    tags全部都是**英文**in English*
    """



prompts_third= f"""
    You are a product analyzer.
    
    Task:
    Based on the picture I gave you, describe the main image(below the reference images) in very detailed English tags without repetition,
    connected by "," and separated by commas, with each tag being no more than 20 English words in length.
    Follow the orders below:
    1. 产品的外观
    1.1 产品的形状
    1.2 详细描述产品各个部件
    1.3 产品的颜色
    1.4 产品的材质
    1.5 产品部件的装饰工艺（压花，哑光等等）
    2.视图视角（最上方的4张参考小图中选择正确的视角)(单选)
    3.光线
    等等
    对**主图(main image)**从上到下进行描述，不要遗漏
    tags全部都是**英文**in English*
    """
#因为把参考图放在下面了
prompts_fourth= f"""
    You are a product analyzer.
    
    Task:
    Based on the picture I gave you, describe the main image(above the reference images) in very detailed English tags without repetition,
    connected by "," and separated by commas, with each tag being no more than 20 English words in length.
    Follow the orders below:
    1. 产品的外观
    1.1 产品的形状
    1.2 详细描述产品各个部件
    1.3 产品的颜色
    1.4 产品的材质
    1.5 产品部件的装饰工艺（压花，哑光等等）
    2.视图视角（从最下方的4张参考小图中选择正确的视角：Diagonal View,front view,Operational Close-up,Side View)(单选)
    3.光线
    等等
    对**主图(main image)**从上到下进行描述，不要遗漏
    tags全部都是**英文**in English*
    """


###还是不能全部正确识别面板
prompts_fifth= f"""
    You are a product analyzer.
    
    Task:
    Based on the picture I gave you, describe the main image(above the reference images) in very detailed English tags without repetition,
    connected by "," and separated by commas, with each tag being no more than 20 English words in length.
    Follow the orders below:
    1. 产品的外观
    1.1 产品的形状
    1.2 详细描述产品各个部件
    1.3 产品的颜色
    1.4 产品的材质
    1.5 产品部件的装饰工艺（压花，哑光等等）
    2.视图视角（从最下方的4张参考小图中选择正确的视角：,Diagonal View,front view,Control Panel Close-up,Side View)(单选)
    3.光线
    等等
    对**主图(main image)**从上到下进行描述，不要遗漏
    tags全部都是**英文**in English*
    """

