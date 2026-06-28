# AI陪玩平台

基于Python实现的AI陪玩平台，提供陪玩匹配、论坛交流、消息聊天等功能。

## 功能特性

### 🎮 核心功能
- **陪玩列表** - 浏览和筛选50+专业陪玩师
- **心愿匹配** - AI智能匹配符合需求的陪玩
- **游戏论坛** - 游戏攻略分享、组队开黑讨论
- **消息中心** - 与陪玩即时聊天沟通
- **用户中心** - 个人信息管理、订单管理

### 🎨 界面特点
- 现代化深色主题设计
- 响应式布局，支持各种屏幕尺寸
- 流畅的动画效果和交互体验

## 技术栈

- **后端**: Python 3.x (内置HTTP服务器)
- **前端**: HTML5 + CSS3 + JavaScript
- **数据存储**: JSON文件数据库
- **头像生成**: DiceBear API

## 快速开始

### 环境要求

- Python 3.7+

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd PGTX
```

2. **生成数据**
```bash
python generate_data.py
```

3. **启动服务器**
```bash
python main.py
```

4. **访问网站**

打开浏览器访问: http://localhost:8080

## 页面结构

```
/                    # 首页
/partners            # 陪玩列表
/wish                # 心愿匹配
/forum               # 游戏论坛
/chat                # 消息中心
/login               # 登录页面
/register            # 注册页面
/center              # 用户中心
/feedback            # 问题反馈
/admin               # 管理后台
```

## 数据文件

项目使用JSON文件存储数据，位于 `data/` 目录：

- `user.json` - 用户数据
- `partner.json` - 陪玩数据
- `order.json` - 订单数据
- `comment.json` - 评价数据
- `forum_posts.json` - 论坛帖子
- `forum_comments.json` - 论坛评论
- `chat_sessions.json` - 聊天会话
- `chat_messages.json` - 聊天消息

## 使用说明

### 1. 浏览陪玩
- 访问首页或 `/partners` 查看所有陪玩师
- 使用筛选器按游戏、价格、声线筛选
- 点击卡片查看陪玩详情

### 2. 心愿匹配
- 访问 `/wish` 进入心愿匹配页面
- 填写目标游戏、预算区间、声线偏好
- 点击"开始AI匹配"获取推荐结果

### 3. 论坛交流
- 访问 `/forum` 浏览论坛帖子
- 点击帖子查看详情和评论
- 点击"发帖"按钮发布新帖子

### 4. 消息聊天
- 访问 `/chat` 查看消息列表
- 点击聊天会话进入聊天窗口
- 发送消息与陪玩实时沟通

### 5. 用户注册/登录
- 点击右上角"登录"或"注册"
- 注册后可使用完整功能

## 默认账户

### 管理员账户
- 用户名: admin
- 密码: admin123

### 测试用户
系统生成了20个测试玩家和50个陪玩师，可直接浏览体验。

## 项目结构

```
PGTX/
├── main.py              # 主服务器文件
├── generate_data.py     # 数据生成脚本
├── data/                # 数据文件目录
├── template/            # HTML模板目录
│   ├── home_html.py
│   ├── partner_html.py
│   ├── wish_html.py
│   ├── forum_html.py
│   ├── chat_html.py
│   └── ...
├── service/             # 服务模块
│   └── recommend_ai.py
└── utils/               # 工具模块
    └── json_db.py
```

## 开发说明

### 添加新页面

1. 在 `template/` 目录创建新的HTML模板文件
2. 在 `main.py` 中添加路由和处理逻辑

### 修改样式

所有页面样式均使用内联CSS，可在对应模板文件中修改。

## 注意事项

- 本项目仅用于学习和演示目的
- 数据存储使用JSON文件，不适合大规模生产环境
- 建议在本地开发环境运行

## License

MIT License
