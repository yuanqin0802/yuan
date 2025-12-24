import streamlit as st
from datetime import datetime
from PIL import Image
import io
import base64

# 页面配置
st.set_page_config(
    page_title="个人简历生成器",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 设置深色主题样式
st.markdown("""
<style>
    /* 主背景和字体颜色 */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* 表单容器样式 */
    .form-container {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    
    /* 预览容器样式 */
    .preview-container {
        background-color: #1E1E1E;
        padding: 30px;
        border-radius: 10px;
        border: 1px solid #333;
        height: 100%;
    }
    
    /* 简历标题样式 */
    .resume-title {
        color: #4A90E2;
        border-bottom: 2px solid #4A90E2;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* 个人信息样式 */
    .personal-info {
        display: flex;
        align-items: center;
        margin-bottom: 30px;
    }
    
    .avatar-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #4A90E2;
        margin-right: 20px;
    }
    
    .info-details h2 {
        margin: 0;
        color: #FFFFFF;
    }
    
    .info-details p {
        margin: 5px 0;
        color: #CCCCCC;
    }
    
    /* 技能标签样式 */
    .skill-tag {
        display: inline-block;
        background-color: #2D2D2D;
        color: #4A90E2;
        padding: 5px 15px;
        border-radius: 20px;
        margin: 5px;
        font-size: 0.9em;
    }
    
    /* 节目标题样式 */
    .section-title {
        color: #4A90E2;
        margin-top: 20px;
        margin-bottom: 10px;
        padding-bottom: 5px;
        border-bottom: 1px solid #333;
    }
    
    /* 调整输入框样式 */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: #2D2D2D;
        color: #FAFAFA;
        border: 1px solid #444;
    }
    
    /* 调整滑块样式 */
    .stSlider {
        color: #4A90E2;
    }
    
    /* 上传区域样式 */
    .uploadedFile {
        background-color: #2D2D2D;
    }
    
    /* 隐藏默认的Streamlit标记 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 响应式调整 */
    @media (max-width: 768px) {
        .personal-info {
            flex-direction: column;
            text-align: center;
        }
        .avatar-img {
            margin-right: 0;
            margin-bottom: 15px;
        }
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'avatar' not in st.session_state:
    st.session_state.avatar = None
if 'user_info' not in st.session_state:
    st.session_state.user_info = {
        'name': '陆紫光',
        'position': '软件测试',
        'phone': '17677169536',
        'email': '237917611@qq.com',
        'birthdate': '2025-06-07',
        'gender': '男',
        'education': '本科',
        'languages': ['中文', '英语'],
        'skills': ['Java', 'HTML/CSS', '机器学习', 'Python'],
        'experience': 0,
        'salary_min': 5000,
        'salary_max': 23130,
        'bio': """陆紫光，本科和研究生专业均为信息安全专业，主要研究内容为机器学习与信息安全，现为广西职业师范学院专任教师(讲师)、广西职业师范学院前沿交叉学科创新研究中心委员、广西职业师范学院前沿交叉学科创新研究中心委员、广西职业师范学院计算机与信息工程学院金宇算法工作负责人、广西职业师范学院智能编码社团指导老师，广西职业师范学院计算机与信息工程学院专业学科竞赛负责人。公开发表学术论文15篇，主持完成了大学生创新创业实践项目25项(区级立项)，4家校企合作，7项外包项目。4项新文科院角下的工具与平台研发。""",
        'best_time': '20:41'
    }

# 主标题
st.title("个人简历生成器")
st.markdown("### 使用Streamline创建的个性化简历")

# 创建两列布局
col1, col2 = st.columns([1, 1], gap="large")

# 左侧：个人信息表单
with col1:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown("### 📋 个人信息表单")
    
    # 基本信息输入
    name = st.text_input("姓名", value=st.session_state.user_info['name'])
    position = st.text_input("职位", value=st.session_state.user_info['position'])
    phone = st.text_input("电话", value=st.session_state.user_info['phone'])
    email = st.text_input("邮箱", value=st.session_state.user_info['email'])
    birthdate = st.date_input("出生日期", 
                             value=datetime.strptime(st.session_state.user_info['birthdate'], '%Y-%m-%d'),
                             format="YYYY/MM/DD")
    
    # 性别和学历
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        gender = st.selectbox("性别", ["男", "女"], index=0 if st.session_state.user_info['gender'] == "男" else 1)
    with col1_2:
        education = st.selectbox("学历", ["大专", "本科", "硕士", "博士"], index=1)
    
    # 语言能力（多选）
    languages = st.multiselect(
        "语言能力",
        ["中文", "英语", "日语", "韩语", "法语", "德语", "西班牙语"],
        default=st.session_state.user_info['languages']
    )
    
    # 技能（多选）
    skills = st.multiselect(
        "技能",
        ["Java", "Python", "JavaScript", "HTML/CSS", "机器学习", "深度学习", 
         "数据分析", "SQL", "React", "Vue", "Docker", "Kubernetes"],
        default=st.session_state.user_info['skills']
    )
    
    # 工作经验滑块
    experience = st.slider("工作经验（年）", 0, 30, st.session_state.user_info['experience'])
    
    # 薪资范围
    salary_min, salary_max = st.slider(
        "薪资范围（元）",
        0, 50000,
        (st.session_state.user_info['salary_min'], st.session_state.user_info['salary_max'])
    )
    
    # 个人简介
    bio = st.text_area(
        "个人简介",
        value=st.session_state.user_info['bio'],
        height=150
    )
    
    # 每日最佳联系时间段
    best_time = st.selectbox(
        "每日最佳联系时间段",
        ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", 
         "16:00", "17:00", "18:00", "19:00", "20:00", "20:41", "21:00", "22:00"],
        index=12
    )
    
    # 上传个人照片
    st.markdown("### 上传个人照片")
    uploaded_file = st.file_uploader(
        "Drag and drop file here",
        type=['jpg', 'jpeg', 'png'],
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.session_state.avatar = image
        st.success("图片上传成功！")
        st.image(image, width=150)
    else:
        st.info("请上传个人照片 (.JPG, .JPEG, .PNG)")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 更新按钮
    if st.button("🔄 更新简历预览", type="primary", use_container_width=True):
        st.session_state.user_info.update({
            'name': name,
            'position': position,
            'phone': phone,
            'email': email,
            'birthdate': birthdate.strftime('%Y-%m-%d'),
            'gender': gender,
            'education': education,
            'languages': languages,
            'skills': skills,
            'experience': experience,
            'salary_min': salary_min,
            'salary_max': salary_max,
            'bio': bio,
            'best_time': best_time
        })
        st.success("简历信息已更新！")

# 右侧：简历预览
with col2:
    st.markdown('<div class="preview-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="resume-title">个人简历</h1>', unsafe_allow_html=True)
    
    # 个人信息区域
    st.markdown('<div class="personal-info">', unsafe_allow_html=True)
    
    # 显示头像
    if st.session_state.avatar:
        st.image(st.session_state.avatar, width=120, caption="")
    else:
        # 显示默认头像
        st.markdown('<div style="width:120px; height:120px; border-radius:50%; background-color:#2D2D2D; display:flex; align-items:center; justify-content:center; border:3px solid #4A90E2; margin-right:20px;">'
                   '<span style="color:#666; font-size:14px;">头像</span></div>', unsafe_allow_html=True)
    
    # 个人信息详情
    st.markdown("""
    <div class="info-details">
        <h2>{name}</h2>
        <p style="color:#4A90E2; font-size:18px; font-weight:bold;">{position}</p>
        <p>📱 {phone} | ✉️ {email}</p>
        <p>🎂 {birthdate} | 👤 {gender} | 🎓 {education}</p>
    </div>
    """.format(
        name=st.session_state.user_info['name'],
        position=st.session_state.user_info['position'],
        phone=st.session_state.user_info['phone'],
        email=st.session_state.user_info['email'],
        birthdate=st.session_state.user_info['birthdate'],
        gender=st.session_state.user_info['gender'],
        education=st.session_state.user_info['education']
    ), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 个人简介部分
    st.markdown('<h3 class="section-title">个人简介</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#CCCCCC; line-height:1.6;">{st.session_state.user_info["bio"]}</p>', unsafe_allow_html=True)
    
    # 语言能力
    st.markdown('<h3 class="section-title">语言能力</h3>', unsafe_allow_html=True)
    languages_html = " ".join([f'<span class="skill-tag">{lang}</span>' for lang in st.session_state.user_info["languages"]])
    st.markdown(languages_html, unsafe_allow_html=True)
    
    # 专业技能
    st.markdown('<h3 class="section-title">专业技能</h3>', unsafe_allow_html=True)
    skills_html = " ".join([f'<span class="skill-tag">{skill}</span>' for skill in st.session_state.user_info["skills"]])
    st.markdown(skills_html, unsafe_allow_html=True)
    
    # 工作经验
    st.markdown('<h3 class="section-title">工作经验</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#CCCCCC;">{st.session_state.user_info["experience"]} 年</p>', unsafe_allow_html=True)
    
    # 期望薪资
    st.markdown('<h3 class="section-title">期望薪资</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#CCCCCC;">{st.session_state.user_info["salary_min"]} - {st.session_state.user_info["salary_max"]} 元/月</p>', unsafe_allow_html=True)
    
    # 最佳联系时间
    st.markdown('<h3 class="section-title">最佳联系时间段</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#CCCCCC;">每日 {st.session_state.user_info["best_time"]}</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 底部操作按钮
st.markdown("---")
col3, col4, col5 = st.columns([1, 2, 1])
with col4:
    if st.button("💾 导出为PDF", use_container_width=True):
        st.info("PDF导出功能需要额外配置，请安装相关依赖")
    if st.button("🖨️ 打印简历", use_container_width=True):
        st.info("打印功能需要浏览器支持")

# 页脚
st.markdown("""
---
<div style="text-align: center; color: #666; font-size: 0.9em; padding: 20px;">
    <p>© 2024 个人简历生成器 | 使用 Streamlit 构建</p>
</div>
""", unsafe_allow_html=True)
