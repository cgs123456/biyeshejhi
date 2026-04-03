<template>
  <div class="user">
    <!-- 调试信息已注释 -->
    <div class="user-header">
      <div class="photo-warp">
        <img :src="this.img[0]" class="wb-img">
      </div>
      <div class="wb-name">
        <span class="name">{{this.userInfo[0].fields.NickName}}</span>
        <img :src="this.imgsex" class="sex">
        <div class="wb-brief">{{this.wbbrief}}</div>
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
                {{this.userInfo[0].fields.Num_Follows}}
              </div>
              <div class="text item item1">
                {{this.userInfo[0].fields.Num_Fans}}
              </div>
              <div class="text item">
                {{this.userInfo[0].fields.Num_Tweets}}
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
                <span v-if="this.srcs"><img v-for="src in this.srcs" :key="src" :src="src" class="wb-xz"></span>
                <span v-else>该用户没有勋章哦~</span>
              </div>
              <div class="text item3 item3-txt">
                所在地方
              </div>
              <div class="text item3-detail">
                {{this.userInfo[0].fields.Province}} {{this.userInfo[0].fields.City}}
              </div>
              <div class="text item3 item3-txt">
                生日/星座
              </div>
              <div class="text item3-detail" v-if="this.userInfo[0].fields.Birthday || this.userInfo[0].fields.Constellation">
                {{this.userInfo[0].fields.Birthday}} {{this.userInfo[0].fields.Constellation}}
              </div>
              <div class="text item3-detail" v-else>
                无
              </div>
              <div class="text item3 item3-txt">
                性取向
              </div>
              <div class="text item3-detail">
                <span v-if="this.userInfo[0].fields.SexOrientation">{{this.userInfo[0].fields.SexOrientation}}</span>
                <span v-else>无</span>
              </div>
              <div class="text item3 item3-txt">
                情感状态
              </div>
              <div class="text item3-detail">
                <span v-if="this.userInfo[0].fields.Sentiment">{{this.userInfo[0].fields.Sentiment}}</span>
                <span v-else>无</span>
              </div>
              <div class="text item3 item3-txt">
                VIP等级
              </div>
              <div class="text item3-detail">
                <span v-if="this.userInfo[0].fields.VIPlevel">{{this.userInfo[0].fields.VIPlevel}}</span>
                <span v-else>无</span>
              </div>
              <div class="text item3 item3-txt">
                认证
              </div>
              <div class="text item3-detail">
                <span v-if="this.userInfo[0].fields.Authentication">{{this.userInfo[0].fields.Authentication}}</span>
                <span v-else>无</span>
              </div>
              <div class="text item3 item3-txt">
                主页
              </div>
              <div class="text item3-detail">
                <a :href='this.userInfo[0].fields.URL' target="_blank" class="index">{{this.userInfo[0].fields.NickName}}</a>
              </div>
            </el-card>
            <el-card class="box-card-detail ciyun">
              <div slot="header" class="clearfix">
                <span>词云展示</span>
                <el-button style="float: right; padding: 3px 0" type="text"></el-button>
              </div>
              <div v-if="this.chartData ==='' " style="padding: 0.3125rem;">词云加载中...</div>
              <div v-else>
                <ve-wordcloud :data="chartData" :settings="chartSettings"></ve-wordcloud>
                <div class="well fz14" style="padding: 0.3125rem;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important">
                  用户@<strong>{{this.userInfo[0].fields.NickName}}</strong>的微博内容中，词云分析结果如上图所示，其中
                  <strong>{{this.chartData.rows[0].word}}</strong>的频率最高，达到
                  <strong>{{this.chartData.rows[0].count}}</strong>次，其次是
                  <strong>{{this.chartData.rows[1].word}}</strong>、
                  <strong>{{this.chartData.rows[2].word}}</strong>、
                  <strong>{{this.chartData.rows[3].word}}</strong>分别达到
                  <strong>{{this.chartData.rows[1].count}}</strong>、
                  <strong>{{this.chartData.rows[2].count}}</strong>、
                  <strong>{{this.chartData.rows[3].count}}</strong>次。
                </div>
              </div>
            </el-card>
            <el-card class="box-card-detail ciyun">
              <div slot="header" class="clearfix">
                <span>敏感率</span>
                <el-button style="float: right; padding: 3px 0" type="text"></el-button>
              </div>
              <div v-if="this.minganData === '' || !this.minganData.rows || this.minganData.rows.length === 0" style="padding: 0.3125rem;">敏感率加载中...</div>
              <div v-else>
                <ve-bar :data="this.minganData" height="3.4rem" style="margin-top: .3125rem;"></ve-bar>
                <div class="well fz14" style="padding: 0.3125rem;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important">
                  用户@<strong>{{this.userInfo[0].fields.NickName}}</strong>的微博内容中，敏感占比（当前敏感率只检测暴恐、反动、民生、色情等词汇）
                  <strong>{{this.minganData.rows[0].敏感*100}}%</strong>,
                  在<strong>
                    <span v-if="this.minganData.rows[0].敏感 < 0.25">极低</span>
                    <span v-else-if="this.minganData.rows[0].敏感 >= 0.25 && this.minganData.rows[0].敏感 < 0.5">低</span>
                    <span v-else-if="this.minganData.rows[0].敏感 >= 0.5  && this.minganData.rows[0].敏感 < 0.75">高</span>
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
              <div v-if="this.textchartData ==='' " style="padding: 0.3125rem;">情感分析结果加载中...</div>
              <div v-else>
                <ve-line :data="textchartData" style="margin-top: .3125rem;"></ve-line>
                <div class="well fz14" style="padding: 0.3125rem;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important">
                  用户@<strong>{{this.userInfo[0].fields.NickName}}</strong>的微博内容中，
                  总微博条数<strong>{{this.userInfo[0].fields.Num_Tweets}}</strong>条，
                  经过处理得到有效微博条数<strong>{{this.emtionanaly.len}}</strong>条。有效微博情感分析结果如上图所示，
                  其中消极评论最小值<strong>{{ this.emtionanaly.smalldate }}</strong>
                  ，次数是<strong>{{ this.emtionanaly.smallcount }}</strong>；
                  积极评论最大值<strong>{{ this.emtionanaly.bigdate }}</strong>
                  ，次数是<strong>{{ this.emtionanaly.bigcount }}</strong>；
                  最大的评论次数是<strong>{{ this.emtionanaly.maxcount }}</strong>次
                  ，情感值是<strong>{{ this.emtionanaly.maxdate }}</strong>。
                  全部评论中：消极评论内容占比<strong>{{ (this.emtionanaly.count0 / this.emtionanaly.len)*100 }}%</strong>，
                  积极评论内容占比<strong>{{ (this.emtionanaly.count1 / this.emtionanaly.len)*100 }}%</strong>。
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
                <el-button style="float: right; padding: 3px 0" type="text"></el-button>
              </div>
              <div v-for="(tweet, index) in this.userTweets" :key="index" style="height:auto">
                <div class="tweets-header">
                  <div class="wb-id">
                    <span>微博ID：{{tweet.pk}}</span>
                    <!-- 爬取的微博编号，以目前的系统框架不可跳转到原微博 -->
                    <el-button style="float: right; padding: 3px 0" type="text">{{tweet.fields.PubTime}} </el-button>
                  </div>
                  <div class="wb-content">
                    <i class="el-icon-edit write"></i>{{tweet.fields.Content}}
                  </div>
                  <div class="wb-add">
                    <span>
                      定位：{{tweet.fields.Co_oridinates}}
                      来自{{tweet.fields.Tools}}
                    </span>
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
            </el-card>
          </div>
        </div>
      </el-col>
    </el-row>
    <div class="page" ref="page">
      <el-pagination @current-change="handleCurrentChange" :current-page.sync="currentPage" :page-size="this.size"
        layout="prev, pager, next" :total='this.total'>
      </el-pagination>
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
      mytweets: this.$store.state.usertweets,
      srcs: this.msrcs(),
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
      total: state => state.total
    }),
    userInfo: function () {
      return eval('(' + this.user + ')')
    },
    userTweets: function () {
      return eval('(' + this.mytweets + ')')
    },
    img: function () {
      return eval('(' + this.userInfo[0].fields.Image + ')')
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
    }
  },
  methods: {
    format (sentiments) {
      return '情感积极'
    },
    format1 (sentiments) {
      return '情感消极'
    },
    msrcs: function () {
      if (this.imglen > 1) {
        return this.img.splice(1)
      } else {
        return 0
      }
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
        axios.get('http://localhost:8000/wordcloudapi?&weiboId=' + this.weiboId)
          .then((response) => {
            let res = []
            for (let i = 0; i < response.data.cipin.length; i++) {
              res.push({
                'word': response.data.cipin[i].word,
                'count': response.data.cipin[i].count
              })
            }
            let chartData = {
              columns: ['word', 'count'],
              rows: res
            }
            this.chartData = chartData
            let mingan = {
              columns: ['敏感率', '敏感', '非敏感'],
              rows: [
                { '敏感率': '敏感率', '敏感': parseFloat(response.data.mingan.toFixed(2)), '非敏感': parseFloat((1 - response.data.mingan).toFixed(2)) }
              ]
            }
            this.minganData = mingan
            
            // 情感分析折线图
            let tu = eval('(' + response.data.tu + ')')
            this.emtionanaly.len = tu.length
            this.emtionanaly.smalldate = tu[0][0]
            this.emtionanaly.smallcount = tu[0][1]
            this.emtionanaly.bigdate = tu[tu.length - 1][0]
            this.emtionanaly.bigcount = tu[tu.length - 1][1]
            let tures = []
            for (let i = 0; i < tu.length; i++) {
              if (tu[i][1] > this.emtionanaly.maxcount) {
                this.emtionanaly.maxcount = tu[i][1]
                this.emtionanaly.maxdate = tu[i][0]
              }
              tures.push({
                '情感值': tu[i][0].substring(0, 4),
                '次数': tu[i][1]
              })
              if (tu[i][0] < 0.5) {
                this.emtionanaly.count0++
              } else {
                this.emtionanaly.count1++
              }
            }
            let textchartData = {
              columns: ['情感值', '次数'],
              rows: tures
            }
            this.textchartData = textchartData
            let pl = '消极偏多😭'
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
      axios.post('http://localhost:8000/tweetsapi/',
        Qs.stringify({
          weiboId: this.weiboId,
          page: val
        })
      ).then((response) => {
        this.$store.state.usertweets = response.data.data
        this.mytweets = response.data.data
      })
    },
    ...mapMutations(['changeUserTweets'])
  },
  mounted () {
    this.open()
  }
}
</script>

<style lang="css" scoped>
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
    }
  }
}
</style>
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

    .page {
      text-align: right;
      position: relative;
      bottom: 0;
      z-index: 3;
    }
  }

  .index {
    text-decoration: none;
  }

  .ciyun {
     .el-card__body {
      padding: 0;
    }
  }

</style>