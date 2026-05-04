<template>
  <div class="about-page">
    <div class="logo">
      <svg class="svg" width="72px" height="72px" viewBox="0 0 64 64" version="1.1">
        <title>Icon</title>
        <defs>
          <linearGradient x1="50%" y1="0%" x2="50%" y2="100%" id="linearGradient-1">
            <stop stop-color="#FFFFFF" offset="0%"></stop>
            <stop stop-color="#F2F2F2" offset="100%"></stop>
          </linearGradient>
          <circle id="path-2" cx="31.9988602" cy="31.9988602" r="2.92886048"></circle>
          <filter x="-85.4%" y="-68.3%" width="270.7%" height="270.7%" filterUnits="objectBoundingBox" id="filter-3">
            <feOffset dx="0" dy="1" in="SourceAlpha" result="shadowOffsetOuter1"></feOffset>
            <feGaussianBlur stdDeviation="1.5" in="shadowOffsetOuter1" result="shadowBlurOuter1"></feGaussianBlur>
            <feColorMatrix values="0 0 0 0 0   0 0 0 0 0   0 0 0 0 0  0 0 0 0.159703351 0" type="matrix"
              in="shadowBlurOuter1"></feColorMatrix>
          </filter>
        </defs>
        <g id="slogo" class="rotation" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
          <g>
            <g id="Icon">
              <circle id="Oval-1" fill="url(#linearGradient-1)" cx="32" cy="32" r="32"></circle>
              <path
                d="M36.7078009,31.8054514 L36.7078009,51.7110548 C36.7078009,54.2844537 34.6258634,56.3695395 32.0579205,56.3695395 C29.4899777,56.3695395 27.4099998,54.0704461 27.4099998,51.7941246 L27.4099998,31.8061972 C27.4099998,29.528395 29.4909575,27.218453 32.0589004,27.230043 C34.6268432,27.241633 36.7078009,29.528395 36.7078009,31.8054514 Z"
                id="blue" fill="#2359F1" fill-rule="nonzero"></path>
              <path
                d="M45.2586091,17.1026914 C45.2586091,17.1026914 45.5657231,34.0524383 45.2345291,37.01141 C44.9033351,39.9703817 43.1767091,41.6667796 40.6088126,41.6667796 C38.040916,41.6667796 35.9609757,39.3676862 35.9609757,37.0913646 L35.9609757,17.1034372 C35.9609757,14.825635 38.0418959,12.515693 40.6097924,12.527283 C43.177689,12.538873 45.2586091,14.825635 45.2586091,17.1026914 Z"
                id="green" fill="#57CF27" fill-rule="nonzero"
                transform="translate(40.674608, 27.097010) rotate(60.000000) translate(-40.674608, -27.097010) "></path>
              <path
                d="M28.0410158,17.0465598 L28.0410158,36.9521632 C28.0410158,39.525562 25.9591158,41.6106479 23.3912193,41.6106479 C20.8233227,41.6106479 18.7433824,39.3115545 18.7433824,37.035233 L18.7433824,17.0473055 C18.7433824,14.7695034 20.8243026,12.4595614 23.3921991,12.4711513 C25.9600956,12.4827413 28.0410158,14.7695034 28.0410158,17.0465598 Z"
                id="red" fill="#FF561B" fill-rule="nonzero"
                transform="translate(23.392199, 27.040878) rotate(-60.000000) translate(-23.392199, -27.040878) ">
              </path>
              <g id="inner-round">
                <use fill="black" fill-opacity="1" filter="url(#filter-3)" xlink:href="#path-2"></use>
                <use fill="#F7F7F7" fill-rule="evenodd" xlink:href="#path-2"></use>
              </g>
            </g>
          </g>
        </g>
      </svg>
      <span class="name">系统架构</span>
    </div>

    <div class="about-content">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>系统处理流程</span>
        </div>
        <div class="flow-chart">
          <div class="flow-step">
            <div class="step-icon"><i class="el-icon-search"></i></div>
            <div class="step-title">数据采集</div>
            <div class="step-desc">Scrapy + Scrapyd 分布式爬虫<br>微博用户信息、微博内容、评论数据</div>
          </div>
          <div class="flow-arrow"><i class="el-icon-right"></i></div>
          <div class="flow-step">
            <div class="step-icon"><i class="el-icon-coin"></i></div>
            <div class="step-title">数据存储</div>
            <div class="step-desc">Django ORM + SQLite<br>用户信息、微博内容、评论、词云结果</div>
          </div>
          <div class="flow-arrow"><i class="el-icon-right"></i></div>
          <div class="flow-step">
            <div class="step-icon"><i class="el-icon-data-analysis"></i></div>
            <div class="step-title">情感分析</div>
            <div class="step-desc">SnowNLP 情感分析引擎<br>情感值计算、关键词提取、敏感词检测</div>
          </div>
          <div class="flow-arrow"><i class="el-icon-right"></i></div>
          <div class="flow-step">
            <div class="step-icon"><i class="el-icon-monitor"></i></div>
            <div class="step-title">可视化展示</div>
            <div class="step-desc">Vue + ECharts + Element UI<br>词云、折线图、柱状图、数据表格</div>
          </div>
        </div>
      </el-card>

      <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="8">
          <el-card class="box-card tech-card">
            <div slot="header" class="clearfix">
              <span>前端技术栈</span>
            </div>
            <div class="tech-list">
              <el-tag type="success" size="medium" effect="dark">Vue.js 2.x</el-tag>
              <el-tag type="primary" size="medium" effect="dark">Vuex</el-tag>
              <el-tag type="info" size="medium" effect="dark">Vue Router</el-tag>
              <el-tag type="warning" size="medium" effect="dark">Axios</el-tag>
              <el-tag effect="dark" size="medium">Element UI</el-tag>
              <el-tag type="success" size="medium" effect="dark">ECharts / v-charts</el-tag>
              <el-tag type="danger" size="medium" effect="dark">Webpack</el-tag>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="box-card tech-card">
            <div slot="header" class="clearfix">
              <span>后端技术栈</span>
            </div>
            <div class="tech-list">
              <el-tag type="success" size="medium" effect="dark">Python 3.x</el-tag>
              <el-tag type="primary" size="medium" effect="dark">Django 2.2</el-tag>
              <el-tag type="info" size="medium" effect="dark">Django ORM</el-tag>
              <el-tag type="warning" size="medium" effect="dark">SQLite</el-tag>
              <el-tag effect="dark" size="medium">XAdmin</el-tag>
              <el-tag type="danger" size="medium" effect="dark">REST API</el-tag>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="box-card tech-card">
            <div slot="header" class="clearfix">
              <span>爬虫 &amp; NLP</span>
            </div>
            <div class="tech-list">
              <el-tag type="success" size="medium" effect="dark">Scrapy</el-tag>
              <el-tag type="primary" size="medium" effect="dark">Scrapyd</el-tag>
              <el-tag type="info" size="medium" effect="dark">Requests</el-tag>
              <el-tag type="warning" size="medium" effect="dark">SnowNLP</el-tag>
              <el-tag effect="dark" size="medium">XPath</el-tag>
              <el-tag type="danger" size="medium" effect="dark">jieba 分词</el-tag>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-card class="box-card" style="margin-top: 20px;">
        <div slot="header" class="clearfix">
          <span>系统简介</span>
        </div>
        <div class="intro-text">
          <p>本系统是一个基于自然语言处理的微博用户情感分析系统，主要功能包括：</p>
          <ul>
            <li><strong>微博数据采集</strong>：通过 Scrapy 爬虫框架和 Scrapyd 分布式部署，实现对微博用户信息、微博内容和评论的自动化采集</li>
            <li><strong>情感分析</strong>：基于 SnowNLP 对微博文本进行情感值计算、关键词提取和词性标注</li>
            <li><strong>敏感词检测</strong>：对微博内容进行敏感词过滤和敏感率统计</li>
            <li><strong>词云生成</strong>：基于微博文本内容生成词云图，直观展示用户关注热点</li>
            <li><strong>可视化展示</strong>：通过 ECharts 图表库，以折线图、柱状图、饼图等多种形式展示分析结果</li>
            <li><strong>舆情预警</strong>：对分组用户的负面情绪占比进行监控，超过阈值时发出预警</li>
            <li><strong>数据导出</strong>：支持将微博数据和用户信息导出为 CSV 文件</li>
          </ul>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutMain'
}
</script>

<style lang="css" scoped>
  .about-page {
    text-align: center;
    padding-bottom: 50px;
  }

  .logo {
    margin-top: 50px;
  }

  .svg {
    vertical-align: middle;
  }

  .name {
    vertical-align: middle;
    font-size: .48rem;
    margin-left: .24rem;
    font-weight: 200;
    color: #fff;
  }

  @-webkit-keyframes rotation {
    from { -webkit-transform: rotate(0deg); }
    to { -webkit-transform: rotate(360deg); }
  }

  .rotation {
    -webkit-transform: rotate(360deg);
    animation: rotation 3s linear infinite;
    transform-origin: center center;
  }

  .about-content {
    max-width: 1000px;
    margin: 30px auto;
    padding: 0 20px;
  }

  .flow-chart {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    padding: 20px 0;
  }

  .flow-step {
    width: 180px;
    text-align: center;
  }

  .step-icon {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 10px;
  }

  .step-icon i {
    font-size: 28px;
    color: #fff;
  }

  .step-title {
    font-size: 16px;
    font-weight: bold;
    color: #333;
    margin-bottom: 8px;
  }

  .step-desc {
    font-size: 13px;
    color: #666;
    line-height: 1.6;
  }

  .flow-arrow {
    font-size: 24px;
    color: #409EFF;
    margin: 0 10px;
  }

  .tech-card {
    min-height: 200px;
  }

  .tech-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    padding: 10px 0;
  }

  .intro-text {
    text-align: left;
    font-size: 15px;
    line-height: 1.8;
    color: #333;
  }

  .intro-text ul {
    padding-left: 20px;
  }

  .intro-text li {
    margin-bottom: 8px;
  }
</style>
