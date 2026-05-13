<template>
  <div class="outer">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span class="title">持续爬虫用户情感分析结果</span>
        <el-button style="float: right; padding: 3px 0" type="text"></el-button>
      </div>

      <!-- 舆情预警横幅 -->
      <el-alert
        v-if="warning"
        :title="warningTitle"
        :type="warningLevel"
        :description="warningDescription"
        :closable="false"
        show-icon
        class="warning-alert">
      </el-alert>

      <div class="user">
        <div class="text item" v-for="(o, index) in groupInfos" :key="index" :title="infos(o.user[0].fields)" @click="goInWb(o.user[0].pk)">
          <div class="m_l">
            <img :src="o.user[0].fields.Image">
          </div>
          <div class="m_r">
          <p>{{o.user[0].fields.NickName}}</p>
          <div>简介：
            <span v-if="o.user[0].fields.BriefIntroduction">
              {{o.user[0].fields.BriefIntroduction}}
            </span>
            <span v-else>
              无
            </span>
          </div>
          </div>
        </div>
      </div>
      <div class="userinfo">
        <el-table
        :data="tableData"
        style="width: 100%"
        :row-class-name="tableRowClassName">
          <el-table-column
            prop="index"
            label="主页">
          </el-table-column>
          <el-table-column
            prop="place"
            label="所在地方">
          </el-table-column>
          <el-table-column
            prop="birthday"
            label="生日/星座">
          </el-table-column>
          <el-table-column
            prop="sex"
            label="性取向">
          </el-table-column>
          <el-table-column
            prop="emotions"
            label="情感状态">
          </el-table-column>
          <el-table-column
            prop="vip"
            label="VIP等级">
          </el-table-column>
          <el-table-column
            prop="auth"
            label="认证">
          </el-table-column>
        </el-table>
      </div>
      <div class="usermain">
        <p>词云分析</p>
        <div v-if="chartData === null" v-loading="true" style="min-height: 200px;"></div>
        <div v-else-if="!chartData.rows || chartData.rows.length === 0">
          <el-empty description="暂无词云数据"></el-empty>
        </div>
        <div v-else>
          <ve-wordcloud :data="chartData" :settings="chartSettings1"></ve-wordcloud>
          <div class="well fz14" style="padding: 15px 2px;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important">用户
            <span v-for="(o, index) in groupInfos" :key="index">
              @<strong>{{o.user[0].fields.NickName}}</strong>
            </span>
            的微博的评论中，词汇<strong id="analysis_time">{{chartData.rows[0] && chartData.rows[0].word ? chartData.rows[0].word : '无数据'}}</strong>频率最高，达到<strong id="bloger">{{chartData.rows[0] && chartData.rows[0].count ? chartData.rows[0].count : 0}}</strong> 次。
            其次为<strong id="analysis_time">{{chartData.rows[1] && chartData.rows[1].word ? chartData.rows[1].word : ''}}、{{chartData.rows[2] && chartData.rows[2].word ? chartData.rows[2].word : ''}}、{{chartData.rows[3] && chartData.rows[3].word ? chartData.rows[3].word : ''}}</strong>分别达到
            <strong id="bloger">{{chartData.rows[1] && chartData.rows[1].count ? chartData.rows[1].count : 0}}、{{chartData.rows[2] && chartData.rows[2].count ? chartData.rows[2].count : 0}}、{{chartData.rows[3] && chartData.rows[3].count ? chartData.rows[3].count : 0}}</strong> 次。
          </div>
        </div>
        <p>敏感率（当前敏感率只检测暴恐、反动、民生、色情等词汇）</p>
        <div v-if="chartData1 === null" v-loading="true" style="min-height: 200px;"></div>
        <div v-else-if="!chartData1.rows || chartData1.rows.length === 0">
          <el-empty description="暂无敏感率数据"></el-empty>
        </div>
        <div v-else>
          <ve-bar :data="chartData1" height="3.4rem"></ve-bar>
          <div class="well fz14" style="padding: 15px 2px;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important">用户
            <span v-for="(o, index) in groupInfos" :key="index">
              @<strong>{{o.user[0].fields.NickName}}</strong>
            </span>
            的所有微博分析中，敏感占比<strong>{{mingandata * 100}}%</strong>,
            在<strong>
              <span v-if="mingandata < 0.25">极低</span>
              <span v-else-if="mingandata >= 0.25 && mingandata < 0.5">低</span>
              <span v-else-if="mingandata >= 0.5  && mingandata < 0.75">高</span>
              <span v-else>极高</span>
            </strong>敏感范围内
          </div>
        </div>
        <p>情感分析柱状图</p>
        <div v-if="chartData2 === null" v-loading="true" style="min-height: 200px;"></div>
        <div v-else-if="!chartData2.rows || chartData2.rows.length === 0">
          <el-empty description="暂无情感分析数据"></el-empty>
        </div>
        <div v-else>
          <ve-histogram :data="chartData2" :settings="chartSettings2"></ve-histogram>
          <div class="well fz14" style="padding: 15px 2px;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important">用户
            <span v-for="(o, index) in groupInfos" :key="index">
              @<strong>{{o.user[0].fields.NickName}}</strong>
            </span>
            的微博评论中消极评论最小值<strong>{{ this.emtionanaly.smalldate }} </strong>
            ，次数是<strong>{{ this.emtionanaly.smallcount }} </strong>；
            积极评论最大值<strong>{{ this.emtionanaly.bigdate }} </strong>
            ，次数是<strong>{{ this.emtionanaly.bigcount }} </strong>；
            最大的评论次数是<strong>{{ this.emtionanaly.maxcount }} </strong>次
            ，情感值是<strong>{{ this.emtionanaly.maxdate }} </strong>。
            全部评论中：消极评论内容占比<strong>{{ emtionanaly.len > 0 ? ((emtionanaly.count0 / emtionanaly.len)*100).toFixed(2) : 0 }}%</strong>，
            积极评论内容占比<strong>{{ emtionanaly.len > 0 ? ((emtionanaly.count1 / emtionanaly.len)*100).toFixed(2) : 0 }}%</strong>。
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'
import Qs from 'qs'
import { api } from '@/api'
import { mapState } from 'vuex'

export default {
  name: 'GroupMain',
  data: function () {
    this.chartSettings1 = {
      sizeMin: 30,
      sizeMax: 60
    }
    this.chartSettings2 = {
      metrics: ['次数'],
      dimension: ['情感值']
    }
    return {
      tableData: [],
      chartData: null,
      chartData1: null,
      chartData2: null,
      mingandata: 0,
      loading: '',
      warning: false,
      warningLevel: 'normal',
      warningTitle: '',
      warningDescription: '',
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
  computed: (function () {
    var computedObj = {}
    var stateMap = mapState({
      groupInfo: function (state) {
        return state.group
      }
    })
    for (var key in stateMap) {
      if (stateMap.hasOwnProperty(key)) {
        computedObj[key] = stateMap[key]
      }
    }

    computedObj.groupInfos = function () {
      var res = this.groupInfo
      if (!res || !Array.isArray(res) || res.length === 0) return []
      var result = []
      for (var i = 0; i < res.length; i++) {
        var item = Object.assign({}, res[i])
        try {
          item.user = JSON.parse(item.user)
        } catch (e) {
          item.user = []
        }
        result.push(item)
      }
      return result
    }

    return computedObj
  })(),
  methods: {
    infos: function (infos) {
      return '微博数：' + infos.tweets_num + '  粉丝数：' + infos.fans_num + '  关注数：' + infos.follows_num
    },
    tableRowClassName: function (obj) {
      var rowIndex = obj.rowIndex
      if (rowIndex === 1) {
        return 'warning-row'
      } else if (rowIndex === 3) {
        return 'success-row'
      }
      return ''
    },
    setTableData: function () {
      var res = []
      for (var i = 0; i < this.groupInfos.length; i++) {
        res.push({
          'index': this.groupInfos[i].user[0].fields.NickName,
          'place': this.groupInfos[i].user[0].fields.City ? this.groupInfos[i].user[0].fields.City : '无',
          'birthday': this.groupInfos[i].user[0].fields.Birthday ? this.groupInfos[i].user[0].fields.Birthday : this.groupInfos[i].user[0].fields.Constellation,
          'sex': this.groupInfos[i].user[0].fields.SexOrientation ? this.groupInfos[i].user[0].fields.SexOrientation : '无',
          'emotions': this.groupInfos[i].user[0].fields.Sentiment ? this.groupInfos[i].user[0].fields.Sentiment : '无',
          'vip': this.groupInfos[i].user[0].fields.VIPlevel ? this.groupInfos[i].user[0].fields.VIPlevel : '无',
          'auth': this.groupInfos[i].user[0].fields.Verified ? '已认证' : '无'
        })
      }
      this.tableData = res
    },
    goInWb: function (id) {
      this.openFullScreen2('正在加载用户数据...')
      axios.post(api.spider,
        Qs.stringify({
          weiboId: id
        })
      ).then(function (response) {
        this.$store.state.user = response.data.data
        this.$store.state.usertweets = response.data.tweets
        this.$store.state.total = response.data.total
        this.loading.close()
        this.$router.push({
          path: '/user'
        })
      }.bind(this)).catch(function (error) {
        this.loading.close()
        this.$message.error('加载用户数据失败，请检查网络连接或稍后重试')
        console.error('goInWb error:', error)
      }.bind(this))
    },
    openFullScreen2: function (text) {
      this.loading = this.$loading({
        lock: true,
        text: text || '后台疯狂进行爬虫计算中',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
    }
  },
  mounted: function () {
    this.setTableData()
    this.$notify.info({
      title: '消息',
      message: '请稍后，正在计算最终情感结果',
      position: 'bottom-right'
    })
    axios.get(api.group + '?&weiboIds=' + this.$store.state.tempIds)
      .then(function (response) {
        var res = []
        console.log(response.data)

        // ================== 舆情预警处理 ==================
        if (response.data.warning) {
          this.warning = true
          this.warningLevel = response.data.warning_level === 'danger' ? 'error' : 'warning'
          const ratio = (response.data.negative_ratio * 100).toFixed(2)
          if (response.data.warning_level === 'danger') {
            this.warningTitle = '⚠️ 高危舆情预警！'
            this.warningDescription = `负面情绪占比达到 ${ratio}%，超过 50% 阈值！建议密切关注。`
          } else {
            this.warningTitle = '⚠️ 中危舆情预警'
            this.warningDescription = `负面情绪占比 ${ratio}%，超过 30% 阈值，建议关注。`
          }
        } else {
          this.warning = false
        }

        for (var i = 0; i < response.data.cipin.length; i++) {
          res.push({
            'word': response.data.cipin[i].word,
            'count': response.data.cipin[i].count
          })
        }
        var chartData = {
          columns: ['word', 'count'],
          rows: res
        }
        this.chartData = chartData

        var minganValue = parseFloat(response.data.mingan)
        var chartData1 = {
          columns: ['敏感程度', '敏感', '非敏感'],
          rows: [
            { '敏感程度': '敏感程度', '敏感': minganValue, '非敏感': 1 - minganValue }
          ]
        }
        this.mingandata = minganValue
        this.chartData1 = chartData1

        var rows = []
        if (response.data.analy && response.data.analy.length > 0) {
          this.emtionanaly.len = response.data.analy.length
          this.emtionanaly.smalldate = response.data.analy[0][0]
          this.emtionanaly.smallcount = response.data.analy[0][1]
          this.emtionanaly.bigdate = response.data.analy[response.data.analy.length - 1][0]
          this.emtionanaly.bigcount = response.data.analy[response.data.analy.length - 1][1]

          for (let i = 0; i < response.data.analy.length; i++) {
            if (response.data.analy[i][1] > this.emtionanaly.maxcount) {
              this.emtionanaly.maxcount = response.data.analy[i][1]
              this.emtionanaly.maxdate = response.data.analy[i][0]
            }

            rows.push({
              '情感值': response.data.analy[i][0],
              '次数': response.data.analy[i][1]
            })

            if (response.data.analy[i][0] < 0.5) {
              this.emtionanaly.count0++
            } else {
              this.emtionanaly.count1++
            }
          }
        }

        var chartData2 = {
          columns: ['情感值', '次数'],
          rows: rows
        }
        this.chartData2 = chartData2

        var pl = '消极偏多😭'
        if (this.emtionanaly.count0 > this.emtionanaly.count1) {
          pl = '消极偏多😭'
        } else {
          pl = '积极偏多😁'
        }

        this.$notify({
          title: '成功',
          message: '微博内容评论倾向：' + pl,
          type: 'success',
          position: 'bottom-right'
        })
      }.bind(this))
  }
}
</script>

<style lang="css" scoped>
  .outer {
    margin: 0 auto;
    max-width: 900px;
  }
  .title {
    font-size: 16px;
    padding: 15px 10px 15px 50px;
    margin: 0 0 10px;
    color: #FFF;
    text-align: center;
    background-color: #F8661E;
    background-image: url('../../../assets/icon-wyq.png');
    background-repeat: no-repeat;
    background-position: 10px center;
    padding-left: 50px;
    border-radius: 3px;
  }

  .item{
    padding: 10px;
    overflow: hidden;
    width: 280px;
    display: inline-block;
  }

  .item:hover {
    background-color: #E4E7ED;
    cursor: pointer;
  }

  .item .m_l {
    width: 50px;
    float: left;
  }

  .item .m_l img {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: block;
    cursor: pointer;
    padding: 10px 0;
  }

  .m_r {
    margin-left: 80px;
    font-size: 14px;
  }

  .m_r p {
    color: #0000EE;
  }

  .user, .userInfo {
    border-bottom: 1px solid #E4E7ED;
  }

   .el-table .warning-row {
    background: oldlace;
  }

   .el-table .success-row {
    background: #f0f9eb;
  }

  .usermain {
    P {
      color: #1d77b4;
      font-size: 0.28125rem;
      margin: 0.234375rem 0;
      border-bottom: 1px solid #E4E7ED;
    }
  }

  .warning-alert {
    margin-bottom: 20px;
  }

</style>
