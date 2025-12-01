# 🔧 唯品会开票工具 - 红冲负数修复

**完成日期**：2024年12月1日  
**改进者**：Benjamin  
**状态**：✅ 完成

---

## 📋 改进说明

### 问题描述
唯品会处理发票时，如果是红冲单据，单价和金额需要改为负数，以符合开票系统的标准要求。

### 解决方案
修改 `program/tools/invoice_processor/main.py` 中的红冲处理逻辑，当检测到红冲时，自动将单价和金额转换为负数。

---

## 🔍 具体改动

### 文件
`program/tools/invoice_processor/main.py`

### 位置
第 540-543 行

### 代码变更

```python
# 添加的代码（第 540-543 行）
# 红冲时单价和金额改为负数
if is_red_invoice:
    unit_price = -unit_price
    amt_f = -amt_f
```

### 注释更新

```python
# 第 560 行
unit_price,            # 单价（含税）- 红冲时为负数

# 第 562 行
amt_f,                 # 金额（含税）- 红冲时为负数
```

---

## 📊 处理流程

```
检测红冲标记
    ↓
is_red_invoice = True
    ↓
计算单价和金额
    ↓
红冲时转换为负数
    ↓
unit_price = -unit_price
amt_f = -amt_f
    ↓
导出到 Excel
```

---

## ✅ 验证方法

### 测试步骤

1. **打开开票工具**
   ```bash
   start.bat
   # 选择开票工具
   ```

2. **选择包含红冲标记的唯品会表格**
   - 选择 Excel 文件
   - 确保表格中有红冲标记的行

3. **处理发票**
   - 点击"处理发票"按钮
   - 等待处理完成

4. **验证导出文件**
   - 打开导出的 Excel 文件
   - 查看红冲行的数据：
     - 单价列：应该是负数（如 -100.00）
     - 金额列：应该是负数（如 -500.00）
     - 备注列：应该显示"红冲"

### 验证示例

```
原始数据：
- 单价：100.00
- 金额：500.00
- 红冲标记：是

导出后（红冲）：
- 单价：-100.00 ✅
- 金额：-500.00 ✅
- 备注：红冲 ✅

导出后（非红冲）：
- 单价：100.00 ✅
- 金额：500.00 ✅
- 备注：（空） ✅
```

---

## 🎯 改进的好处

✅ **符合开票系统标准**
- 红冲单据的单价和金额必须是负数
- 自动处理，减少手动修改

✅ **提高工作效率**
- 无需手动修改负数
- 自动化处理，一键完成

✅ **减少错误**
- 避免手动修改导致的错误
- 确保数据准确性

✅ **用户体验更好**
- 导出的文件可以直接使用
- 无需额外处理

---

## 📝 相关代码

### 红冲检测逻辑
```python
# 第 519-524 行
is_red_invoice = False
if (is_red_text == "是") or ("红冲" in rc_text and "非红冲" not in rc_text):
    is_red_invoice = True
elif str(tax_id).strip():
    invoice_type = "普票"
```

### 负数转换逻辑
```python
# 第 540-543 行
# 红冲时单价和金额改为负数
if is_red_invoice:
    unit_price = -unit_price
    amt_f = -amt_f
```

### 数据行构建
```python
# 第 545-564 行
row = [
    invoice_type,          # 发票类型（必须填写）
    "",                    # 发票号（冲红需填写）
    date_str,              # 开票日期
    str(order_no or ""),  # 订单号
    str(title or ""),     # 客户名称
    str(tax_id or ""),    # 客户税号
    "",                   # 客户地址
    "",                   # 客户电话
    "",                   # 开户银行
    "",                   # 银行账号
    "无人机",             # 货物名称
    "",                   # 规格型号
    "台",                 # 单位
    qty,                   # 数量
    unit_price,            # 单价（含税）- 红冲时为负数
    "",                   # 税率
    amt_f,                 # 金额（含税）- 红冲时为负数
    "红冲" if is_red_invoice else "",  # 备注（红冲时写"红冲"）
]
```

---

## 🔄 完整的红冲处理流程

### 第 1 步：检测红冲标记
```python
rc_status = ws.cell(row=r, column=col("红冲状态")).value
is_red = ws.cell(row=r, column=col("是否红冲")).value
rc_text = str(rc_status).strip() if rc_status is not None else ""
is_red_text = str(is_red).strip() if is_red is not None else ""
```

### 第 2 步：判断是否红冲
```python
is_red_invoice = False
if (is_red_text == "是") or ("红冲" in rc_text and "非红冲" not in rc_text):
    is_red_invoice = True
```

### 第 3 步：计算单价和金额
```python
amt_f = float(amount) if amount not in (None, "") else 0.0
unit_price = amt_f / qty_f if qty_f else amt_f
unit_price = round(unit_price, 2)
```

### 第 4 步：红冲时转换为负数
```python
if is_red_invoice:
    unit_price = -unit_price
    amt_f = -amt_f
```

### 第 5 步：构建数据行
```python
row = [
    ...,
    unit_price,            # 单价（含税）- 红冲时为负数
    ...,
    amt_f,                 # 金额（含税）- 红冲时为负数
    "红冲" if is_red_invoice else "",  # 备注
]
```

---

## 📋 改进清单

| 项目 | 状态 | 说明 |
|------|------|------|
| 红冲检测 | ✅ | 正确识别红冲标记 |
| 单价转负数 | ✅ | 红冲时自动转换 |
| 金额转负数 | ✅ | 红冲时自动转换 |
| 备注标记 | ✅ | 备注列显示"红冲" |
| 代码注释 | ✅ | 清晰的代码注释 |

---

## 🎉 总结

✅ **改进完成**：红冲时单价和金额自动转换为负数  
✅ **符合标准**：符合开票系统的标准要求  
✅ **自动化**：无需手动修改，一键完成  
✅ **准确性**：减少错误，提高数据准确性  

---

**改进完成日期**：2024年12月1日  
**改进者**：Benjamin  
**版本**：1.0.1  
**状态**：✅ 完成并验证
