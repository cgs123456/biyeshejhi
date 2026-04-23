# -*- encoding: utf-8 -*-
"""
@File    :   Header.vue
@Contact :   cgs614074127@icloud.com
@License :   (C)Copyright 2022
@Author    @Version    @Description
-------    --------    -----------
jackie_chen      1.0         页面头部样式
"""
&lt;template&gt;
  &lt;div class="header-wrapper"&gt;
    &lt;div class="nav-links"&gt;
      &lt;router-link to="/"&gt;
        &lt;p&gt;个人微博分析首页&lt;/p&gt;
      &lt;/router-link&gt;
      &lt;router-link to="/comment"&gt;
        &lt;p&gt;单条微博分析首页&lt;/p&gt;
      &lt;/router-link&gt;
      &lt;router-link to="/hot"&gt;
        &lt;p&gt;热度排名&lt;/p&gt;
      &lt;/router-link&gt;
      &lt;router-link to="/crawler"&gt;
        &lt;p&gt;微博持续爬虫&lt;/p&gt;
      &lt;/router-link&gt;
      &lt;router-link to="/analysis"&gt;
        &lt;p&gt;自定义文本分析&lt;/p&gt;
      &lt;/router-link&gt;
      &lt;router-link to="/mycrawler"&gt;
        &lt;p&gt;已爬虫用户和微博&lt;/p&gt;
      &lt;/router-link&gt;
    &lt;/div&gt;
    &lt;div class="user-area"&gt;
      &lt;template v-if="isLoggedIn"&gt;
        &lt;span class="user-name"&gt;{{ user?.nickname || user?.username }}&lt;/span&gt;
        &lt;el-button type="text" class="logout-btn" @click="handleLogout"&gt;登出&lt;/el-button&gt;
      &lt;/template&gt;
      &lt;template v-else&gt;
        &lt;el-button type="text" @click="$emit('openLogin')"&gt;登录&lt;/el-button&gt;
        &lt;el-button type="text" @click="$emit('openRegister')"&gt;注册&lt;/el-button&gt;
      &lt;/template&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script&gt;
import axios from 'axios'
import { api } from '@/api'

export default {
  name: 'CommonHeader',
  props: {
    isLoggedIn: {
      type: Boolean,
      default: false
    },
    user: {
      type: Object,
      default: null
    }
  },
  methods: {
    async handleLogout () {
      try {
        await axios.post(api.auth.logout)
        this.$emit('logout')
        this.$message.success('已登出')
      } catch (error) {
        this.$message.error('登出失败')
      }
    }
  }
}
&lt;/script&gt;

&lt;style lang="css" scoped&gt;
  .header-wrapper {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
  }

  .nav-links {
    display: inline-block;
  }

  .user-area {
    display: inline-block;
    margin-left: auto;
  }

  .user-name {
    color: #fff;
    margin-right: 10px;
  }

  .logout-btn {
    color: #4fb6ff;
  }

  div {
    text-align: center;
  }

  p {
    display: inline-block;
    color: #fff;
    font-size: .3rem;
    padding: .26rem .24rem;
    -webkit-font-smoothing: antialiased;
    text-align: center;
  }

  p:hover {
    color: #4fb6ff;
  }
&lt;/style&gt;
