<template>
  <div>
    <common-header></common-header>
    <index-main ref="main" @search="handleSearch" @showHistory="showHistoryDialog=true"></index-main>
    <common-footer></common-footer>
    <bg-color></bg-color>

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
      showHistoryDialog: false,
      searchHistory: []
    }
  },
  methods: {
    async handleSearch (data) {
      try {
        await axios.post(api.history.add, data)
        this.fetchSearchHistory()
      } catch (error) {
        console.error('保存搜索历史失败', error)
      }
    },
    async fetchSearchHistory () {
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
    this.fetchSearchHistory()
  },
  activated () {}
}
</script>

<style lang="css">
</style>
