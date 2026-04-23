# -*- encoding: utf-8 -*-
"""
@File    :   CommentHeader.vue
@Contact :   cgs614074127@icloud.com
@License :   (C)Copyright 2022
@Author    @Version    @Description
-------    --------    -----------
jackie_chen      1.0         单条微博分析详情页面
"""
&lt;template&gt;
  &lt;div&gt;
    &lt;el-card class="box-card"&gt;
      &lt;div slot="header" class="clearfix"&gt;
        &lt;span class="title"&gt;微博分析&lt;/span&gt;
        &lt;router-link to="/comment"&gt;
          &lt;p class="title-analysis"&gt;继续分析&lt;/p&gt;
        &lt;/router-link&gt;
      &lt;/div&gt;

      &lt;div v-if="isMulti" class="multi-nav"&gt;
        &lt;el-button
          v-for="(wid, index) in weiboIds"
          :key="wid"
          size="small"
          :type="currentIndex === index ? 'primary' : ''"
          @click="currentIndex = index"
        &gt;{{index + 1}}. {{wid.substring(0, 10)}}...&lt;/el-button&gt;
      &lt;/div&gt;

      &lt;div class="mwbcon" v-if="currentData"&gt;
        &lt;div class="m_l v_yellow"&gt;
          &lt;img id="weiboContentUserHead" style="cursor: pointer;" :src="userInfo[0].fields.wb_user_profile_image_url"&gt;
        &lt;/div&gt;
        &lt;div class="m_r"&gt;
          &lt;p id="weiboContentUserNickname"&gt;
            &lt;a class="mscrame" href="javascript:;" @click="website(userId)" target="_blank"&gt;{{userInfo[0].fields.wb_userName}}&lt;/a&gt;
          &lt;/p&gt;
          &lt;div class="mwbcontext" id="weiboContentPic"&gt;
            &lt;p v-html="sanitizedUserText" ref="cvs"&gt;&lt;/p&gt;
            &lt;img v-for="(img, index) in userImg" :key="index" :src="setImg(img)" :class="imglen" preview="1"&gt;
          &lt;/div&gt;
          &lt;div class="mfont-buttom" id="weiboContentButtomTime" style="display: block;"&gt;
            &lt;div class="mfont-buttom_l" id="weiboContentTime" style="bottom: 20px;padding-top: 0px;"&gt;
              &lt;span style="cursor: pointer;" @click="website(wburl)"&gt;{{userInfo[0].fields.wb_created_at}}&lt;/span&gt;
              &lt;span&gt;分析时间: {{dateFormat(create_time)}}&lt;/span&gt;
              &lt;span v-if="userInfo[0].fields.wb_source"&gt;来自{{userInfo[0].fields.wb_source}}&lt;/span&gt;
            &lt;/div&gt;
            &lt;div class="mfont-buttom_r" style="bottom: 20px; right: 20px; z-index: 4;padding-top: 0px;"&gt;
              &lt;a class="weibo-multi-panel weibo-list-a" id="weiboContentForwardNumber"&gt;转发({{userInfo[0].fields.wb_reposts}})&lt;/a&gt;
              &lt;a class="weibo-multi-panel weibo-list-a" id="weiboContentCommentNumber"&gt;评论({{userInfo[0].fields.wb_comments}})&lt;/a&gt; |
              &lt;a class="weibo-multi-panel weibo-list-a" id="weiboContentPraiseNumber"&gt;赞({{userInfo[0].fields.wb_like}})&lt;/a&gt;
            &lt;/div&gt;
          &lt;/div&gt;
        &lt;/div&gt;
        &lt;div class="clear explain" id="weiboContentNote" style="display: block; bottom: 10px;"&gt;&lt;strong style="color:#B94A48"&gt;数据说明：&lt;/strong&gt;系统分析的数据来自微博的最高层级的转发及评论数据。&lt;/div&gt;
      &lt;/div&gt;

      &lt;div class="row-fluid" v-if="currentData"&gt;
        &lt;div class="mwbcon" id="all_dec"&gt;
          &lt;div class="well fz14" style="padding: 15px 2px;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important"&gt;
            截至分析时间&lt;strong id="analysis_time"&gt;{{dateFormat(create_time)}}&lt;/strong&gt;，@&lt;strong id="blogger"&gt;{{userInfo[0].fields.wb_userName}}&lt;/strong&gt; 的微博共收获转发数&lt;strong id="transNum"&gt;{{userInfo[0].fields.wb_reposts}}&lt;/strong&gt;次（其中有效转发&lt;strong id="repostsUserCount"&gt;{{userInfo[0].fields.wb_reposts}}&lt;/strong&gt;次）、
            评论数&lt;strong id="comment"&gt;{{userInfo[0].fields.wb_comments}}&lt;/strong&gt;条（其中有效评论&lt;strong id="repostsUserCount"&gt;{{commentInfo.length}}&lt;/strong&gt;条），点赞数&lt;strong id="likeNum"&gt;{{userInfo[0].fields.wb_like}}&lt;/strong&gt;个；@&lt;strong id="keyUserName"&gt;{{commentInfo[0]?.fields.c_userName}}&lt;/strong&gt; 评论微博并成为关键传播用户。
          &lt;/div&gt;
        &lt;/div&gt;
      &lt;/div&gt;

      &lt;div class="row-fluid" v-if="currentData"&gt;
        &lt;div class="mwbcon"&gt;
          &lt;p class="c-title"&gt;评论趋势图&lt;/p&gt;
        &lt;/div&gt;
        &lt;ve-line :data="commentchart" :settings="chartSettings"&gt;&lt;/ve-line&gt;
        &lt;div class="well fz14" style="padding: 15px 2px;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important"&gt;
           该微博始发于&lt;strong id="start_time"&gt;{{usercomment.commentqushi[10]?.date.replace(/"/g, '')}}&lt;/strong&gt;,于&lt;strong id="blogger"&gt;{{maxComment()}}&lt;/strong&gt;评论达到最高峰&lt;strong id="transNum"&gt;{{usercomment.commentqushi[10]?.count}}&lt;/strong&gt;
        &lt;/div&gt;
      &lt;/div&gt;

      &lt;div class="row-fluid" v-if="currentData"&gt;
        &lt;div class="mwbcon"&gt;
          &lt;p class="c-title"&gt;用户引爆点&lt;/p&gt;
        &lt;/div&gt;
        &lt;el-table :data="tableData" style="width: 100%" :row-class-name="tableRowClassName"&gt;
          &lt;el-table-column prop="date" label="时间" width="150"&gt;&lt;/el-table-column&gt;
          &lt;el-table-column prop="name" label="昵称" width="100"&gt;&lt;/el-table-column&gt;
          &lt;el-table-column prop="content" label="内容"&gt;&lt;/el-table-column&gt;
          &lt;el-table-column prop="like" label="点赞数" width="80"&gt;&lt;/el-table-column&gt;
        &lt;/el-table&gt;
      &lt;/div&gt;

      &lt;div class="row-fluid" v-if="currentData"&gt;
        &lt;div class="mwbcon"&gt;
          &lt;p class="c-title"&gt;评论词云&lt;/p&gt;
        &lt;/div&gt;
        &lt;ve-wordcloud :data="getRows()" :settings="chartSettings1" :showTooltip="true"&gt;&lt;/ve-wordcloud&gt;
        &lt;div class="well fz14" style="padding: 15px 2px;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important"&gt;
          该微博评论中&lt;strong id="analysis_time"&gt;{{usercomment.cipin[0]?.word}}&lt;/strong&gt;频率最高,达到
          &lt;strong id="blogger"&gt;{{usercomment.cipin[0]?.count}}&lt;/strong&gt;次。分别是&lt;strong id="analysis_time"&gt;
          {{usercomment.cipin[1]?.word}}、{{usercomment.cipin[2]?.word}}、{{usercomment.cipin[3]?.word}}&lt;/strong&gt;
          分别达到&lt;strong id="blogger"&gt;{{usercomment.cipin[1]?.count}}、{{usercomment.cipin[2]?.count}}、{{usercomment.cipin[3]?.count}}&lt;/strong&gt;次。
        &lt;/div&gt;
      &lt;/div&gt;

      &lt;div class="row-fluid" v-if="currentData"&gt;
        &lt;div class="mwbcon"&gt;
          &lt;p class="c-title"&gt;评论敏感率（当前敏感率只检测暴恐、反动、民生、色情等词汇）&lt;/p&gt;
        &lt;/div&gt;
        &lt;ve-bar :data="minganData()" height="3.4rem"&gt;&lt;/ve-bar&gt;
        &lt;div class="well fz14" style="padding: 15px 2px;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important"&gt;
          该评论中,敏感占比&lt;strong&gt;{{usercomment.mingan?.toFixed(2)}}%&lt;/strong&gt;,
          在&lt;strong&gt;
          &lt;span v-if="usercomment.mingan?.toFixed(2) &lt; 0.25"&gt;极低&lt;/span&gt;
            &lt;span v-else-if="usercomment.mingan?.toFixed(2) &gt;= 0.25 &amp;&amp; usercomment.mingan?.toFixed(2) &lt; 0.5"&gt;低&lt;/span&gt;
            &lt;span v-else-if="usercomment.mingan?.toFixed(2) &gt;= 0.5 &amp;&amp; usercomment.mingan?.toFixed(2) &lt; 0.75"&gt;高&lt;/span&gt;
            &lt;span v-else&gt;极高&lt;/span&gt;
        &lt;/strong&gt;敏感范围内
        &lt;/div&gt;
      &lt;/div&gt;

      &lt;div class="row-fluid" v-if="currentData"&gt;
        &lt;div class="mwbcon"&gt;
          &lt;p class="c-title"&gt;评论内容情感分析&lt;/p&gt;
          &lt;ve-histogram :data="chartData" :settings="chartSettings2"&gt;&lt;/ve-histogram&gt;
        &lt;/div&gt;
        &lt;div class="well fz14" style="padding: 15px 2px;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important"&gt;
          根据该微博评论的情感分析情况：
          消极评论最小值&lt;strong&gt;{{ emtionanaly.smalldate }}&lt;/strong&gt;
          ，次数是&lt;strong&gt;{{ emtionanaly.smallcount }}&lt;/strong&gt;;
          积极评论最大值&lt;strong&gt;{{ emtionanaly.bigdate }}&lt;/strong&gt;
           ，次数是&lt;strong&gt;{{ emtionanaly.bigcount }}&lt;/strong&gt;;
          最大的评论次数是&lt;strong&gt;{{ emtionanaly.maxcount }}&lt;/strong&gt;次
          ，情感值是&lt;strong&gt;{{ emtionanaly.maxdate }}&lt;/strong&gt;。
          全部评论中：消极评论内容占比&lt;strong&gt;{{ (emtionanaly.count0 / emtionanaly.len)*100 }}%&lt;/strong&gt;，
          积极评论内容占比&lt;strong&gt;{{ (emtionanaly.count1 / emtionanaly.len)*100 }}%&lt;/strong&gt;。
        &lt;/div&gt;
      &lt;/div&gt;
    &lt;/el-card&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script&gt;
import {mapState} from 'vuex'
import axios from 'axios'
import { api } from '@/api'

export default {
  name: 'CommentHeader',
  data () {
    this.chartSettings = {
      stack: { '用户': ['评论用户'] },
      area: true
    }
    this.chartSettings1 = {
      sizeMin: 30,
      sizeMax: 60
    }
    this.chartSettings2 = {
      metrics: ['次数'],
      dimension: ['情感值']
    }
    return {
      create_time: Date(),
      currentIndex: 0,
      chartData: {
        columns: ['情感值'],
        rows: []
      },
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
      usercomment: state =&gt; state.usercomment,
      tempid: state =&gt; state.tempids
    }),
    isMulti () {
      return !this.usercomment.data || !this.usercomment.info
    },
    weiboIds () {
      if (this.isMulti) {
        return Object.keys(this.usercomment)
      }
      return [this.tempid]
    },
    currentData () {
      if (this.isMulti) {
        return this.usercomment[this.weiboIds[this.currentIndex]]
      }
      return this.usercomment
    },
    userInfo () {
      return JSON.parse(this.currentData.data)
    },
    userId () {
      return 'https://m.weibo.cn/' + this.userInfo[0].fields.wb_userId
    },
    userText () {
      return this.userInfo[0].fields.wb_text?.replace('data-hide=""', 'target="_blank"').replace(/1rem/g, '.3rem') || ''
    },
    sanitizedUserText () {
      let text = this.userText
      text = text.replace(/&lt;script[^&gt;]*&gt;[\s\S]*?&lt;\/script&gt;/gi, '')
      text = text.replace(/&lt;iframe[^&gt;]*&gt;[\s\S]*?&lt;\/iframe&gt;/gi, '')
      text = text.replace(/&lt;form[^&gt;]*&gt;[\s\S]*?&lt;\/form&gt;/gi, '')
      text = text.replace(/&lt;input[^&gt;]*&gt;/gi, '')
      text = text.replace(/&lt;button[^&gt;]*&gt;[\s\S]*?&lt;\/button&gt;/gi, '')
      text = text.replace(/on\w+="[^"]*"/gi, '')
      text = text.replace(/on\w+='[^']*'/gi, '')
      return text
    },
    userImg () {
      const pics = this.userInfo[0].fields.wb_pic_ids
      try {
        return typeof pics === 'string' ? JSON.parse(pics) : pics || []
      } catch (e) {
        return []
      }
    },
    imglen () {
      const len = this.userImg.length
      if (len === 1) return 'wb-img1'
      if (len === 2) return 'wb-img2'
      return 'wb-img3'
    },
    wburl () {
      return 'https://m.weibo.cn/' + this.userInfo[0].fields.wb_userId + '/' + this.userInfo[0].pk
    },
    commentInfo () {
      return JSON.parse(this.currentData.info)
    },
    commentchart () {
      let mrows = []
      const qushi = this.currentData.commentqushi || []
      for (let i = 0; i &lt; 10 &amp;&amp; i &lt; qushi.length; i++) {
        mrows.push({
          '日期': qushi[i]?.date?.replace(/"/g, '') || '',
          '评论用户': qushi[i]?.count || 0
        })
      }
      return {
        columns: ['日期', '评论用户'],
        rows: mrows
      }
    },
    tableData () {
      let date = []
      for (let i = 0; i &lt; 10 &amp;&amp; i &lt; this.commentInfo.length; i++) {
        date.push({
          date: this.commentInfo[i]?.fields.c_created_at || '',
          name: this.commentInfo[i]?.fields.c_userName || '',
          content: this.commentInfo[i]?.fields.c_text || '',
          like: this.commentInfo[i]?.fields.c_like_num || 0
        })
      }
      return date
    }
  },
  watch: {
    currentIndex () {
      this.resetData()
      this.loadSentiments()
    }
  },
  mounted () {
    this.resetData()
    this.loadSentiments()
  },
  methods: {
    resetData () {
      this.chartData.rows = []
      this.emtionanaly = {
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
    },
    loadSentiments () {
      const currentId = this.isMulti ? this.weiboIds[this.currentIndex] : this.tempid
      this.$notify.info({
        title: '消息',
        message: '请稍后,正在计算最终情感结果',
        position: 'bottom-right'
      })
      axios.get(api.comment + '?&amp;commentId=' + currentId)
        .then((response) =&gt; {
          let rows = []
          const data = response.data
          this.emtionanaly.len = data.length || 1
          if (data.length &gt; 0) {
            this.emtionanaly.smalldate = data[0][0]
            this.emtionanaly.smallcount = data[0][1]
            this.emtionanaly.bigdate = data[data.length - 1][0]
            this.emtionanaly.bigcount = data[data.length - 1][1]
            for (let i = 0; i &lt; data.length; i++) {
              if (data[i][1] &gt; this.emtionanaly.maxcount) {
                this.emtionanaly.maxcount = data[i][1]
                this.emtionanaly.maxdate = data[i][0]
              }
              rows.push({
                '情感值': data[i][0],
                '次数': data[i][1]
              })
              if (data[i][0] &lt; 0.5) {
                this.emtionanaly.count0++
              } else {
                this.emtionanaly.count1++
              }
            }
          }
          this.chartData.rows = rows
          this.mopen()
        })
    },
    tableRowClassName ({row, rowIndex}) {
      if (rowIndex === 1) {
        return 'warning-row'
      } else if (rowIndex === 3) {
        return 'success-row'
      }
      return ''
    },
    website (url) {
      window.open(url)
    },
    setImg (src) {
      return '/static/' + src + '.jpg'
    },
    dateFormat () {
      let date = new Date()
      let year = date.getFullYear()
      let month = date.getMonth() + 1 &lt; 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1
      let day = date.getDate() &lt; 10 ? '0' + date.getDate() : date.getDate()
      let hours = date.getHours() &lt; 10 ? '0' + date.getHours() : date.getHours()
      let minutes = date.getMinutes() &lt; 10 ? '0' + date.getMinutes() : date.getMinutes()
      let seconds = date.getSeconds() &lt; 10 ? '0' + date.getSeconds() : date.getSeconds()
      return year + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds
    },
    maxComment () {
      const qushi = this.currentData.commentqushi || []
      for (let i = 0; i &lt; qushi.length; i++) {
        if (qushi[10]?.count === qushi[i]?.count) {
          return qushi[i]?.date?.replace(/"/g, '') || ''
        }
      }
      return ''
    },
    getRows () {
      let res = []
      const cipin = this.currentData.cipin || []
      for (let i = 0; i &lt; cipin.length; i++) {
        res.push({
          'word': cipin[i]?.word || '',
          'count': cipin[i]?.count || 0
        })
      }
      return {
        columns: ['word', 'count'],
        rows: res
      }
    },
    minganData () {
      const minganValue = parseFloat(this.currentData.mingan?.toFixed(2) || 0)
      return {
        columns: ['敏感程度', '敏感', '非敏感'],
        rows: [{
          '敏感程度': '敏感程度',
          '敏感': minganValue,
          '非敏感': 1 - minganValue
        }]
      }
    },
    mopen () {
      if (this.$refs.cvs &amp;&amp; this.$refs.cvs.innerText) {
        console.log(this.$refs.cvs.innerText)
        axios.get(api.snownlp + '?&amp;snownlp=' + this.$refs.cvs.innerText.replace(/#/g, ''))
          .then((response) =&gt; {
            console.log(response.data)
            let success = '积极😁'
            if (response.data.sentiments &gt; 0.5) {
              success = '积极😁'
            } else {
              success = '消极😭'
            }
            let pl = '消极偏多😭'
            if (this.emtionanaly.count0 &gt; this.emtionanaly.count1) {
              pl = '消极偏多😭'
            } else {
              pl = '积极偏多😁'
            }
            this.$notify({
              title: '成功',
              dangerouslyUseHTMLString: true,
              message: '微博情感值：' + response.data.sentiments + '&lt;br&gt;情感评定：' + success + '&lt;br&gt;关键词是：' + response.data.keywords + '&lt;br&gt;评论倾向：' + pl,
              type: 'success',
              position: 'bottom-right',
              duration: 0
            })
          })
      }
    }
  }
}
&lt;/script&gt;

&lt;style lang="css" scoped&gt;
  .clear {
    clear: both;
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
    width: 90%;
    position: relative;
    margin: 0 auto;
  }

  .title {
    font-size: 16px;
    padding: 15px 10px 15px 50px;
    margin: 0 0 10px;
    color: #fff;
    text-align: center;
    background-color: #F8661E;
    background-image: url('../../../assets/icon-wyq.png');
    background-repeat: no-repeat;
    background-position: 10px center;
    padding-left: 50px;
    border-radius: 3px;
  }

  .title-analysis {
    font-size: 17px;
    margin-left: 30px;
    display: inline-block;
    color: #1d77b4;
    margin-top: 10px;
    margin-bottom: 10px;
    cursor: pointer;
  }

  .title-analysis:hover {
    text-decoration: underline;
  }

  .multi-nav {
    margin: 20px 0;
    text-align: center;
  }

  .mwbcon .m_l &gt; img {
    width: 60px;
    height: 60px;
    border-radius: 50%;
  }

  img {
    margin: 0px;
    padding: 0px;
    list-style-type: none;
    border-style: none;
    vertical-align: middle;
    outline: none;
    border: 1px solid rgba(216, 134, 10, 0.2);
  }

  div {
    margin: 0 auto;
  }

  div.v_blue, div.v_yellow {
    position: relative;
  }

  div.v_yellow:after {
    background-image: url('../../../assets/v_yellow.png');
  }

  div.v_blue:after, div.v_yellow:after {
    content: "";
    text-align: center;
    width: 20px;
    height: 20px;
    position: absolute;
    bottom: -4px;
    left: 40px;
    background-position: center;
    background-repeat: no-repeat;
  }

  .mwbcon .m_r {
    margin-left: 80px;
    font-size: 14px;
  }

  p {
    margin: 0px;
    padding: 0px;
    border: currentColor;
    list-style-type: none;
  }

  .mwbcon {
    padding: 10px;
    overflow: hidden;
  }

  .mwbcon .m_l {
    width: 50px;
    float: left;
  }

  .mwbcontext {
    padding-top: 10px;
    line-height: 25px;
    font-size: 16px;
  }

  .mfont-buttom_l &gt; span {
    margin-right: 30px;
  }

  .mfont-buttom {
    color: #666;
    font-size: 12px;
    line-height: 30px;
    width: 100%;
    display: inline-block;
  }

  .mscrame {
    font-size: 18px;
  }

  .mfont-buttom_r {
    float: right;
  }

  .mfont-buttom_l {
    float: left;
  }

  .explain {
    font-size: 12px;
    color: #999;
    margin-top: 10px;
    display: inline-block;
    width: 100%;
  }

  .wb-img3 {
    margin: .2rem 0;
    width: 100px;
    height: 100px;
    cursor: pointer;
  }

  .wb-img2 {
    margin: .2rem 0;
    width: 150px;
    height: 150px;
    cursor: pointer;
  }

  .wb-img1 {
    margin: .2rem 0;
    max-width: 300px;
    cursor: pointer;
  }

  .row-fluid {
    border-bottom: 3px solid #e4e7ed;
  }

  .c-title {
    font-size: 18px;
    color: #1d77b4;
    margin: 15px 0;
  }

  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
&lt;/style&gt;
