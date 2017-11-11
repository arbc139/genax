<template>
  <md-layout
    class="help-frame"
    md-row
    md-align="start"
  >
    <md-layout :md-flex="66">
      <md-whiteframe class="tool" md-elevation="2">
        <slot name="tool" />
      </md-whiteframe>
    </md-layout>
    <md-layout :md-flex="33">
      <md-whiteframe class="help" md-elevation="2">
        <slot name="help" />
      </md-whiteframe>
    </md-layout>
  </md-layout>
</template>

<script>
export default {
  name: 'help-frame',
};
</script>

<style scoped>
.help-frame {
  margin-bottom: 16px;
}

.tool {
  width: 100%;
  height: 100%;
  padding: 16px;
}

.help {
  width: 100%;
  height: 100%;
  padding: 16px;
  margin-left: 16px;
}
</style>
