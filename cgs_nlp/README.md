# WeiboNLP - 微博数据分析系统

微博数据分析系统，支持微博用户信息爬取、评论分析、情感分析和词云可视化。

## 技术栈

- **后端**: Django 2.2 + MySQL/SQLite
- **爬虫**: Scrapy
- **前端**: Vue 2 + Element UI
- **数据分析**: SnowNLP + WordCloud

## 项目结构

```
cgs_nlp/
├── cgs_nlp/          # Django项目配置
├── src/              # 应用模块
│   ├── SpiderAPI/     # 微博爬虫API
│   ├── ScrapydAPI/    # 爬虫管理API
│   └── SnowNLPAPI/   # 情感分析API
├── webview/          # Vue前端
├── scrapydserver/    # Scrapy爬虫服务
└── extra_apps/       # 第三方应用
```

## 安装

### 1. 安装依赖

```bash
pip install -r requirements.txt
cd webview && npm install
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并配置：

```bash
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DB_PASSWORD=your-db-password
```

### 3. 数据库迁移

```bash
python manage.py migrate
```

### 4. 启动服务

开发环境：
```bash
python manage.py runserver
```

前端开发：
```bash
cd webview && npm run serve
```

## 环境变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| DJANGO_SECRET_KEY | Django密钥 | 自动生成 |
| DJANGO_DEBUG | 调试模式 | False |
| DJANGO_ALLOWED_HOSTS | 允许的域名 | localhost,127.0.0.1 |
| CORS_ALLOW_ALL | 允许所有跨域 | False |
| DATABASE_URL | 数据库URL | (空，使用SQLite) |
| DB_NAME | 数据库名 | WclNlpSystem |
| DB_USER | 数据库用户 | root |
| DB_PASSWORD | 数据库密码 | (空) |
| DB_HOST | 数据库主机 | localhost |
| DB_PORT | 数据库端口 | 3306 |

## 功能特性

- 微博用户信息爬取
- 微博内容分析和词云生成
- 评论数据采集和趋势分析
- SnowNLP情感分析
- 微博用户快速搜索

## 许可证

MIT License
