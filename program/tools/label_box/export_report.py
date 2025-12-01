#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
导出标签统计报告
"""

def export_statistics(output_base, mmdd, total_expected, total_copied, missing_map, missing_details=None):
    """
    导出标签统计报告到文件
    
    参数:
        output_base: 输出目录
        mmdd: 日期标识
        total_expected: 应该生成的标签数
        total_copied: 已生成的标签数
        missing_map: 缺少的标签映射
        missing_details: 缺少标签的详细信息（可选）
    
    返回:
        报告文件路径
    """
    from pathlib import Path
    import os
    
    output_base = Path(output_base)
    total_missing = len([id for ids in missing_map.values() for id in ids])
    report_path = output_base / f"标签统计_{mmdd}.txt"
    
    # 确保输出目录存在
    os.makedirs(output_base, exist_ok=True)
    
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("标签处理统计报告\n")
            f.write(f"生成时间：{mmdd}\n")
            f.write(f"应该生成：{total_expected} 个\n")
            f.write(f"已生成：{total_copied} 个\n")
            f.write(f"缺少：{total_missing} 个\n")
            f.write("=" * 80 + "\n\n")
            
            if total_missing > 0:
                f.write("缺少的标签详情：\n\n")
                
                # 优先使用 missing_details
                if missing_details:
                    for sheet, details_list in missing_details.items():
                        if details_list:
                            f.write(f"【{sheet}】\n")
                            for i, detail in enumerate(details_list, 1):
                                sku = detail.get('sku', '')
                                e_val = detail.get('e_val', '')
                                f.write(f"{i}. SKU: {sku}")
                                if e_val:
                                    f.write(f" ({e_val})")
                                f.write("\n")
                            f.write("\n")
                else:
                    # 使用 missing_map
                    for sheet, missing_ids in missing_map.items():
                        if missing_ids:
                            f.write(f"【{sheet}】\n")
                            for i, mid in enumerate(missing_ids, 1):
                                f.write(f"{i}. {mid}\n")
                            f.write("\n")
            else:
                f.write("所有标签都已成功生成！\n")
        
        return str(report_path)
    except Exception as e:
        # 即使出错，也要生成一个空文件作为标记
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"[错误] 导出统计报告失败：{e}\n")
        except:
            pass
        raise Exception(f"导出统计报告失败：{e}")
