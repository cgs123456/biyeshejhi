# -*- encoding: utf-8 -*-
"""
@File    :   Header.vue
@Contact :   cgs614074127@icloud.com
@License :   (C)Copyright 2022
@Author    @Version    @Description
-------    --------    -----------
jackie_chen      1.0         页面头部样式
"""
<template>
  <div class="header-wrapper">
    <div class="nav-links">
      <router-link to="/">
        <p>个人微博分析首页</p>
      </router-link>
      <router-link to="/comment">
        <p>单条微博分析首页</p>
      </router-link>
      <router-link to="/hot">
        <p>热度排名</p>
      </router-link>
      <router-link to="/crawler">
        <p>微博持续爬虫</p>
      </router-link>
      <router-link to="/analysis">
        <p>自定义文本分析</p>
      </router-link>
      <router-link to="/mycrawler">
        <p>已爬虫用户和微博</p>
      </router-link>
    </div>
    <div class="user-area">
      <template v-if="isLoggedIn">
        <span class="user-name">{{ user && (user.nickname || user.username) }}</span>
        <el-button type="text" class="logout-btn" @click="handleLogout">登出</el-button>
      </template>
      <template v-else>
        <el-button type="text" class="auth-btn" @click="showLoginDialog = true">登录</el-button>
        <el-button type="text" class="auth-btn" @click="showRegisterDialog = true">注册</el-button>
      </template>
    </div>

    <el-dialog
      title="用户登录"
      :visible.sync="showLoginDialog"
      width="400px"
      append-to-body
    >
      <el-form :model="loginForm" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="loginForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="loginForm.password" type="password"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showLoginDialog = false">取消</el-button>
        <el-button type="primary" @click="handleLogin">登录</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="用户注册"
      :visible.sync="showRegisterDialog"
      width="400px"
      append-to-body
    >
      <el-form :model="registerForm" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="registerForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="registerForm.password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="昵称">
          <el-input v-model="registerForm.nickname"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showRegisterDialog = false">取消</el-button>
        <el-button type="primary" @click="handleRegister">注册</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import { api } from '@/api'

export default {
  name: 'CommonHeader',
  data () {
    return {
      isLoggedIn: false,
      user: null,
      showLoginDialog: false,
      showRegisterDialog: false,
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        password: '',
        nickname: ''
      }
    }
  },
  methods: {
    async fetchCurrentUser () {
      try {
        const response = await axios.get(api.auth.current)
        if (response.data.success) {
          this.isLoggedIn = response.data.isLoggedIn
          this.user = response.data.user
        }
      } catch (error) {
        this.isLoggedIn = false
        this.user = null
      }
    },
    async handleLogin () {
      if (!this.loginForm.username || !this.loginForm.password) {
        this.$message.error('请输入用户名和密码')
        return
      }
      try {
        const response = await axios.post(api.auth.login, this.loginForm)
        if (response.data.success) {
          this.isLoggedIn = true
          this.user = response.data.user
          this.showLoginDialog = false
          this.$message.success('登录成功')
          this.loginForm = { username: '', password: '' }
        } else {
          this.$message.error(response.data.message || '登录失败')
        }
      } catch (error) {
        this.$message.error('登录失败，请检查网络连接')
      }
    },
    async handleRegister () {
      if (!this.registerForm.username || !this.registerForm.password) {
        this.$message.error('请输入用户名和密码')
        return
      }
      try {
        const response = await axios.post(api.auth.register, this.registerForm)
        if (response.data.success) {
          this.isLoggedIn = true
          this.user = response.data.user
          this.showRegisterDialog = false
          this.$message.success('注册成功')
          this.registerForm = { username: '', password: '', nickname: '' }
        } else {
          this.$message.error(response.data.message || '注册失败')
        }
      } catch (error) {
        this.$message.error('注册失败，请检查网络连接')
      }
    },
    async handleLogout () {
      try {
        await axios.post(api.auth.logout)
        this.isLoggedIn = false
        this.user = null
        this.$message.success('已登出')
      } catch (error) {
        this.$message.error('登出失败')
      }
    }
  },
  mounted () {
    this.fetchCurrentUser()
  }
}
</script>

<style lang="css" scoped>
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

  .auth-btn {
    color: #fff;
  }

  .auth-btn:hover {
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
</style>
