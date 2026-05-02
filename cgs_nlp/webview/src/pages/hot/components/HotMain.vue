# -*- encoding: utf-8 -*-
"""
@File    :   HotMain.vue
@Contact :   cgs614074127@icloud.com
@License :   (C)Copyright 2022
@Author    @Version    @Desciption
-------    --------    -----------
jackie_chen      1.0         热度排名主页面
"""
<template>
  <div class="home-des">
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
                transform="translate(40.674608, 27.097010) rotate(60.000000) translate(-40.674608, -27.097010) ">
              </path>
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
      <span class="name">微博热度排名</span>
    </div>
    <div class="detail">
      按互动量（点赞+评论+转发）排序的热门微博
    </div>
    <div class="search">
      <el-input-number v-model="limit" :min="10" :max="100" :step="10" label="显示条数" style="margin: 0 10px;"></el-input-number>
      <el-button type="primary" @click="fetchHotTweets" :loading="loading">刷新</el-button>
    </div>
    <div class="hot-list">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>热门微博 TOP{{limit}}</span>
        </div>
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="!tweets.length" class="empty">暂无数据</div>
        <div v-else>
          <div v-for="(tweet, index) in tweets" :key="tweet.id" class="tweet-item">
            <div class="rank-badge" :class="'rank-' + (index + 1)">{{index + 1}}</div>
            <div class="tweet-content">
              <div class="tweet-text">{{tweet.content}}</div>
              <div class="tweet-meta">
                <span class="like"><i class="el-icon-thumb-up"></i> {{tweet.like}}</span>
                <span class="comment"><i class="el-icon-chat-dot-round"></i> {{tweet.comment}}</span>
                <span class="repost"><i class="el-icon-refresh-right"></i> {{tweet.transfer}}</span>
                <span class="total">互动: {{tweet.totalInteraction}}</span>
                <span class="sentiment" :class="tweet.sentiments > 0.5 ? 'positive' : 'negative'">
                  情感值: {{tweet.sentiments.toFixed(2)}}
                </span>
              </div>
              <div class="tweet-time">发布时间: {{tweet.pubTime}}</div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { api } from '@/api'

export default {
  name: 'HotMain',
  data () {
    return {
      limit: 20,
      tweets: [],
      loading: false
    }
  },
  mounted () {
    this.fetchHotTweets()
  },
  methods: {
    async fetchHotTweets () {
      this.loading = true
      try {
        const response = await axios.get(api.hot + '?limit=' + this.limit)
        if (response.data.success) {
          this.tweets = response.data.tweets
          this.$notify.success({
            title: '成功',
            message: '已获取 ' + this.tweets.length + ' 条热门微博',
            position: 'bottom-right'
          })
        }
      } catch (error) {
        this.$message.error('获取热度排名失败，请检查后台')
        console.error(error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style lang="css" scoped>
  .home-des {
    text-align: center;
    margin-top: 50px;
    padding-bottom: 50px;
  }

  .svg {
    vertical-align: middle;
  }

  .detail {
    vertical-align: middle;
    font-size: .28rem;
    margin-left: .24rem;
    font-weight: 200;
    color: #fff;
    margin-top: 20px;
  }

  .search {
    margin-top: 30px;
  }

  .name {
    vertical-align: middle;
    font-size: .48rem;
    margin-left: .24rem;
    font-weight: 200;
    color: #fff;
  }

  @-webkit-keyframes rotation {
    from {
      -webkit-transform: rotate(0deg);
    }

    to {
      -webkit-transform: rotate(360deg);
    }
  }

  .rotation {
    -webkit-transform: rotate(360deg);
    animation: rotation 3s linear infinite;
    -moz-animation: rotation 3s linear infinite;
    -webkit-animation: rotation 3s linear infinite;
    -o-animation: rotation 3s linear infinite;
    transform-origin: center center;
  }

  .hot-list {
    margin: 40px auto;
    max-width: 900px;
  }

  .box-card {
    width: 100%;
  }

  .loading, .empty {
    padding: 50px 0;
    color: #999;
    font-size: 16px;
  }

  .tweet-item {
    display: flex;
    padding: 20px 0;
    border-bottom: 1px solid #e4e7ed;
    align-items: flex-start;
  }

  .tweet-item:last-child {
    border-bottom: none;
  }

  .rank-badge {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: #fff;
    flex-shrink: 0;
    margin-right: 20px;
  }

  .rank-1 { background: linear-gradient(135deg, #ffd700, #ffaa00); }
  .rank-2 { background: linear-gradient(135deg, #c0c0c0, #a0a0a0); }
  .rank-3 { background: linear-gradient(135deg, #cd7f32, #b06f2a); }
  .rank-4, .rank-5, .rank-6, .rank-7, .rank-8, .rank-9, .rank-10 { background: linear-gradient(135deg, #667eea, #764ba2); }
  .rank-badge:not(.rank-1):not(.rank-2):not(.rank-3):not(.rank-4):not(.rank-5):not(.rank-6):not(.rank-7):not(.rank-8):not(.rank-9):not(.rank-10) {
    background: linear-gradient(135deg, #8a8a8a, #666);
  }

  .tweet-content {
    flex: 1;
    text-align: left;
  }

  .tweet-text {
    font-size: 15px;
    color: #333;
    margin-bottom: 10px;
    line-height: 1.6;
  }

  .tweet-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    font-size: 13px;
    color: #666;
    margin-bottom: 8px;
  }

  .tweet-meta span {
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .total {
    color: #409eff;
    font-weight: bold;
  }

  .positive {
    color: #67c23a;
  }

  .negative {
    color: #f56c6c;
  }

  .tweet-time {
    font-size: 12px;
    color: #999;
  }
</style>
