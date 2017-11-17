<template>
 <md-whiteframe md-elevation="2" class="bcbTemp">
  <div>
    <h1>Welcome to GENAX</h1>
    <h4>GENAX uses the keywords you enter to dynamically find genes associated with your keywords.</h4>
    <p>For given keywords, GENAX finds keyword related genes. GENAX usesE-utilitiesof Entrez to collect papers. E-utilities is an API that allows users to browse Entrez's database. GENAX uses these features of E-utilites to collect PubMed paper for your keywords. GENAX's method of collecting papers allows users to query complex and specific keywords. In the next chapter, you will learn how to build keywords.</p>
    <p>GENAX collects papers from PubMed using the E-utilities of Entrez. GENAX collects papers using the time period, allowing users to search for articles in a dynamic and complex way, regardless of time. What's more, you can use the time period to see which genes are attracting attention in the desired age.</p>
  </div>
 </md-whiteframe>
</template>

<script>
export default {
  name: 'about',
};
</script>

<style scoped>
.bcbTemp{
  margin: 15px,
  padding: 15px
  }
</style>
