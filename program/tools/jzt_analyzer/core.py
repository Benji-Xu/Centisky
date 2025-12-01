"""
京准通快车数据分析核心模块
"""
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np


def identify_weeks_in_data(file_path):
    """
    识别数据文件中的所有完整周（周一到周日）
    
    参数:
        file_path: Excel/CSV 文件路径
    
    返回:
        weeks_info: [{'week_num': 1, 'start_date': date, 'end_date': date, 'label': '第1周 (10-21 ~ 10-27)'}, ...]
    """
    try:
        # 读取文件
        file_path_obj = Path(file_path)
        file_ext = file_path_obj.suffix.lower()
        
        if file_ext == '.csv':
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(file_path, encoding='gbk')
                except UnicodeDecodeError:
                    df = pd.read_csv(file_path, encoding='utf-8-sig')
        else:
            df = pd.read_excel(file_path)
        
        # 识别日期列
        date_col = df.columns[0]
        
        # 解析日期
        def parse_date(date_value):
            if pd.isna(date_value):
                return pd.NaT
            date_str = str(date_value).strip()
            if len(date_str) == 8 and date_str.isdigit():
                try:
                    return pd.to_datetime(date_str, format='%Y%m%d')
                except:
                    pass
            try:
                return pd.to_datetime(date_value)
            except:
                return pd.NaT
        
        df[date_col] = df[date_col].apply(parse_date)
        df = df.dropna(subset=[date_col])
        
        if len(df) == 0:
            return []
        
        # 按日期排序
        df = df.sort_values(date_col)
        
        # 获取所有日期
        dates = df[date_col].dt.date.unique()
        dates = sorted(dates)
        
        # 识别完整的周（周一到周日）
        weeks = []
        
        # 将日期按周分组
        for date in dates:
            # 获取该日期所在周的周一
            weekday = date.weekday()  # 0=周一, 6=周日
            week_start = date - timedelta(days=weekday)
            
            # 检查该周是否已记录
            if not weeks or weeks[-1]['start'] != week_start:
                weeks.append({
                    'start': week_start,
                    'end': week_start + timedelta(days=6),
                    'dates': []
                })
            
            weeks[-1]['dates'].append(date)
        
        # 筛选出完整的周（有7天数据），按时间从早到晚编号
        complete_weeks = []
        for i, week in enumerate(weeks):
            # 检查该周是否有数据（不一定要7天，但要是连续的）
            if len(week['dates']) >= 1:  # 至少有数据
                complete_weeks.append({
                    'start_date': week['start'],
                    'end_date': week['end'],
                    'data_days': len(week['dates'])
                })

        # 按时间顺序重新编号：第1周 = 最早一周
        for idx, week in enumerate(complete_weeks, start=1):
            week['week_num'] = idx
            week['label'] = f"第{idx}周 ({week['start_date'].strftime('%m-%d')} ~ {week['end_date'].strftime('%m-%d')})"

        return complete_weeks
    
    except Exception as e:
        print(f"识别周数据失败：{e}")
        import traceback
        traceback.print_exc()
        return []


def analyze_kuaiche_data(file_path, week1_num=None, week2_num=None, progress_callback=None, weeks_info=None):
    """
    分析京准通快车数据（两周对比）
    
    参数:
        file_path: Excel/CSV 文件路径
        week1_num: 本周的周编号（从1开始，默认为最近一周）
        week2_num: 对比周的周编号（从1开始，默认为本周的上一周）
        progress_callback: 进度回调函数
    
    返回:
        分析结果字典
    """
    def progress(value, text=None):
        if progress_callback:
            progress_callback(value, text)
    
    try:
        progress(20, "正在读取数据...")
        
        # 根据文件扩展名选择读取方式
        file_path_obj = Path(file_path)
        file_ext = file_path_obj.suffix.lower()
        
        if file_ext == '.csv':
            # 读取 CSV 文件（尝试不同编码）
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(file_path, encoding='gbk')
                except UnicodeDecodeError:
                    df = pd.read_csv(file_path, encoding='utf-8-sig')
        else:
            # 读取 Excel 文件
            df = pd.read_excel(file_path)
        
        # 识别日期列（第一列应该是"点击时间"）
        date_col = df.columns[0]
        
        # 转换日期格式 - 支持多种格式
        def parse_date(date_value):
            """解析多种日期格式"""
            if pd.isna(date_value):
                return pd.NaT
            
            date_str = str(date_value).strip()
            
            # 如果是8位数字格式：20251013
            if len(date_str) == 8 and date_str.isdigit():
                try:
                    return pd.to_datetime(date_str, format='%Y%m%d')
                except:
                    pass
            
            # 尝试标准日期解析
            try:
                return pd.to_datetime(date_value)
            except:
                return pd.NaT
        
        df[date_col] = df[date_col].apply(parse_date)
        
        # 删除无效日期的行
        df = df.dropna(subset=[date_col])
        
        if len(df) == 0:
            return {"success": False, "error": "未找到有效的日期数据"}
        
        # 按日期排序
        df = df.sort_values(date_col)
        
        progress(40, "正在分析周数据...")
        
        # 识别所有周（如果调用方未传入 weeks_info，则在此处识别）
        if weeks_info is None:
            weeks_info = identify_weeks_in_data(file_path)
        
        if len(weeks_info) < 2:
            return {"success": False, "error": "数据中少于2周，无法进行对比"}
        
        # 如果没有指定周编号，使用最近两周（最后两周）
        last_week_num = len(weeks_info)
        prev_week_num = max(1, last_week_num - 1)
        if week1_num is None:
            week1_num = last_week_num  # 最近一周
        if week2_num is None:
            week2_num = prev_week_num  # 上一周
        
        # 验证周编号
        if week1_num > len(weeks_info) or week2_num > len(weeks_info):
            return {"success": False, "error": f"指定的周编号超出范围（共有{len(weeks_info)}周数据）"}
        
        # 获取选中的两周信息
        week1_info = weeks_info[week1_num - 1]
        week2_info = weeks_info[week2_num - 1]
        
        # 定义关键指标列（根据实际列名匹配）
        col_mapping = detect_column_names(df)
        
        # 调试：输出列名映射
        print("识别到的列名映射：")
        for key, col in col_mapping.items():
            print(f"  {key} -> {col}")
        print(f"所有列名：{df.columns.tolist()}")
        print(f"本周：{week1_info['label']}")
        print(f"对比周：{week2_info['label']}")
        
        # 按周筛选数据
        week1_df = df[(df[date_col].dt.date >= week1_info['start_date']) & 
                      (df[date_col].dt.date <= week1_info['end_date'])]
        week2_df = df[(df[date_col].dt.date >= week2_info['start_date']) & 
                      (df[date_col].dt.date <= week2_info['end_date'])]
        
        if len(week1_df) == 0 or len(week2_df) == 0:
            return {"success": False, "error": "选择的周没有数据"}
        
        progress(60, "正在计算指标...")
        
        # 计算汇总数据
        week1_summary = calculate_week_summary(week1_df, col_mapping)
        week2_summary = calculate_week_summary(week2_df, col_mapping)
        
        progress(80, "正在生成对比分析...")
        
        # 计算变化率
        comparison = calculate_comparison(week1_summary, week2_summary)
        
        # 格式化日期范围
        week1_range = f"{week1_info['start_date'].strftime('%Y-%m-%d')} ~ {week1_info['end_date'].strftime('%Y-%m-%d')}"
        week2_range = f"{week2_info['start_date'].strftime('%Y-%m-%d')} ~ {week2_info['end_date'].strftime('%Y-%m-%d')}"
        
        progress(100, "✓ 分析完成！")
        
        return {
            "success": True,
            "weeks_info": weeks_info,  # 所有周信息
            "selected_week1": week1_info,
            "selected_week2": week2_info,
            "summary": {
                "week1_range": week1_range,
                "week2_range": week2_range,
                "week1_cost": week1_summary.get('花费', 0),
                "week1_clicks": week1_summary.get('点击数', 0),
                "week1_impressions": week1_summary.get('展现数', 0),
                "week1_gmv": week1_summary.get('交易额', 0),
                "week1_roi": week1_summary.get('投产比', 0),
                "week2_cost": week2_summary.get('花费', 0),
                "week2_clicks": week2_summary.get('点击数', 0),
                "week2_impressions": week2_summary.get('展现数', 0),
                "week2_gmv": week2_summary.get('交易额', 0),
                "week2_roi": week2_summary.get('投产比', 0),
                "cost_change": comparison.get('花费_变化', 0),
                "clicks_change": comparison.get('点击数_变化', 0),
                "impressions_change": comparison.get('展现数_变化', 0),
                "gmv_change": comparison.get('交易额_变化', 0),
                "roi_change": comparison.get('投产比_变化', 0),
            },
            "comparison": {
                "花费_本周": week1_summary.get('花费', 0),
                "花费_上周": week2_summary.get('花费', 0),
                "花费_变化": comparison.get('花费_变化', 0),
                "点击数_本周": week1_summary.get('点击数', 0),
                "点击数_上周": week2_summary.get('点击数', 0),
                "点击数_变化": comparison.get('点击数_变化', 0),
                "展现数_本周": week1_summary.get('展现数', 0),
                "展现数_上周": week2_summary.get('展现数', 0),
                "展现数_变化": comparison.get('展现数_变化', 0),
                "交易额_本周": week1_summary.get('交易额', 0),
                "交易额_上周": week2_summary.get('交易额', 0),
                "交易额_变化": comparison.get('交易额_变化', 0),
                "投产比_本周": week1_summary.get('投产比', 0),
                "投产比_上周": week2_summary.get('投产比', 0),
                "投产比_变化": comparison.get('投产比_变化', 0),
            },
            "week1_data": week1_df.to_dict('records'),
            "week2_data": week2_df.to_dict('records'),
        }
    
    except Exception as e:
        import traceback
        return {
            "success": False, 
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def detect_column_names(df):
    """
    检测并映射列名（处理各种可能的列名变体）
    
    返回:
        字典映射 {'花费': '实际列名', ...}
    """
    col_mapping = {}
    
    # 定义列名匹配规则（精确匹配优先）
    patterns = {
        '展现数': ['展现数'],
        '点击数': ['点击数'],
        '点击率': ['点击率(%)'],
        '花费': ['花费'],
        '交易额': ['总订单金额', '直接成交金额', '交易额', 'GMV'],
        '订单数': ['直接订单数', '订单数', '直接成交单量'],
        '投产比': ['投产比'],
    }
    
    columns = df.columns.tolist()
    
    # 先尝试精确匹配
    for key, possible_names in patterns.items():
        for name in possible_names:
            if name in columns:
                col_mapping[key] = name
                break
    
    # 如果精确匹配失败，尝试模糊匹配
    for key, possible_names in patterns.items():
        if key in col_mapping:
            continue
        for col in columns:
            col_str = str(col).strip()
            for name in possible_names:
                if name in col_str:
                    col_mapping[key] = col
                    break
            if key in col_mapping:
                break
    
    return col_mapping


def calculate_week_summary(df, col_mapping):
    """
    计算一周的汇总数据
    
    参数:
        df: 数据框（一周的数据）
        col_mapping: 列名映射
    
    返回:
        汇总数据字典
    """
    summary = {}
    
    # 只对映射的数值列进行求和，安全地处理缺失值
    def safe_sum(col_name):
        """安全地对列求和，排除非数值数据"""
        if col_name in df.columns:
            try:
                # 转换为数值类型，强制错误转为 NaN
                return pd.to_numeric(df[col_name], errors='coerce').fillna(0).sum()
            except:
                return 0
        return 0
    
    # 展现数
    if '展现数' in col_mapping:
        summary['展现数'] = safe_sum(col_mapping['展现数'])
    else:
        summary['展现数'] = 0
    
    # 点击数
    if '点击数' in col_mapping:
        summary['点击数'] = safe_sum(col_mapping['点击数'])
    else:
        summary['点击数'] = 0
    
    # 花费
    if '花费' in col_mapping:
        summary['花费'] = safe_sum(col_mapping['花费'])
    else:
        summary['花费'] = 0
    
    # 交易额
    if '交易额' in col_mapping:
        summary['交易额'] = safe_sum(col_mapping['交易额'])
    else:
        summary['交易额'] = 0
    
    # 订单数
    if '订单数' in col_mapping:
        summary['订单数'] = safe_sum(col_mapping['订单数'])
    else:
        summary['订单数'] = 0
    
    # 投产比（ROI）- 如果CSV中有投产比列，使用平均值；否则计算
    if '投产比' in col_mapping:
        # 使用CSV中的投产比列的平均值
        if col_mapping['投产比'] in df.columns:
            try:
                summary['投产比'] = pd.to_numeric(df[col_mapping['投产比']], errors='coerce').fillna(0).mean()
            except:
                summary['投产比'] = 0
        else:
            summary['投产比'] = 0
    elif summary['花费'] > 0:
        # 如果没有投产比列，自己计算
        summary['投产比'] = summary['交易额'] / summary['花费']
    else:
        summary['投产比'] = 0
    
    # 计算点击率
    if summary['展现数'] > 0:
        summary['点击率'] = (summary['点击数'] / summary['展现数']) * 100
    else:
        summary['点击率'] = 0
    
    return summary


def calculate_comparison(week1_summary, week2_summary):
    """
    计算两周的对比数据（变化率）
    
    返回:
        对比数据字典
    """
    comparison = {}
    
    indicators = ['花费', '点击数', '展现数', '交易额', '投产比', '订单数', '点击率']
    
    for indicator in indicators:
        val1 = week1_summary.get(indicator, 0)
        val2 = week2_summary.get(indicator, 0)
        
        # 计算变化率
        if val2 != 0:
            change_rate = ((val1 - val2) / val2) * 100
        else:
            change_rate = 100 if val1 > 0 else 0
        
        comparison[f'{indicator}_变化'] = round(change_rate, 2)
    
    return comparison
