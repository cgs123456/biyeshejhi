<template>
  <div>
    <common-header></common-header>
    <about-main></about-main>
    <common-footer></common-footer>
    <bg-color></bg-color>
  </div>
</template>

<script>
import CommonHeader from 'common/Header'
import CommonFooter from 'common/Footer1'
import BgColor from 'common/BgSet'
import AboutMain from './components/AboutMain'

export default {
  name: 'About',
  components: {
    CommonHeader,
    AboutMain,
    CommonFooter,
    BgColor
  }
}
</script>

<style lang="css" scoped>
</style>
