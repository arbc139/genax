<template>
  <md-layout class="main" md-column>
    <md-toolbar>
      <router-link class="title-route-link" to="/">
        <h2 class="md-title title">
          {{ $t('common.title') }}
        </h2>
      </router-link>
      <div class="empty-space" />
      <md-button
        class="md-icon-button title-button"
        :href="$t('common.githubLink')"
      >
        <md-icon class="github-icon" md-src="/static/GitHub-Mark-Light-64px.png" />
      </md-button>
      <md-button
        class="md-icon-button title-button"
        :href="$t('common.documentLink')"
      >
        <md-icon>description</md-icon>
      </md-button>
    </md-toolbar>
    <md-layout class="route">
      <router-view />
    </md-layout>
  </md-layout>
</template>

<script>
export default {
  name: 'main',
};
</script>

<style scoped>
.main {
  height: 100vh;
  overflow: hidden;
}

.title {
  color: white;
}

.title-route-link {
  color: white !important;
  text-decoration-color: white !important;
  text-decoration-line: none !important;
}

.empty-space {
  flex: 1;
}

.title-button {
  margin: 0 16px;
}

.route {
  overflow: auto;
}
</style>
