import streamlit as st

# 设置页面标题
st.title("我的图片相册")

# 准备图片数据：列表中每个元素是(图片路径, 图注)
# 注意：请将这里的图片路径替换为你本地的图片路径，或使用网络图片URL
image_data = [
    ("D:/sssss_env/阿德利企鹅.png", "向日葵美女"),
    ("D:/sssss_env/巴布亚企鹅.png", "开心美女"),
    ("D:/sssss_env/帽带企鹅.png", "大山")
]

# 初始化会话状态，记录当前显示的图片索引
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0

# 定义切换图片的函数
def prev_image():
    st.session_state.current_idx = (st.session_state.current_idx - 1) % len(image_data)

def next_image():
    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(image_data)

# 显示当前图片和图注
current_img, current_caption = image_data[st.session_state.current_idx]
st.image(current_img, caption=current_caption, width=600)

# 按钮布局：上一张 + 下一张
col1, col2 = st.columns(2)
with col1:
    st.button("上一张", on_click=prev_image)
with col2:
    st.button("下一张", on_click=next_image)
