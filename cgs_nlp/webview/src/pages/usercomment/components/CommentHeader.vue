<template>
  <div>
    <div v-if="!hasData" class="no-data">
      <el-card style="text-align: center; padding: 40px;">
        <i class="el-icon-warning" style="font-size: 48px; color: #E6A23C;"></i>
        <p style="font-size: 18px; margin-top: 20px;">暂无评论数据</p>
        <p style="color: #999;">请先在单条微博分析页面输入微博链接</p>
        <el-button type="primary" style="margin-top: 20px;" @click="$router.push('/comment')">返回评论分析</el-button>
      </el-card>
    </div>
    <div v-else>
      <div class="comment-header">
        <div class="comment-info">
          <h3>微博评论分析</h3>
          <p v-if="weiboIds && weiboIds.length">微博ID: {{weiboIds.join(', ')}}</p>
        </div>
      </div>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>评论词云</span>
            </div>
            <div v-if="chartData === ''" style="padding: 10px;">词云加载中...</div>
            <div v-else>
              <ve-wordcloud :data="chartData" :settings="chartSettings" @click="handleWordClick"></ve-wordcloud>
              <div v-if="filterWord" class="filter-banner">
                <el-alert
                  :title="'当前筛选词: ' + filterWord"
                  type="info"
                  :closable="true"
                  @close="clearFilter">
                </el-alert>
              </div>
              <div class="well fz14" style="padding: 10px;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important">
                评论内容中，词云分析结果如上图所示，其中
                <strong>{{chartData.rows[0] ? chartData.rows[0].word : '无'}}</strong>的频率最高，达到
                <strong>{{chartData.rows[0] ? chartData.rows[0].count : 0}}</strong>次。
              </div>
            </div>
          </el-card>
          <el-card class="box-card" style="margin-top: 20px;">
            <div slot="header" class="clearfix">
              <span>敏感率</span>
            </div>
            <div v-if="minganData === ''" style="padding: 10px;">敏感率加载中...</div>
            <div v-else>
              <ve-bar :data="minganData" height="3.4rem"></ve-bar>
              <div class="well fz14" style="padding: 10px;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important">
                评论内容中，敏感占比
                <strong>{{minganData.rows[0] ? (minganData.rows[0].敏感 * 100).toFixed(2) : 0}}%</strong>。
              </div>
            </div>
          </el-card>
          <el-card class="box-card" style="margin-top: 20px;">
            <div slot="header" class="clearfix">
              <span>情感分析折线图</span>
            </div>
            <div v-if="textchartData === ''" style="padding: 10px;">情感分析结果加载中...</div>
            <div v-else>
              <ve-line :data="textchartData" style="margin-top: 10px;"></ve-line>
              <div class="well fz14" style="padding: 10px;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important">
                评论情感分析结果如上图所示，
                全部评论中：消极评论内容占比<strong>{{emtionanaly.len > 0 ? ((emtionanaly.count0 / emtionanaly.len)*100).toFixed(2) : 0}}%</strong>，
                积极评论内容占比<strong>{{emtionanaly.len > 0 ? ((emtionanaly.count1 / emtionanaly.len)*100).toFixed(2) : 0}}%</strong>。
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>评论内容情感分析</span>
              <el-button style="float: right; padding: 3px 0" type="text" @click="exportComments">导出评论数据</el-button>
            </div>
            <div v-for="(comment, index) in filteredComments" :key="index" style="height:auto">
              <div class="comment-item">
                <div class="comment-header-info">
                  <span class="comment-user">{{comment.fields.c_userName}}</span>
                  <span class="comment-time">{{comment.fields.c_created_at}}</span>
                </div>
                <div class="comment-content">
                  <span v-if="!filterWord">{{comment.fields.c_content}}</span>
                  <span v-else v-html="highlightText(comment.fields.c_content)"></span>
                </div>
                <div class="comment-footer">
                  <span>来自 {{comment.fields.c_source || '微博'}}</span>
                  <span>点赞 {{comment.fields.c_like_num}}</span>
                </div>
              </div>
              <div class="comment-sentiment">
                <div class="sentiment-left">
                  关键字：
                  <span v-if="comment.fields.sentiments > 0.5" style="background:#c2e7b0">{{comment.fields.tags}}</span>
                  <span v-else style="background:#fbc4c4">{{comment.fields.tags}}</span>
                  <br>
                  情感数值：{{comment.fields.sentiments}}
                </div>
                <div class="sentiment-right">
                  <el-progress v-if="comment.fields.sentiments > 0.5" type="circle"
                    :percentage="comment.fields.sentiments * 100" color="#13ce66" :format="formatPos"></el-progress>
                  <el-progress v-else type="circle"
                    :percentage="comment.fields.sentiments * 100" color="#ff4949" :format="formatNeg"></el-progress>
                </div>
              </div>
              <hr style="background-color:#50bfff;height:1px;border:none;">
            </div>
            <div v-if="filterWord && filteredComments.length === 0" style="text-align: center; padding: 30px; color: #999;">
              <p>没有找到包含"{{filterWord}}"的评论</p>
              <el-button type="primary" size="small" @click="clearFilter">清除筛选</el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'
import { api } from '@/api'

export default {
  name: 'CommentHeader',
  data () {
    this.chartSettings = {
      sizeMin: 20,
      sizeMax: 40
    }
    return {
      chartData: '',
      minganData: '',
      textchartData: '',
      filterWord: '',
      emtionanaly: {
        count0: 0,
        count1: 0,
        len: 1,
        maxdate: 0,
        maxcount: 0,
        smalldate: 0,
        smallcount: 0,
        bigdate: 0,
        bigcount: 0
      }
    }
  },
  computed: {
    ...mapState({
      usercomment: state => state.usercomment,
      tempIds: state => state.tempIds
    }),
    hasData () {
      if (!this.usercomment || this.usercomment === 'null' || this.usercomment === '{}') return false
      try {
        var parsed = typeof this.usercomment === 'string' ? JSON.parse(this.usercomment) : this.usercomment
        if (Array.isArray(parsed)) return parsed.length > 0
        if (typeof parsed === 'object') return Object.keys(parsed).length > 0
        return false
      } catch (e) {
        return false
      }
    },
    comments () {
      try {
        var parsed = typeof this.usercomment === 'string' ? JSON.parse(this.usercomment) : this.usercomment
        if (Array.isArray(parsed)) return parsed
        if (typeof parsed === 'object' && parsed !== null) {
          if (parsed.data) {
            var dataStr = typeof parsed.data === 'string' ? parsed.data : JSON.stringify(parsed.data)
            try {
              var dataParsed = JSON.parse(dataStr)
              if (Array.isArray(dataParsed)) return dataParsed
            } catch (e) {}
          }
          var result = []
          for (var key in parsed) {
            if (parsed.hasOwnProperty(key) && Array.isArray(parsed[key])) {
              result = result.concat(parsed[key])
            }
          }
          return result
        }
        return []
      } catch (e) {
        return []
      }
    },
    weiboIds () {
      var ids = this.tempIds
      if (!ids) return []
      if (typeof ids === 'string') {
        return ids.split(',').map(function (id) { return id.trim() })
      }
      if (Array.isArray(ids)) return ids
      return [ids]
    },
    filteredComments () {
      if (!this.filterWord) return this.comments
      return this.comments.filter(function (comment) {
        if (!comment.fields || !comment.fields.c_content) return false
        return comment.fields.c_content.includes(this.filterWord)
      }.bind(this))
    }
  },
  methods: {
    handleWordClick (e) {
      if (e && e.data && e.data.name) {
        this.filterWord = e.data.name
        this.$message.success('已筛选包含"' + e.data.name + '"的评论')
      }
    },
    clearFilter () {
      this.filterWord = ''
    },
    highlightText (text) {
      if (!text || !this.filterWord) return text
      var regex = new RegExp('(' + this.filterWord + ')', 'g')
      return text.replace(regex, '<span style="background-color: #ffeb3b; font-weight: bold; padding: 0 2px; border-radius: 3px;">$1</span>')
    },
    formatPos () {
      return '积极'
    },
    formatNeg () {
      return '消极'
    },
    exportComments () {
      var ids = this.weiboIds.join(',')
      var url = api.export.tweets + '?weiboId=' + ids
      window.open(url, '_blank')
    },
    loadData () {
      if (!this.hasData) return
      var ids = this.weiboIds.join(',')
      this.$notify.info({
        title: '消息',
        message: '正在计算评论情感分析结果',
        position: 'bottom-right'
      })
      axios.get(api.comment + '?commentId=' + ids)
        .then(function (response) {
          var data = response.data
          if (typeof data === 'string') {
            try { data = JSON.parse(data) } catch (e) { return }
          }
          var firstKey = Object.keys(data)[0]
          if (firstKey && data[firstKey] && (data[firstKey].cipin || data[firstKey].mingan || data[firstKey].analy)) {
            data = data[firstKey]
          }
          var res = []
          if (data.cipin) {
            for (var i = 0; i < data.cipin.length; i++) {
              res.push({
                'word': data.cipin[i].word,
                'count': data.cipin[i].count
              })
            }
          }
          if (res.length > 0) {
            this.chartData = {
              columns: ['word', 'count'],
              rows: res
            }
          }

          if (data.mingan !== undefined) {
            var minganValue = parseFloat(data.mingan)
            this.minganData = {
              columns: ['敏感率', '敏感', '非敏感'],
              rows: [
                { '敏感率': '敏感率', '敏感': parseFloat(minganValue.toFixed(2)), '非敏感': parseFloat((1 - minganValue).toFixed(2)) }
              ]
            }
          }

          if (data.analy && data.analy.length > 0) {
            this.emtionanaly.len = data.analy.length
            this.emtionanaly.smalldate = data.analy[0][0]
            this.emtionanaly.smallcount = data.analy[0][1]
            this.emtionanaly.bigdate = data.analy[data.analy.length - 1][0]
            this.emtionanaly.bigcount = data.analy[data.analy.length - 1][1]

            var rows = []
            for (var j = 0; j < data.analy.length; j++) {
              if (data.analy[j][1] > this.emtionanaly.maxcount) {
                this.emtionanaly.maxcount = data.analy[j][1]
                this.emtionanaly.maxdate = data.analy[j][0]
              }
              rows.push({
                '情感值': data.analy[j][0],
                '次数': data.analy[j][1]
              })
              if (data.analy[j][0] < 0.5) {
                this.emtionanaly.count0++
              } else {
                this.emtionanaly.count1++
              }
            }
            this.textchartData = {
              columns: ['情感值', '次数'],
              rows: rows
            }
          }

          var pl = this.emtionanaly.count0 > this.emtionanaly.count1 ? '消极偏多' : '积极偏多'
          this.$notify({
            message: '评论情感倾向：' + pl,
            type: 'success',
            position: 'bottom-right'
          })
        }.bind(this))
        .catch(function (error) {
          this.$message.error('加载评论分析数据失败')
          console.error(error)
        }.bind(this))
    }
  },
  mounted () {
    if (this.hasData) {
      this.loadData()
    }
  }
}
</script>

<style lang="css" scoped>
.no-data {
  padding: 100px 200px;
}

.comment-header {
  text-align: center;
  padding: 20px;
}

.comment-header h3 {
  color: #fff;
  font-size: 20px;
}

.comment-header p {
  color: #ccc;
  font-size: 14px;
}

.comment-item {
  padding: 10px 0;
}

.comment-header-info {
  font-size: 14px;
  color: #808080;
}

.comment-header-info .comment-user {
  color: #409EFF;
  margin-right: 10px;
}

.comment-content {
  margin: 8px 0;
  font-size: 15px;
}

.comment-footer {
  text-align: right;
  color: #808080;
  font-size: 13px;
}

.comment-footer span {
  margin-left: 15px;
}

.comment-sentiment {
  border-left: 5px solid #50bfff;
  padding: 10px;
  margin: 10px 0;
  position: relative;
  min-height: 80px;
}

.sentiment-left {
  width: 75%;
  font-size: 13px;
}

.sentiment-right {
  position: absolute;
  top: 0;
  right: 0;
  width: 25%;
}

.sentiment-right .el-progress {
  transform: scale(0.7);
}

.filter-banner {
  margin: 10px 0;
}

.box-card {
  margin-bottom: 15px;
}
</style>
