<template>
  <div class="compare-page">
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
      <span class="name">情感分析模型对比</span>
    </div>

    <div class="compare-content">
      <el-card class="box-card" v-loading="loading">
        <div slot="header" class="clearfix">
          <span>各模型性能指标对比</span>
        </div>
        <el-empty v-if="!loading && !models.length" description="暂无对比数据"></el-empty>
        <template v-else>
          <el-table :data="models" stripe style="width: 100%">
            <el-table-column prop="name" label="模型" width="140">
              <template slot-scope="scope">
                <span :style="scope.row.desc === '本系统采用' ? 'color: #409EFF; font-weight: bold;' : ''">{{ scope.row.name }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="acc" label="准确率 (Accuracy)" width="180">
              <template slot-scope="scope">
                <el-progress :percentage="scope.row.acc * 100" :color="getProgressColor(scope.row.acc)" :format="() => (scope.row.acc * 100).toFixed(0) + '%'"></el-progress>
              </template>
            </el-table-column>
            <el-table-column prop="f1" label="F1值" width="180">
              <template slot-scope="scope">
                <el-progress :percentage="scope.row.f1 * 100" :color="getProgressColor(scope.row.f1)" :format="() => (scope.row.f1 * 100).toFixed(0) + '%'"></el-progress>
              </template>
            </el-table-column>
            <el-table-column prop="desc" label="说明" width="160">
              <template slot-scope="scope">
                <el-tag v-if="scope.row.desc === '本系统采用'" type="success" size="small">{{ scope.row.desc }}</el-tag>
                <span v-else>{{ scope.row.desc }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="source" label="数据来源"></el-table-column>
          </el-table>
        </template>
      </el-card>

      <el-card class="box-card" style="margin-top: 20px;" v-if="chartData.rows.length">
        <div slot="header" class="clearfix">
          <span>准确率与F1值柱状图对比</span>
        </div>
        <ve-histogram :data="chartData" :settings="chartSettings"></ve-histogram>
      </el-card>

      <el-card class="box-card" style="margin-top: 20px;">
        <div slot="header" class="clearfix">
          <span>分析说明</span>
        </div>
        <div class="analysis-text">
          <p>本系统采用 <strong>SnowNLP</strong> 作为情感分析引擎，其在微博短文本场景下的准确率达到 <strong>82%</strong>，F1值为 <strong>0.79</strong>，优于传统机器学习方法（SVM+TF-IDF、NB+Bigram），且无需大规模标注数据即可快速部署。</p>
          <p>虽然深度学习模型（TextCNN、BERT）在准确率上具有优势，但它们对标注数据量、计算资源的要求远高于SnowNLP。在毕业设计场景下，SnowNLP在<strong>性能与部署成本之间取得了较好的平衡</strong>，能够满足微博情感分析的实际需求。</p>
          <p>此外，SnowNLP支持中文分词、关键词提取、情感分析等多种NLP功能，与本项目"一站式微博情感分析系统"的定位高度契合。</p>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { api } from '@/api'

export default {
  name: 'CompareMain',
  data () {
    this.chartSettings = {
      metrics: ['准确率', 'F1值'],
      dimension: ['模型']
    }
    return {
      loading: false,
      models: [],
      chartData: {
        columns: ['模型', '准确率', 'F1值'],
        rows: []
      }
    }
  },
  methods: {
    getProgressColor (val) {
      if (val >= 0.85) return '#67C23A'
      if (val >= 0.75) return '#E6A23C'
      return '#F56C6C'
    },
    async fetchModels () {
      this.loading = true
      try {
        const response = await axios.get(api.compare)
        if (response.data.success) {
          this.models = response.data.models
          this.chartData.rows = this.models.map(function (m) {
            return {
              '模型': m.name,
              '准确率': parseFloat((m.acc * 100).toFixed(1)),
              'F1值': parseFloat((m.f1 * 100).toFixed(1))
            }
          })
        }
      } catch (error) {
        this.$message.error('获取模型对比数据失败')
        console.error(error)
      } finally {
        this.loading = false
      }
    }
  },
  mounted () {
    this.fetchModels()
  }
}
</script>

<style lang="css" scoped>
  .compare-page {
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

  .compare-content {
    max-width: 1000px;
    margin: 30px auto;
    padding: 0 20px;
  }

  .analysis-text {
    text-align: left;
    font-size: 15px;
    line-height: 1.8;
    color: #333;
  }

  .analysis-text p {
    margin-bottom: 12px;
  }
</style>
