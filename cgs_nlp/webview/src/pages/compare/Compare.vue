<template>
  <div>
    <common-header></common-header>
    <compare-main></compare-main>
    <common-footer></common-footer>
    <bg-color></bg-color>
  </div>
</template>

<script>
import CommonHeader from 'common/Header'
import CommonFooter from 'common/Footer1'
import BgColor from 'common/BgSet'
import CompareMain from './components/CompareMain'

export default {
  name: 'Compare',
  components: {
    CommonHeader,
    CompareMain,
    CommonFooter,
    BgColor
  }
}
</script>

<style lang="css" scoped>
</style>
