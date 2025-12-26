import streamlit as st
import pandas as pd

# 页面配置 + 深色主题自定义CSS
st.set_page_config(
    page_title="学生小陆-数字档案",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>
/* 全局深色背景+白色文字 */
.stApp {
    background-color: #000000;
    color: #ffffff;
}
/* 标题/子标题样式 */
h1, h2, h3, h4 {
    color: #ffffff !important;
}
/* 进度条颜色 */
.stProgress > div > div {
    background-color: #4CAF50 !important;
}
/* 表格样式（深色背景+白色文字） */
.dataframe {
    color: #ffffff !important;
    background-color: #1a1a1a !important;
    border: none !important;
}
.dataframe th, .dataframe td {
    border: 1px solid #333333 !important;
}
/* 代码块样式 */
.stCodeBlock {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)


# 1. 标题
st.markdown("# 学生 小陆 - 数字档案")


# 2. 基础信息模块
st.subheader("🔑 基础信息")
info_cols = st.columns(3)
with info_cols[0]:
    st.write("学号: NB-2023-001")
with info_cols[1]:
    st.write("注册时间: 2023-09-01")
with info_cols[2]:
    st.write("<span style='color:green'>精神状态: ✅ 正常</span>", unsafe_allow_html=True)
st.write("进度条: 95% [安全值: 低]")
st.progress(0.95)  # 进度条匹配95%


# 3. 技能矩阵模块
st.subheader("🎯 技能矩阵")
skill_cols = st.columns(3)
with skill_cols[0]:
    st.write("C#")
    st.write("95%")
    st.write("<span style='color:green'>↑ 2%</span>", unsafe_allow_html=True)
with skill_cols[1]:
    st.write("Python")
    st.write("87%")
    st.write("<span style='color:red'>↓ 1%</span>", unsafe_allow_html=True)
with skill_cols[2]:
    st.write("Java")
    st.write("68%")
    st.write("<span style='color:red'>↓ 30%</span>", unsafe_allow_html=True)


# 4. Streamlit课程进度
st.subheader("Streamlit课程进度")
st.progress(0.8)  # 匹配原图进度条填充度


# 5. 任务日志模块
st.subheader("📋 任务日志")
task_data = {
    "日期": ["2023-09-01", "2023-09-05", "2023-09-12"],
    "任务": ["学生数据管理", "课程管理系统", "数据报表展示"],
    "状态": [
        "<span style='color:green'>✅ 完成</span>",
        "<span style='color:orange'>🔴 进行中</span>",
        "<span style='color:red'>❌ 未完成</span>"
    ],
    "难度": ["⭐⭐⭐⭐⭐", "⭐⭐⭐☆☆", "⭐⭐⭐⭐☆"]
}
# 渲染带HTML样式的表格
df_tasks = pd.DataFrame(task_data)
st.write(df_tasks.to_html(escape=False), unsafe_allow_html=True)


# 6. 最新代码成果
st.subheader("💻 最新代码成果")
code_content = """def attack_target():
    if detect_vulnerability():
        exploit()
        print("ACCESS GRANTED")
    else:
        status_redo()
"""
st.code(code_content, language="python")


# 7. 底部系统消息
st.markdown("""
---
<span style='color:green'>SYSTEM MESSAGE: 下一个任务已解锁...</span>
<span style='color:green'>TARGET: 课程管理系统</span>
<span style='color:green'>系统状态: 在线 进度状态: 已完成</span>
""", unsafe_allow_html=True)
