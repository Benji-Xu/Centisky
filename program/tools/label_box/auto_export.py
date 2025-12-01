#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动导出统计报告 - 在处理完成后自动生成
"""
import os
from pathlib import Path


def auto_export_after_process(output_base, mmdd, total_expected, total_copied, missing_map):
    """
    在处理完成后自动导出统计报告
    这个函数会被 main.py 调用
    """
    try:
        output_base = Path(output_base)
        report_path = output_base / f"标签统计_{mmdd}.txt"
        
        # 确保目录存在
        os.makedirs(output_base, exist_ok=True)
        
        # 计算缺少的数量
        total_missing = len([id for ids in missing_map.values() for id in ids])
        
        # 调试：打印 missing_map 的内容
        print(f"[DEBUG] missing_map: {missing_map}")
        print(f"[DEBUG] total_missing: {total_missing}")
        
        # 写入文件
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("标签处理统计报告\n")
            f.write(f"生成时间：{mmdd}\n")
            f.write(f"应该生成：{total_expected} 个\n")
            f.write(f"已生成：{total_copied} 个\n")
            f.write(f"缺少：{total_missing} 个\n")
            f.write("=" * 80 + "\n\n")
            
            # 调试信息
            f.write(f"[DEBUG] missing_map 内容：{missing_map}\n")
            f.write(f"[DEBUG] missing_map 类型：{type(missing_map)}\n")
            f.write(f"[DEBUG] missing_map 长度：{len(missing_map)}\n\n")
            
            if total_missing > 0:
                f.write("缺少的标签详情：\n\n")
                has_details = False
                for sheet, missing_ids in missing_map.items():
                    if missing_ids:
                        has_details = True
                        f.write(f"【{sheet}】\n")
                        for i, mid in enumerate(missing_ids, 1):
                            # mid 可能是空字符串，使用行号代替
                            display_id = mid if mid and mid.strip() else f"(未知行{i})"
                            f.write(f"{i}. {display_id}\n")
                        f.write("\n")
                
                if not has_details:
                    f.write("（缺少的标签ID信息未能获取，请查看日志）\n")
            else:
                f.write("所有标签都已成功生成！\n")
        
        return str(report_path)
    except Exception as e:
        print(f"导出失败：{e}")
        return None
