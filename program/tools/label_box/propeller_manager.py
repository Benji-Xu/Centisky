# -*- coding: utf-8 -*-
"""
螺旋桨映射管理工具
用于管理和维护螺旋桨商品编号与PLD文件的映射关系
"""

import json
from pathlib import Path
from propeller_config import (
    STATIC_PROPELLER_MAP, 
    add_propeller_mapping, 
    remove_propeller_mapping,
    get_all_mappings,
    save_mappings_to_file,
    load_mappings_from_file
)

class PropellerManager:
    """螺旋桨映射管理器"""
    
    def __init__(self):
        self.config_file = Path(__file__).parent / "propeller_mappings.json"
        self.load_from_file()
    
    def load_from_file(self):
        """从文件加载映射"""
        if self.config_file.exists():
            load_mappings_from_file(str(self.config_file))
    
    def save_to_file(self):
        """保存映射到文件"""
        save_mappings_to_file(str(self.config_file))
    
    def add_mapping(self, product_code, pld_filename):
        """添加新映射"""
        add_propeller_mapping(product_code, pld_filename)
        self.save_to_file()
    
    def remove_mapping(self, product_code):
        """移除映射"""
        result = remove_propeller_mapping(product_code)
        if result:
            self.save_to_file()
        return result
    
    def list_mappings(self):
        """列出所有映射"""
        mappings = get_all_mappings()
        print("\n当前螺旋桨映射：")
        print("-" * 50)
        for code, filename in mappings.items():
            print(f"{code} -> {filename}")
        print(f"\n共 {len(mappings)} 个映射")
        return mappings
    
    def find_unmapped_propellers(self, template_dir):
        """查找未映射的螺旋桨PLD文件"""
        template_path = Path(template_dir)
        if not template_path.exists():
            print(f"模板目录不存在：{template_path}")
            return []
        
        # 查找所有螺旋桨相关的PLD文件
        propeller_files = []
        for pld_file in template_path.rglob("*.pld"):
            filename = pld_file.name
            if any(keyword in filename for keyword in ["螺旋桨", "propeller", "螺桨"]):
                propeller_files.append(filename)
        
        # 检查哪些文件没有映射
        mapped_files = set(get_all_mappings().values())
        unmapped_files = [f for f in propeller_files if f not in mapped_files]
        
        if unmapped_files:
            print(f"\n发现 {len(unmapped_files)} 个未映射的螺旋桨文件：")
            for i, filename in enumerate(unmapped_files, 1):
                print(f"{i}. {filename}")
        else:
            print("\n所有螺旋桨文件都已映射")
        
        return unmapped_files
    
    def interactive_add_mapping(self):
        """交互式添加映射"""
        print("\n=== 添加螺旋桨映射 ===")
        product_code = input("请输入商品编号：").strip()
        if not product_code:
            print("商品编号不能为空")
            return False
        
        pld_filename = input("请输入PLD文件名（包含.pld后缀）：").strip()
        if not pld_filename:
            print("PLD文件名不能为空")
            return False
        
        if not pld_filename.endswith('.pld'):
            pld_filename += '.pld'
        
        # 检查是否已存在
        if product_code in get_all_mappings():
            existing = get_all_mappings()[product_code]
            overwrite = input(f"商品编号 {product_code} 已映射到 {existing}，是否覆盖？(y/N): ").strip().lower()
            if overwrite != 'y':
                print("取消添加")
                return False
        
        self.add_mapping(product_code, pld_filename)
        print(f"✓ 已添加映射：{product_code} -> {pld_filename}")
        return True
    
    def interactive_remove_mapping(self):
        """交互式移除映射"""
        mappings = get_all_mappings()
        if not mappings:
            print("没有可移除的映射")
            return False
        
        print("\n=== 移除螺旋桨映射 ===")
        print("当前映射：")
        codes = list(mappings.keys())
        for i, (code, filename) in enumerate(mappings.items(), 1):
            print(f"{i}. {code} -> {filename}")
        
        try:
            choice = input(f"\n请选择要移除的映射 (1-{len(codes)}) 或输入商品编号：").strip()
            
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(codes):
                    product_code = codes[index]
                else:
                    print("选择无效")
                    return False
            else:
                product_code = choice
                if product_code not in mappings:
                    print(f"商品编号 {product_code} 不存在")
                    return False
            
            confirm = input(f"确认移除 {product_code} -> {mappings[product_code]}？(y/N): ").strip().lower()
            if confirm == 'y':
                self.remove_mapping(product_code)
                print(f"✓ 已移除映射：{product_code}")
                return True
            else:
                print("取消移除")
                return False
                
        except ValueError:
            print("输入无效")
            return False

def main():
    """主程序"""
    manager = PropellerManager()
    
    while True:
        print("\n" + "="*50)
        print("螺旋桨映射管理工具")
        print("="*50)
        print("1. 查看所有映射")
        print("2. 添加新映射")
        print("3. 移除映射")
        print("4. 查找未映射的螺旋桨文件")
        print("5. 退出")
        
        choice = input("\n请选择操作 (1-5): ").strip()
        
        if choice == '1':
            manager.list_mappings()
        
        elif choice == '2':
            manager.interactive_add_mapping()
        
        elif choice == '3':
            manager.interactive_remove_mapping()
        
        elif choice == '4':
            template_dir = input("请输入模板目录路径：").strip()
            if template_dir:
                manager.find_unmapped_propellers(template_dir)
            else:
                print("目录路径不能为空")
        
        elif choice == '5':
            print("退出程序")
            break
        
        else:
            print("无效选择，请重试")

if __name__ == "__main__":
    main()
