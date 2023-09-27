import re

text = """物品类别: 腰带
稀 有 度: 稀有
鹰翼 绸带
深渊腰带
--------
需求:
等级: 67
--------
插槽: A 
--------
物品等级: 86
--------
拥有 1 个深渊插槽 (implicit)
--------
+9 护甲
晕眩回复和格挡回复提高 13%
冷却回复速度加快 16%
--------
圣战者物品
--------
出售获得通货:非绑定"""

# 使用正则表达式提取两个分割线之间的多行文本
pattern = r"--------\n(.*?)\n--------"
matches = re.findall(pattern, text, re.DOTALL)

print(matches[1])