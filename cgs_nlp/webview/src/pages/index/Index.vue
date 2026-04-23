<template>
  <div>
    <common-header
      :isLoggedIn="isLoggedIn"
      :user="user"
      @openLogin="showLoginDialog = true"
      @openRegister="showRegisterDialog = true"
      @logout="handleLogout"
    ></common-header>
    <index-main ref="main" @search="handleSearch" @showHistory="showHistoryDialog=true"></index-main>
    <common-footer></common-footer>
    <bg-color></bg-color>

    <!-- 登录弹窗 -->
    <el-dialog
      title="用户登录"
      :visible.sync="showLoginDialog"
      width="400px"
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

    <!-- 注册弹窗 -->
    <el-dialog
      title="用户注册"
      :visible.sync="showRegisterDialog"
      width="400px"
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

    <!-- 搜索历史弹窗 -->
    <el-dialog
      title="搜索历史"
      :visible.sync="showHistoryDialog"
      width="600px"
    >
      <el-table :data="searchHistory" stripe>
        <el-table-column prop="keyword" label="搜索关键词" width="200"></el-table-column>
        <el-table-column prop="nickname" label="用户昵称" width="150"></el-table-column>
        <el-table-column prop="search_time" label="搜索时间" width="200"></el-table-column>
        <el-table-column label="操作" width="100">
          <template slot-scope="scope">
            <el-button type="text" @click="searchFromHistory(scope.row)">再次搜索</el-button>
          </template>
        </el-table-column>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showHistoryDialog = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import BgColor from 'common/BgSet'
import CommonHeader from 'common/Header'
import CommonFooter from 'common/Footer1'
import IndexMain from './components/main'
import axios from 'axios'
import { api } from '@/api'

export default {
  name: 'Index',
  components: {
    BgColor,
    CommonHeader,
    IndexMain,
    CommonFooter
  },
  data () {
    return {
      isLoggedIn: false,
      user: null,
      showLoginDialog: false,
      showRegisterDialog: false,
      showHistoryDialog: false,
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        password: '',
        nickname: ''
      },
      searchHistory: []
    }
  },
  computed: {},
  methods: {
    async fetchCurrentUser () {
      try {
        const response = await axios.get(api.auth.current)
        if (response.data.success) {
          this.isLoggedIn = response.data.isLoggedIn
          this.user = response.data.user
        }
      } catch (error) {
        console.error('获取用户信息失败', error)
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
          this.fetchSearchHistory()
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
    handleLogout () {
      this.isLoggedIn = false
      this.user = null
      this.searchHistory = []
    },
    async handleSearch (data) {
      if (this.isLoggedIn) {
        try {
          await axios.post(api.history.add, data)
          this.fetchSearchHistory()
        } catch (error) {
          console.error('保存搜索历史失败', error)
        }
      }
    },
    async fetchSearchHistory () {
      if (!this.isLoggedIn) return
      try {
        const response = await axios.get(api.history.list)
        if (response.data.success) {
          this.searchHistory = response.data.history
        }
      } catch (error) {
        console.error('获取搜索历史失败', error)
      }
    },
    searchFromHistory (item) {
      this.showHistoryDialog = false
      if (item.weibo_id) {
        this.$refs.main.$refs.wbId.value = item.weibo_id
        this.$refs.main.getWbId()
      }
    }
  },
  mounted () {
    this.fetchCurrentUser()
    this.fetchSearchHistory()
  },
  activated () {}
}
</script>

<style lang="css">
</style>
