<template>
  <div class="main-tabs-container">
    <md-tabs class="main-tabs" @change="onTabChange" :md-dynamic-height="false">
      <md-tab
        id="about"
        :md-active="currentTab === TabType.about"
        :md-label="$t('mainTabs.about.label')"
      />
      <md-tab
        id="run"
        :md-active="currentTab === TabType.stepper"
        :md-label="$t('mainTabs.run.label')"
      />
      <md-tab
        id="performance"
        :md-active="currentTab === TabType.performance"
        :md-label="$t('mainTabs.performance.label')"
      />
    </md-tabs>
    <router-view />
  </div>
</template>

<script>
const TabType = {
  about: 'TAB_TYPE_ABOUT',
  stepper: 'TAB_TYPE_STEPPER',
  performance: 'TAB_TYPE_PERFORMANCE',
};

export default {
  name: 'main-tabs',
  data() {
    return { TabType };
  },
  computed: {
    currentTab() {
      let currentTab = '';
      switch (this.$route.name) {
        case 'About':
          currentTab = this.TabType.about;
          break;
        case 'Stepper':
          currentTab = this.TabType.stepper;
          break;
        case 'Performance':
          currentTab = this.TabType.performance;
          break;
        default:
          break;
      }
      return currentTab;
    },
  },
  mounted() {
    this.enableTabClick = true;
  },
  methods: {
    tabIndexToType(tabIndex) {
      switch (tabIndex) {
        case 0:
          return this.TabType.about;
        case 1:
          return this.TabType.stepper;
        default:
          return this.TabType.performance;
      }
    },
    onTabChange(tabIndex) {
      if (!this.enableTabClick) {
        return;
      }

      const tabType = this.tabIndexToType(tabIndex);
      switch (tabType) {
        case this.TabType.about:
          this.$router.push({ name: 'About' });
          return;
        case this.TabType.stepper:
          this.$router.push({ name: 'Stepper' });
          return;
        default:
          this.$router.push({ name: 'Performance' });
      }
    },
  },
};
</script>

<style scoped>
.main-tabs-container {
  display: flex;
  flex-direction: column;
  width: 100%;
}
.main-tabs {
  display: unset;
}
</style>

<style>
.main-tabs .md-tabs-content {
  display: none;
}
</style>
