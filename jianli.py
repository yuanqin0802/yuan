import streamlit as st
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
import time

# 页面配置
st.set_page_config(
    page_title="个人简历生成器",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 精确匹配图片中的样式
st.markdown("""
<style>
    /* 主背景 - 深色背景 */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* 主标题样式 */
    .main-header {
        text-align: center;
        color: #FFFFFF;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 5px;
        margin-top: 10px;
    }
    
    .sub-header {
        text-align: center;
        color: #666666;
        font-size: 18px;
        margin-bottom: 40px;
    }
    
    /* 表单容器样式 - 深色卡片 */
    .form-card {
        background-color: #1E1E1E;
        padding: 25px;
        border-radius: 10px;
        border: 1px solid #333333;
        height: 100%;
        margin: 0;
    }
    
    /* 预览容器样式 */
    .preview-card {
        background-color: #1E1E1E;
        padding: 25px;
        border-radius: 10px;
        border: 1px solid #333333;
        height: 100%;
        margin: 0;
    }
    
    /* 表单标题样式 */
    .form-title {
        color: #FFFFFF;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 25px;
        border-bottom: 2px solid #FF4B4B;
        padding-bottom: 10px;
    }
    
    /* 预览标题样式 */
    .preview-title {
        color: #FFFFFF;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 25px;
        border-bottom: 2px solid #FF4B4B;
        padding-bottom: 10px;
    }
    
    /* 输入框标签样式 */
    .stTextInput > label, .stTextArea > label, .stSelectbox > label, .stDateInput > label, .stMultiSelect > label, .stSlider > label {
        color: #CCCCCC !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        margin-bottom: 8px !important;
    }
    
    /* 输入框样式 */
    .stTextInput input, .stTextArea textarea, .stSelectbox select, .stDateInput input, .stMultiSelect input {
        background-color: #2D2D2D !important;
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
        border-radius: 5px !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #FF4B4B !important;
        box-shadow: 0 0 0 1px #FF4B4B !important;
    }
    
    /* 滑块样式 - 红色主题 */
    .stSlider [data-baseweb="slider"] {
        color: #FF4B4B !important;
    }
    
    .stSlider [data-testid="stThumbValue"] {
        color: #FF4B4B !important;
        font-weight: bold !important;
    }
    
    /* 技能标签样式 */
    .skill-tag {
        display: inline-block;
        background-color: #2D2D2D;
        color: #FF4B4B;
        padding: 6px 15px;
        border-radius: 15px;
        margin: 4px;
        font-size: 13px;
        border: 1px solid #444444;
    }
    
    /* 语言标签样式 */
    .language-tag {
        display: inline-block;
        background-color: #2D2D2D;
        color: #4CAF50;
        padding: 6px 15px;
        border-radius: 15px;
        margin: 4px;
        font-size: 13px;
        border: 1px solid #444444;
    }
    
    /* 简历标题 */
    .resume-title {
        color: #FF4B4B;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 30px;
        text-align: center;
        padding-bottom: 15px;
        border-bottom: 3px solid #FF4B4B;
    }
    
    /* 个人简介样式 */
    .bio-text {
        color: #CCCCCC;
        line-height: 1.8;
        font-size: 15px;
        margin-bottom: 25px;
        background-color: #2D2D2D;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #FF4B4B;
    }
    
    /* 个人信息区域 */
    .personal-info {
        display: flex;
        align-items: center;
        margin-bottom: 35px;
        padding: 20px;
        background-color: #2D2D2D;
        border-radius: 10px;
    }
    
    .avatar-placeholder {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background-color: #444444;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #999999;
        font-size: 14px;
        margin-right: 25px;
        border: 3px solid #FF4B4B;
    }
    
    .info-details h2 {
        margin: 0 0 8px 0;
        color: #FFFFFF;
        font-size: 28px;
    }
    
    .info-details .position {
        color: #FF4B4B;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 12px;
    }
    
    .info-details .contact {
        color: #AAAAAA;
        font-size: 15px;
        line-height: 1.6;
    }
    
    /* 章节标题 */
    .section-header {
        color: #FF4B4B;
        font-size: 20px;
        font-weight: bold;
        margin-top: 25px;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 2px solid #333333;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 上传组件样式 */
    .uploadedFile {
        background-color: #2D2D2D;
        border: 1px solid #444444;
        border-radius: 5px;
        padding: 10px;
        color: #FFFFFF;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #FF3333;
        transform: translateY(-2px);
    }
    
    /* 红色主题 */
    .red-accent {
        color: #FF4B4B;
        font-weight: bold;
    }
    
    /* 清除按钮样式 */
    .clear-btn {
        background-color: transparent !important;
        border: 1px solid #FF4B4B !important;
        color: #FF4B4B !important;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state - 使用空值或默认占位符
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        'name': '',
        'position': '',
        'phone': '',
        'email': '',
        'birthdate': datetime.now().strftime('%Y-%m-%d'),
        'gender': '请选择',
        'education': '请选择',
        'languages': [],
        'skills': [],
        'experience': 0,
        'salary_min': 5000,
        'salary_max': 15000,
        'bio': '请在此处输入个人简介...',
        'best_time': '09:00'
    }

# 主标题
st.markdown('<div class="main-header">个人简历生成器</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">创建一个专业的个性化简历</div>', unsafe_allow_html=True)

# 创建两列布局
col1, col2 = st.columns([1, 1], gap="large")

# 左侧：个人信息表单（实时更新）
with col1:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">个人信息表单</div>', unsafe_allow_html=True)
    
    # 清除按钮
    if st.button("🧹 清除所有信息", use_container_width=True, type="secondary"):
        st.session_state.form_data = {
            'name': '',
            'position': '',
            'phone': '',
            'email': '',
            'birthdate': datetime.now().strftime('%Y-%m-%d'),
            'gender': '请选择',
            'education': '请选择',
            'languages': [],
            'skills': [],
            'experience': 0,
            'salary_min': 5000,
            'salary_max': 15000,
            'bio': '请在此处输入个人简介...',
            'best_time': '09:00'
        }
        if 'uploaded_image' in st.session_state:
            del st.session_state.uploaded_image
        st.rerun()
    
    # 实时更新函数
    def update_form_field(field, value):
        st.session_state.form_data[field] = value
    
    # 基本信息输入 - 使用on_change实时更新
    name = st.text_input(
        "姓名", 
        value=st.session_state.form_data['name'],
        key="name_input",
        on_change=lambda: update_form_field('name', st.session_state.name_input),
        placeholder="请输入您的姓名"
    )
    
    position = st.text_input(
        "职位", 
        value=st.session_state.form_data['position'],
        key="position_input",
        on_change=lambda: update_form_field('position', st.session_state.position_input),
        placeholder="例如：软件工程师、产品经理"
    )
    
    phone = st.text_input(
        "电话", 
        value=st.session_state.form_data['phone'],
        key="phone_input",
        on_change=lambda: update_form_field('phone', st.session_state.phone_input),
        placeholder="请输入您的手机号码"
    )
    
    email = st.text_input(
        "邮箱", 
        value=st.session_state.form_data['email'],
        key="email_input",
        on_change=lambda: update_form_field('email', st.session_state.email_input),
        placeholder="请输入您的邮箱地址"
    )
    
    # 日期输入
    try:
        birthdate = st.date_input(
            "出生日期",
            value=datetime.strptime(st.session_state.form_data['birthdate'], '%Y-%m-%d'),
            format="YYYY/MM/DD",
            key="birthdate_input",
            on_change=lambda: update_form_field('birthdate', st.session_state.birthdate_input.strftime('%Y-%m-%d'))
        )
    except:
        birthdate = st.date_input(
            "出生日期",
            value=datetime.now(),
            format="YYYY/MM/DD",
            key="birthdate_input",
            on_change=lambda: update_form_field('birthdate', st.session_state.birthdate_input.strftime('%Y-%m-%d'))
        )
    
    # 性别和学历 - 使用columns布局
    col_gender, col_edu = st.columns(2)
    with col_gender:
        gender = st.selectbox(
            "性别", 
            ["请选择", "男", "女", "其他"], 
            index=["请选择", "男", "女", "其他"].index(st.session_state.form_data['gender']) 
            if st.session_state.form_data['gender'] in ["请选择", "男", "女", "其他"] else 0,
            key="gender_select",
            on_change=lambda: update_form_field('gender', st.session_state.gender_select)
        )
    
    with col_edu:
        education = st.selectbox(
            "学历", 
            ["请选择", "高中", "大专", "本科", "硕士", "博士", "其他"], 
            index=["请选择", "高中", "大专", "本科", "硕士", "博士", "其他"].index(st.session_state.form_data['education']) 
            if st.session_state.form_data['education'] in ["请选择", "高中", "大专", "本科", "硕士", "博士", "其他"] else 0,
            key="edu_select",
            on_change=lambda: update_form_field('education', st.session_state.edu_select)
        )
    
    # 语言能力（多选）- 更多选项
    languages = st.multiselect(
        "语言能力 (可多选)",
        ["中文", "英语", "日语", "韩语", "法语", "德语", "西班牙语", "俄语", "阿拉伯语", "葡萄牙语", "意大利语"],
        default=st.session_state.form_data['languages'],
        key="lang_multiselect",
        on_change=lambda: update_form_field('languages', st.session_state.lang_multiselect)
    )
    
    # 技能（多选） - 多元化选项
    skills = st.multiselect(
        "专业技能 (可多选)",
        [
            "Java", "Python", "JavaScript", "TypeScript", "HTML/CSS", "React", "Vue.js", "Angular",
            "Node.js", "Spring Boot", "Django", "Flask", "机器学习", "深度学习", "数据分析",
            "SQL", "NoSQL", "Docker", "Kubernetes", "AWS", "Azure", "Git", "敏捷开发",
            "UI/UX设计", "产品管理", "项目管理", "测试自动化", "网络安全", "区块链"
        ],
        default=st.session_state.form_data['skills'],
        key="skills_multiselect",
        on_change=lambda: update_form_field('skills', st.session_state.skills_multiselect)
    )
    
    # 工作经验滑块
    experience = st.slider(
        "工作经验（年）", 
        0, 30, 
        st.session_state.form_data['experience'],
        key="exp_slider",
        on_change=lambda: update_form_field('experience', st.session_state.exp_slider)
    )
    
    # 薪资范围滑块
    salary_min, salary_max = st.slider(
        "期望薪资范围（元/月）",
        3000, 50000,
        (st.session_state.form_data['salary_min'], st.session_state.form_data['salary_max']),
        key="salary_slider",
        on_change=lambda: update_form_field('salary_min', st.session_state.salary_slider[0]) or 
                        update_form_field('salary_max', st.session_state.salary_slider[1])
    )
    
    # 个人简介
    bio = st.text_area(
        "个人简介",
        value=st.session_state.form_data['bio'],
        height=180,
        key="bio_textarea",
        on_change=lambda: update_form_field('bio', st.session_state.bio_textarea),
        placeholder="请简要介绍您的教育背景、工作经验、专业技能和职业目标..."
    )
    
    # 每日最佳联系时间段
    best_time = st.selectbox(
        "每日最佳联系时间段",
        ["请选择", "08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00", 
         "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00", 
         "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00",
         "20:00-21:00", "21:00-22:00"],
        index=["请选择", "08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00", 
              "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00", 
              "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00",
              "20:00-21:00", "21:00-22:00"].index(st.session_state.form_data['best_time']) 
              if st.session_state.form_data['best_time'] in ["请选择", "08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00", 
              "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00", 
              "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00",
              "20:00-21:00", "21:00-22:00"] else 0,
        key="time_select",
        on_change=lambda: update_form_field('best_time', st.session_state.time_select)
    )
    
    # 上传个人照片区域
    st.markdown("### 上传个人照片")
    uploaded_file = st.file_uploader(
        "拖放文件到这里或点击浏览",
        type=['jpg', 'jpeg', 'png', 'gif'],
        label_visibility="collapsed",
        help="支持 JPG、JPEG、PNG、GIF 格式，最大 200MB"
    )
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.session_state.uploaded_image = image
            st.image(image, caption=f"{uploaded_file.name} - {uploaded_file.size/1024:.2f} KB", width=150)
        except Exception as e:
            st.error(f"图片加载失败: {e}")
    else:
        st.info("请上传个人照片 (.JPG, .JPEG, .PNG, .GIF)")
        if 'uploaded_image' in st.session_state:
            del st.session_state.uploaded_image
    
    st.markdown('</div>', unsafe_allow_html=True)

# 右侧：简历实时预览
with col2:
    st.markdown('<div class="preview-card">', unsafe_allow_html=True)
    st.markdown('<div class="preview-title">简历实时预览</div>', unsafe_allow_html=True)
    
    # 显示实时更新状态
    with st.empty():
        st.markdown(f'<div style="color:#4CAF50; text-align:right; font-size:12px; margin-bottom:10px;">🔄 实时更新中...</div>', unsafe_allow_html=True)
    
    # 简历标题
    st.markdown('<div class="resume-title">个人简历</div>', unsafe_allow_html=True)
    
    # 个人信息区域 - 头像和个人信息
    st.markdown('<div class="personal-info">', unsafe_allow_html=True)
    
    # 头像区域
    if 'uploaded_image' in st.session_state:
        # 调整图片大小并显示
        img = st.session_state.uploaded_image
        img.thumbnail((120, 120))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        st.markdown(f'''
            <div style="margin-right: 25px;">
                <img src="data:image/png;base64,{img_str}" 
                     style="width: 120px; height: 120px; border-radius: 50%; border: 3px solid #FF4B4B; object-fit: cover;">
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('<div class="avatar-placeholder">上传照片</div>', unsafe_allow_html=True)
    
    # 个人信息详情
    name_display = st.session_state.form_data['name'] if st.session_state.form_data['name'] else "【请输入姓名】"
    position_display = st.session_state.form_data['position'] if st.session_state.form_data['position'] else "【请输入职位】"
    phone_display = st.session_state.form_data['phone'] if st.session_state.form_data['phone'] else "【请输入电话】"
    email_display = st.session_state.form_data['email'] if st.session_state.form_data['email'] else "【请输入邮箱】"
    birthdate_display = st.session_state.form_data['birthdate'] if st.session_state.form_data['birthdate'] != datetime.now().strftime('%Y-%m-%d') else "【请选择出生日期】"
    gender_display = st.session_state.form_data['gender'] if st.session_state.form_data['gender'] != "请选择" else "【请选择性别】"
    education_display = st.session_state.form_data['education'] if st.session_state.form_data['education'] != "请选择" else "【请选择学历】"
    
    st.markdown(f'''
    <div class="info-details">
        <h2>{name_display}</h2>
        <div class="position">{position_display}</div>
        <div class="contact">
            📱 {phone_display} | ✉️ {email_display}<br>
            🎂 {birthdate_display} | 👤 {gender_display} | 🎓 {education_display}
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 个人简介
    st.markdown('<div class="section-header">个人简介</div>', unsafe_allow_html=True)
    bio_display = st.session_state.form_data['bio'] if st.session_state.form_data['bio'] != '请在此处输入个人简介...' else "请左侧输入个人简介..."
    st.markdown(f'<div class="bio-text">{bio_display}</div>', unsafe_allow_html=True)
    
    # 专业技能
    st.markdown('<div class="section-header">专业技能</div>', unsafe_allow_html=True)
    if st.session_state.form_data['skills']:
        skills_html = " ".join([f'<span class="skill-tag">{skill}</span>' for skill in st.session_state.form_data["skills"]])
        st.markdown(f'<div>{skills_html}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#666; font-style:italic;">【请选择专业技能】</div>', unsafe_allow_html=True)
    
    # 语言能力
    st.markdown('<div class="section-header">语言能力</div>', unsafe_allow_html=True)
    if st.session_state.form_data['languages']:
        languages_html = " ".join([f'<span class="language-tag">{lang}</span>' for lang in st.session_state.form_data["languages"]])
        st.markdown(f'<div>{languages_html}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#666; font-style:italic;">【请选择语言能力】</div>', unsafe_allow_html=True)
    
    # 工作经验
    st.markdown('<div class="section-header">工作经验</div>', unsafe_allow_html=True)
    exp_display = f"{st.session_state.form_data['experience']} 年" if st.session_state.form_data['experience'] > 0 else "应届生/无工作经验"
    st.markdown(f'<div style="color:#FFFFFF; font-size:18px; font-weight:bold;">{exp_display}</div>', unsafe_allow_html=True)
    
    # 期望薪资
    st.markdown('<div class="section-header">期望薪资</div>', unsafe_allow_html=True)
    salary_display = f"{st.session_state.form_data['salary_min']:,} - {st.session_state.form_data['salary_max']:,} 元/月"
    st.markdown(f'''
    <div style="color:#FFFFFF; font-size:20px; font-weight:bold; background-color:#2D2D2D; padding:15px; border-radius:8px; border-left:4px solid #FF4B4B;">
        {salary_display}
    </div>
    ''', unsafe_allow_html=True)
    
    # 最佳联系时间
    st.markdown('<div class="section-header">最佳联系时间段</div>', unsafe_allow_html=True)
    time_display = st.session_state.form_data['best_time'] if st.session_state.form_data['best_time'] != "请选择" else "请选择时间段"
    st.markdown(f'''
    <div style="color:#FFFFFF; font-size:18px; background-color:#2D2D2D; padding:12px 20px; border-radius:8px; display:inline-block; border:2px solid #FF4B4B;">
        🕐 {time_display}
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 底部操作按钮
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    col_export, col_print, col_reset = st.columns(3)
    with col_export:
        if st.button("📥 导出简历", use_container_width=True, type="primary"):
            st.success("简历数据已准备就绪！")
            st.info("导出功能需要额外配置，可以添加PDF生成或数据导出功能")
    with col_print:
        if st.button("🖨️ 打印预览", use_container_width=True):
            st.info("按下 Ctrl+P 使用浏览器打印功能")
    with col_reset:
        if st.button("🔄 重新开始", use_container_width=True, type="secondary"):
            st.session_state.form_data = {
                'name': '',
                'position': '',
                'phone': '',
                'email': '',
                'birthdate': datetime.now().strftime('%Y-%m-%d'),
                'gender': '请选择',
                'education': '请选择',
                'languages': [],
                'skills': [],
                'experience': 0,
                'salary_min': 5000,
                'salary_max': 15000,
                'bio': '请在此处输入个人简介...',
                'best_time': '09:00'
            }
            if 'uploaded_image' in st.session_state:
                del st.session_state.uploaded_image
            st.rerun()
