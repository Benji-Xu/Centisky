# -*- coding: utf-8 -*-
"""
螺旋桨配置文件
用于管理螺旋桨商品编号与PLD文件的映射关系
"""

import json
from pathlib import Path

# 默认的螺旋桨映射表（向后兼容）
_DEFAULT_PROPELLER_MAP = {
    "100181107889": "外星人螺旋桨.pld",
    "100235985474": "三只梨螺旋桨.pld", 
    "100264779838": "兽螺旋桨.pld",
    "100144781118": "901螺旋桨.pld",
    "100131174559": "909螺旋桨.pld",
}

# 初始化静态螺旋桨映射表
STATIC_PROPELLER_MAP = _DEFAULT_PROPELLER_MAP.copy()

# 自动从 propeller_mappings.json 加载映射
def _load_mappings_from_json():
    """在模块加载时自动从JSON文件加载映射"""
    global STATIC_PROPELLER_MAP
    try:
        json_path = Path(__file__).parent / "propeller_mappings.json"
        if json_path.exists():
            with open(json_path, 'r', encoding='utf-8') as f:
                loaded_map = json.load(f)
            # 合并：JSON文件中的映射优先级更高
            STATIC_PROPELLER_MAP.update(loaded_map)
            return True
    except Exception as e:
        pass
    return False

# 在模块加载时自动加载JSON映射
_load_mappings_from_json()

# 螺旋桨识别关键词（用于自动发现PLD文件）
PROPELLER_KEYWORDS = [
    "螺旋桨", "propeller", "螺桨", "螺旋奖", "螺施桨"
]

# 店铺前缀映射（用于按店铺匹配螺旋桨文件）
SHOP_PREFIXES = [
    "外星人", "三只梨", "兽", "901", "909"
]

# 工作表到店铺的映射
SHEET_TO_SHOP_MAP = {
    "外仓库配货表": "外星人",
    "梨配货表": "三只梨", 
    "兽仓库配货表": "兽",
    "兽无人机拆1": "兽",
    "兽无人机拆2": "兽",
}

def add_propeller_mapping(product_code, pld_filename):
    """
    添加新的螺旋桨映射
    
    参数:
        product_code: 商品编号
        pld_filename: PLD文件名
    """
    STATIC_PROPELLER_MAP[product_code] = pld_filename
    print(f"已添加螺旋桨映射：{product_code} -> {pld_filename}")

def remove_propeller_mapping(product_code):
    """
    移除螺旋桨映射
    
    参数:
        product_code: 商品编号
    """
    if product_code in STATIC_PROPELLER_MAP:
        removed = STATIC_PROPELLER_MAP.pop(product_code)
        print(f"已移除螺旋桨映射：{product_code} -> {removed}")
        return True
    return False

def get_all_mappings():
    """
    获取所有螺旋桨映射
    
    返回:
        字典形式的所有映射
    """
    return STATIC_PROPELLER_MAP.copy()

def save_mappings_to_file(filepath):
    """
    将映射保存到文件
    
    参数:
        filepath: 保存路径
    """
    import json
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(STATIC_PROPELLER_MAP, f, ensure_ascii=False, indent=2)
    print(f"映射已保存到：{filepath}")

def load_mappings_from_file(filepath):
    """
    从文件加载映射
    
    参数:
        filepath: 文件路径
    """
    import json
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            loaded_map = json.load(f)
        STATIC_PROPELLER_MAP.update(loaded_map)
        print(f"已从文件加载 {len(loaded_map)} 个映射")
        return True
    except Exception as e:
        print(f"加载映射文件失败：{e}")
        return False
