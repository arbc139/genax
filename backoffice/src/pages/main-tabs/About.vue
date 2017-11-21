<template>
 <md-whiteframe md-elevation="2" class="bcbTemp">
  <div>
    <h1>Welcome to GENAX</h1>
    <h4>GENAX uses the keywords you enter to dynamically find genes associated with your keywords.</h4>
    <p>GENAX is a web-based sever which extracts gene-gene interactions from the biomedical literature. The proposed tool provides several customizing options which include time, cut-off, weight of edge and so on. Through dynamic collecting, GENAX always provides knowledge extracted from the latest publication. Furthermore, all analysis re-sults can be downloaded as csv file format.</p>
  </div>
 </md-whiteframe>
</template>

<script>
export default {
  name: 'about',
};
</script>

<style scoped>
.bcbTemp {
  margin: 15px;
  padding: 15px;
}
</style>
