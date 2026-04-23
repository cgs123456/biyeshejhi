# -*- encoding: utf-8 -*-
"""
@File    :   Hot.vue
@Contact :   cgs614074127@icloud.com
@License :   (C)Copyright 2022
@Author    @Version    @Desciption
-------    --------    -----------
jackie_chen      1.0         热度排名页面
"""
<template>
  <div>
    <common-header></common-header>
    <hot-main></hot-main>
    <common-footer></common-footer>
    <bg-color></bg-color>
  </div>
</template>

<script>
import CommonHeader from 'common/Header'
import CommonFooter from 'common/Footer1'
import BgColor from 'common/BgSet'
import HotMain from './components/HotMain'

export default {
  name: 'Hot',
  components: {
    CommonHeader,
    HotMain,
    CommonFooter,
    BgColor
  }
}

</script>

<style lang="css" scoped>

</style>
