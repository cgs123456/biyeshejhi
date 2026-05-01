<template>
  <div>
    <div v-if="!hasData" class="no-data">
      <el-card style="text-align: center; padding: 40px;">
        <i class="el-icon-warning" style="font-size: 48px; color: #E6A23C;"></i>
        <p style="font-size: 18px; margin-top: 20px;">暂无用户数据</p>
        <p style="color: #999;">请先在首页输入微博用户ID进行搜索</p>
        <el-button type="primary" style="margin-top: 20px;" @click="$router.push('/')">返回首页</el-button>
      </el-card>
    </div>
    <div class="user" v-else>
      <div class="user-header">
        <div class="photo-warp">
          <img :src="img[0]" class="wb-img">
        </div>
        <div class="wb-name">
          <span class="name">{{userInfo[0].fields.NickName}}</span>
          <img :src="imgsex" class="sex">
          <div class="wb-brief">{{wbbrief}}</div>
        </div>
      </div>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="grid-content bg-purple">
            <div class="info-left">
              <el-card class="box-card">
                <div slot="header" class="clearfix">
                  <span>关注 | 粉丝 | 微博数</span>
                  <el-button style="float: right; padding: 3px 0" type="text"></el-button>
                </div>
                <div class="text item item1">
                  {{userInfo[0].fields.Num_Follows}}
                </div>
                <div class="text item item1">
                  {{userInfo[0].fields.Num_Fans}}
                </div>
                <div class="text item">
                  {{userInfo[0].fields.Num_Tweets}}
                </div>
                <div class="text item item2">关注数</div>
                <div class="text item item2">粉丝数</div>
                <div class="text item item2">微博数</div>
              </el-card>
              <el-card class="box-card-detail">
                <div slot="header" class="clearfix">
                  <span>基本信息</span>
                </div>
                <div class="text item3 item3-txt">
                  微博勋章
                </div>
                <div class="text item3-detail">
                  <span v-if="srcs"><img v-for="src in srcs" :key="src" :src="src" class="wb-xz"></span>
                  <span v-else>该用户没有勋章哦~</span>
                </div>
                <div class="text item3 item3-txt">
                  所在地方
                </div>
                <div class="text item3-detail">
                  {{userInfo[0].fields.Province}} {{userInfo[0].fields.City}}
                </div>
                <div class="text item3 item3-txt">
                  生日/星座
                </div>
                <div class="text item3-detail" v-if="userInfo[0].fields.Birthday || userInfo[0].fields.Constellation">
                  {{userInfo[0].fields.Birthday}} {{userInfo[0].fields.Constellation}}
                </div>
                <div class="text item3-detail" v-else>
                  无
                </div>
                <div class="text item3 item3-txt">
                  性取向
                </div>
                <div class="text item3-detail">
                  <span v-if="userInfo[0].fields.SexOrientation">{{userInfo[0].fields.SexOrientation}}</span>
                  <span v-else>无</span>
                </div>
                <div class="text item3 item3-txt">
                  情感状态
                </div>
                <div class="text item3-detail">
                  <span v-if="userInfo[0].fields.Sentiment">{{userInfo[0].fields.Sentiment}}</span>
                  <span v-else>无</span>
                </div>
                <div class="text item3 item3-txt">
                  VIP等级
                </div>
                <div class="text item3-detail">
                  <span v-if="userInfo[0].fields.VIPlevel">{{userInfo[0].fields.VIPlevel}}</span>
                  <span v-else>无</span>
                </div>
                <div class="text item3 item3-txt">
                  认证
                </div>
                <div class="text item3-detail">
                  <span v-if="userInfo[0].fields.Verified_reason">{{userInfo[0].fields.Verified_reason}}</span>
                  <span v-else>无</span>
                </div>
                <div class="text item3 item3-txt">
                  主页
                </div>
                <div class="text item3-detail">
                  <a :href='userInfo[0].fields.URL' target="_blank" class="index">{{userInfo[0].fields.NickName}}</a>
                </div>
              </el-card>
              <el-card class="box-card-detail ciyun">
                <div slot="header" class="clearfix">
                  <span>词云展示</span>
                  <el-button style="float: right; padding: 3px 0" type="text"></el-button>
                </div>
                <div v-if="chartData ==='' " style="padding: 0.3125rem;">词云加载中...</div>
                <div v-else>
                  <ve-wordcloud
                    :data="chartData"
                    :settings="chartSettings"
                    @click="handleWordClick">
                  </ve-wordcloud>
                  <div v-if="filterWord" class="filter-banner">
                    <el-alert
                      :title="'当前筛选词: ' + filterWord"
                      type="info"
                      :closable="true"
                      @close="clearFilter">
                      <span>显示包含该词的微博</span>
                    </el-alert>
                  </div>
                  <div class="well fz14" style="padding: 0.3125rem;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important">
                    用户@<strong>{{userInfo[0].fields.NickName}}</strong>的微博内容中，词云分析结果如上图所示，其中
                    <strong>{{chartData.rows[0] ? chartData.rows[0].word : '无'}}</strong>的频率最高，达到
                    <strong>{{chartData.rows[0] ? chartData.rows[0].count : 0}}</strong>次，其次是
                    <strong>{{chartData.rows[1] ? chartData.rows[1].word : ''}}</strong>、
                    <strong>{{chartData.rows[2] ? chartData.rows[2].word : ''}}</strong>、
                    <strong>{{chartData.rows[3] ? chartData.rows[3].word : ''}}</strong>分别达到
                    <strong>{{chartData.rows[1] ? chartData.rows[1].count : 0}}</strong>、
                    <strong>{{chartData.rows[2] ? chartData.rows[2].count : 0}}</strong>、
                    <strong>{{chartData.rows[3] ? chartData.rows[3].count : 0}}</strong>次。
                  </div>
                </div>
              </el-card>
              <el-card class="box-card-detail ciyun">
                <div slot="header" class="clearfix">
                  <span>敏感率</span>
                  <el-button style="float: right; padding: 3px 0" type="text"></el-button>
                </div>
                <div v-if="minganData === '' || !minganData.rows || minganData.rows.length === 0" style="padding: 0.3125rem;">敏感率加载中...</div>
                <div v-else>
                  <ve-bar :data="minganData" height="3.4rem" style="margin-top: .3125rem;"></ve-bar>
                  <div class="well fz14" style="padding: 0.3125rem;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important">
                    用户@<strong>{{userInfo[0].fields.NickName}}</strong>的微博内容中，敏感占比（当前敏感率只检测暴恐、反动、民生、色情等词汇）
                    <strong>{{minganData.rows[0]['敏感'] * 100}}%</strong>,
                    在<strong>
                      <span v-if="minganData.rows[0].敏感 < 0.25">极低</span>
                      <span v-else-if="minganData.rows[0].敏感 >= 0.25 && minganData.rows[0].敏感 < 0.5">低</span>
                      <span v-else-if="minganData.rows[0].敏感 >= 0.5  && minganData.rows[0].敏感 < 0.75">高</span>
                      <span v-else>极高</span>
                    </strong>敏感范围内。
                  </div>
                </div>
              </el-card>
              <el-card class="box-card-detail ciyun">
                <div slot="header" class="clearfix">
                  <span>情感分析折线图</span>
                  <el-button style="float: right; padding: 3px 0" type="text"></el-button>
                </div>
                <div v-if="textchartData ==='' " style="padding: 0.3125rem;">情感分析结果加载中...</div>
                <div v-else>
                  <ve-line :data="textchartData" style="margin-top: .3125rem;"></ve-line>
                  <div class="well fz14" style="padding: 0.3125rem;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important">
                    用户@<strong>{{userInfo[0].fields.NickName}}</strong>的微博内容中，
                    总微博条数<strong>{{userInfo[0].fields.Num_Tweets}}</strong>条，
                    经过处理得到有效微博条数<strong>{{emtionanaly.len}}</strong>条。有效微博情感分析结果如上图所示，
                    其中消极评论最小值<strong>{{ emtionanaly.smalldate }}</strong>
                    ，次数是<strong>{{ emtionanaly.smallcount }}</strong>；
                    积极评论最大值<strong>{{ emtionanaly.bigdate }}</strong>
                    ，次数是<strong>{{ emtionanaly.bigcount }}</strong>；
                    最大的评论次数是<strong>{{ emtionanaly.maxcount }}</strong>次
                    ，情感值是<strong>{{ emtionanaly.maxdate }}</strong>。
                    全部评论中：消极评论内容占比<strong>{{ emtionanaly.len > 0 ? ((emtionanaly.count0 / emtionanaly.len)*100).toFixed(2) : 0 }}%</strong>，
                    积极评论内容占比<strong>{{ emtionanaly.len > 0 ? ((emtionanaly.count1 / emtionanaly.len)*100).toFixed(2) : 0 }}%</strong>。
                  </div>
                </div>
              </el-card>
            </div>
          </div>
        </el-col>
        <el-col :span="16">
          <div class="grid-content bg-purple">
            <div class="info-right" ref="element">
              <el-card class="box-card">
                <div slot="header" class="clearfix">
                  <span>微博内容情感分析</span>
                  <div style="float: right;">
                    <el-date-picker
                      v-model="dateRange"
                      type="daterange"
                      range-separator="至"
                      start-placeholder="开始日期"
                      end-placeholder="结束日期"
                      value-format="yyyy-MM-dd"
                      style="margin-right: 10px; width: 350px;"
                      @change="handleDateChange">
                    </el-date-picker>
                    <el-button type="info" size="mini" icon="el-icon-refresh" @click="resetFilter">重置筛选</el-button>
                    <el-button type="primary" size="mini" icon="el-icon-download" @click="exportTweets">导出微博数据</el-button>
                    <el-button type="success" size="mini" icon="el-icon-document" @click="exportUserInfo">导出用户信息</el-button>
                  </div>
                </div>
                <div v-for="(tweet, index) in filteredTweets" :key="index" style="height:auto">
                  <div class="tweets-header">
                    <div class="wb-id">
                      <span>微博ID：{{tweet.pk}}</span>
                      <el-button style="float: right; padding: 3px 0" type="text">{{tweet.fields.PubTime}} </el-button>
                    </div>
                    <div class="wb-content">
                      <i class="el-icon-edit write"></i>
                      <span v-if="!filterWord">{{tweet.fields.Content}}</span>
                      <span v-else v-html="highlightText(tweet.fields.Content)"></span>
                    </div>
                    <div class="wb-add">
                      <span>来自 {{tweet.fields.PubTools}}</span>
                      <button class="el-button el-button--default el-button--small el-b">点赞{{tweet.fields.Like}}</button>
                      <button class="el-button el-button--default el-button--small el-b">评论{{tweet.fields.Comment}}</button>
                      <button class="el-button el-button--default el-button--small el-b">转发{{tweet.fields.Transfer}}</button>
                    </div>
                  </div>
                  <div class="tweets-footer clearfix">
                    <div class="footer-left">
                      关键字：
                      <span v-if="tweet.fields.sentiments>0.5" style="background:#c2e7b0">
                        {{tweet.fields.tags}}
                      </span>
                      <span v-else style="background:#fbc4c4">
                        {{tweet.fields.tags}}
                      </span>
                      <br>
                      情感数值：{{tweet.fields.sentiments}}
                      <br>
                      词性：{{tweet.fields.pinyin}}
                    </div>
                    <div class="footer-right">
                      <el-progress class="progress" v-if="tweet.fields.sentiments>0.5" type="circle"
                        :percentage="tweet.fields.sentiments*100" color="#13ce66" :format="format"></el-progress>
                      <el-progress class="progress" v-else type="circle" :percentage="tweet.fields.sentiments*100"
                        color="#ff4949" :format="format1"></el-progress>
                    </div>
                  </div>
                  <hr style="background-color:#50bfff;height:1px;border:none;">
                </div>
                <div v-if="filterWord && filteredTweets.length === 0" style="text-align: center; padding: 30px; color: #999;">
                  <i class="el-icon-search" style="font-size: 40px; margin-bottom: 15px;"></i>
                  <p>没有找到包含"{{filterWord}}"的微博</p>
                  <el-button type="primary" size="small" @click="clearFilter">清除筛选</el-button>
                </div>
              </el-card>
            </div>
          </div>
        </el-col>
      </el-row>
      <div class="page" ref="page">
        <el-pagination @current-change="handleCurrentChange" :current-page.sync="currentPage" :page-size="size"
          layout="prev, pager, next" :total='total'>
        </el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import {
  mapState,
  mapMutations
} from 'vuex'
import axios from 'axios'
import Qs from 'qs'
import { api } from '@/api'
export default {
  name: 'UserHeader',
  data () {
    this.chartSettings = {
      sizeMin: 20,
      sizeMax: 40
    }
    return {
      textchartData: '',
      chartData: '',
      minganData: '',
      imgObj: {
        sexman: require('@/assets/sex-m.png'),
        sexwoman: require('@/assets/sex-f.png')
      },
      size: 20,
      currentPage: 1,
      dateRange: [],
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
      user: state => state.user,
      total: state => state.total,
      mytweets: state => state.usertweets
    }),
    hasData () {
      if (!this.user || this.user === '[]' || this.user === 'null') return false
      try {
        var parsed = JSON.parse(this.user)
        return parsed && parsed.length > 0
      } catch (e) {
        return false
      }
    },
    userInfo: function () {
      try {
        return JSON.parse(this.user)
      } catch (e) {
        return []
      }
    },
    userTweets: function () {
      try {
        return JSON.parse(this.mytweets)
      } catch (e) {
        return []
      }
    },
    img: function () {
      try {
        return JSON.parse(this.userInfo[0].fields.Image)
      } catch (e) {
        return []
      }
    },
    imglen: function () {
      return this.img.length
    },
    weiboId: function () {
      return this.userInfo[0].pk
    },
    imgsex: function () {
      if (this.userInfo[0].fields.Gender === '男') {
        return this.imgObj.sexman
      } else {
        return this.imgObj.sexwoman
      }
    },
    wbbrief: function () {
      if (this.userInfo[0].fields.BriefIntroduction === '' || this.userInfo[0].fields.BriefIntroduction === null) {
        return '一句话介绍自己，让别人更了解你'
      } else {
        return this.userInfo[0].fields.BriefIntroduction
      }
    },
    srcs: function () {
      if (this.imglen > 1) {
        return this.img.slice(1)
      } else {
        return 0
      }
    },
    filteredTweets () {
      if (!this.filterWord) {
        return this.userTweets
      }
      return this.userTweets.filter(tweet => {
        if (!tweet.fields.Content) return false
        return tweet.fields.Content.includes(this.filterWord)
      })
    }
  },
  methods: {
    handleWordClick (e) {
      if (e && e.data && e.data.name) {
        this.filterWord = e.data.name
        this.$message.success('已筛选包含"' + e.data.name + '"的微博')
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
    handleDateChange (val) {
      this.currentPage = 1
      this.loadTweets()
    },
    resetFilter () {
      this.dateRange = []
      this.filterWord = ''
      this.currentPage = 1
      this.loadTweets()
    },
    loadTweets () {
      var params = {
        weiboId: this.weiboId,
        page: this.currentPage
      }
      if (this.dateRange && this.dateRange.length === 2) {
        params.start_date = this.dateRange[0]
        params.end_date = this.dateRange[1]
        this.$message.info('正在筛选 ' + this.dateRange[0] + ' 至 ' + this.dateRange[1] + ' 的微博...')
      } else {
        this.$message.info('正在加载所有微博...')
      }
      axios.post(api.tweets, Qs.stringify(params))
        .then((response) => {
          this.$store.state.usertweets = response.data.data
          if (this.dateRange && this.dateRange.length === 2) {
            this.open()
          }
        })
        .catch((error) => {
          this.$message.error('加载微博数据失败')
          console.error(error)
        })
    },
    exportTweets () {
      var url = api.export.tweets + '?weiboId=' + this.weiboId
      window.open(url, '_blank')
      this.$message.success('正在导出微博数据...')
    },
    exportUserInfo () {
      var url = api.export.user + '?weiboId=' + this.weiboId
      window.open(url, '_blank')
      this.$message.success('正在导出用户信息...')
    },
    format (sentiments) {
      return '情感积极'
    },
    format1 (sentiments) {
      return '情感消极'
    },
    open () {
      if (this.user === '' || this.user === null || this.mytweets === '' || this.mytweets === null) {
        this.$notify.error({
          title: '信息错误',
          message: '你似乎来到知识的荒原~',
          position: 'bottom-right'
        })
      } else {
        this.$notify.info({
          title: '消息',
          message: '后台抓取用户所有信息开始生成词云',
          position: 'bottom-right'
        })
        axios.get(api.wordcloud + '?&weiboId=' + this.weiboId)
          .then((response) => {
            var res = []
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
            var mingan = {
              columns: ['敏感率', '敏感', '非敏感'],
              rows: [
                { '敏感率': '敏感率', '敏感': parseFloat(response.data.mingan.toFixed(2)), '非敏感': parseFloat((1 - response.data.mingan).toFixed(2)) }
              ]
            }
            this.minganData = mingan

            var tu = JSON.parse(response.data.tu)
            this.emtionanaly.len = tu.length
            this.emtionanaly.smalldate = tu[0][0]
            this.emtionanaly.smallcount = tu[0][1]
            this.emtionanaly.bigdate = tu[tu.length - 1][0]
            this.emtionanaly.bigcount = tu[tu.length - 1][1]
            var tures = []
            for (var j = 0; j < tu.length; j++) {
              if (tu[j][1] > this.emtionanaly.maxcount) {
                this.emtionanaly.maxcount = tu[j][1]
                this.emtionanaly.maxdate = tu[j][0]
              }
              tures.push({
                '情感值': tu[j][0].substring(0, 4),
                '次数': tu[j][1]
              })
              if (tu[j][0] < 0.5) {
                this.emtionanaly.count0++
              } else {
                this.emtionanaly.count1++
              }
            }
            var textchartData = {
              columns: ['情感值', '次数'],
              rows: tures
            }
            this.textchartData = textchartData
            var pl = '消极偏多😭'
            if (this.emtionanaly.count0 > this.emtionanaly.count1) {
              pl = '消极偏多😭'
            } else {
              pl = '积极偏多😁'
            }
            this.$notify({
              message: '整体情感评定：' + pl,
              type: 'success',
              position: 'bottom-right'
            })
          })
      }
    },
    handleCurrentChange (val) {
      console.log(val)
      this.currentPage = val
      this.loadTweets()
    },
    ...mapMutations(['changeUserTweets'])
  },
  mounted () {
    if (this.hasData) {
      this.open()
    }
  }
}
</script>

<style lang="css" scoped>
.no-data {
  padding: 100px 200px;
}

.user {
  padding: 0 100px 0 100px;
  margin-bottom: 20px;
  margin: 0 auto;
  max-width: 1100px;
  min-width: 1000px;

  .user-header {
    width: 100%;
    text-align: center;
    height: 200px;

    .photo-warp {
      width: 120px;
      height: 120px;
      margin: 0 auto;
      border: 1px solid #fff;
      background: rgba(255, 255, 255, 0.3);
      border-radius: 50%;
      position: relative;

      .wb-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        display: block;
      }
    }

    .wb-name {
      margin-top: 5px;

      .name {
        vertical-align: middle;
        color: #fff;
        font-size: .35rem;
      }

      .sex {
        width: 30px;
        height: 30px;
        vertical-align: middle;
      }

      .wb-brief {
        margin-top: 10px;
        color: #fff;
        font-size: .2rem;
      }
    }
  }

  .info-left {
    font-size: .2rem;

    .text {
      font-size: 18px;
    }

    .item {
      margin-bottom: 3px;
      width: 33%;
      float: left;
      text-align: center;
    }

    .item3 {
      margin-bottom: 10px;
      width: 30%;
      float: left;
      text-align: center;
    }

    .item3-detail {
      margin-bottom: 10px;
      width: 70%;
      float: left;
      text-align: center;
    }

    .wb-xz {
      width: 22px;
      height: 22px;
    }

    .item3-txt {
      color: #808080;
    }

    .item1 {
      border-right: 1px solid #c2c2c2;
    }

    .item2 {
      color: #808080;
      margin-bottom: 10px;
    }

    .clearfix:before,
    .clearfix:after {
      display: table;
      content: "";
    }

    .clearfix:after {
      clear: both;
    }

    .box-card {
      width: 100%;
    }

    .box-card-detail {
      width: 100%;
      margin-top: 30px;
      .avatar {
        width: 100%;
      }
    }
  }

  .info-right {
    margin-left: 3%;
    vertical-align: top;
    font-size: .2rem;

    .tweets-header {
      .wb-id {
        font-size: 14px;
        color: #808080;
      }

      .wb-content {
        margin: 10px 0;
        font-size: 15px;

        .write {
          color: #409EFF;
          width: 22px;
          height: 22px;
        }
      }

      .wb-add {
        text-align: right;
        color: #808080;

        span {
          margin-right: 10px;
        }
      }
    }

    .tweets-footer {
      border-left: 5px solid #50bfff;
      height: 105px;
      margin: 10px 0;
      padding: 10px;
      position: relative;

      .footer-left {
        overflow: hidden;
        height: 105px;
        width: 75%;
      }

      .footer-right {
        position: absolute;
        top: -.2rem;
        right: 0;
        width: 25%;

        .progress {
          transform: scale(.7);
        }
      }
    }
  }

  .page {
    text-align: right;
    position: relative;
    bottom: 0;
    z-index: 3;
  }

  .index {
    text-decoration: none;
  }

  .ciyun {
     .el-card__body {
      padding: 0;
    }
  }
}

</style>
