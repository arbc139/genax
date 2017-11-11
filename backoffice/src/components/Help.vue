<template>
  <md-layout md-column md-align="start">
    <span class="md-title title">{{ title }}</span>
    <div
      class="instruction"
      v-for="(instruction, index) in instructions"
      :key="instruction.id"
    >
      <span class="md-body-1" v-show="index !== instructions.length - 1">
        {{ instruction.content }}
      </span>
      <div v-show="index === instructions.length - 1">
        <span class="md-body-1">
          {{ instruction.content }}
        </span>
        <a
          target="_blank"
          class="a-tag-hover"
          :href="instruction.link"
        >
          {{ $t('common.linkMessage') }}
        </a>
      </div>
    </div>
  </md-layout>
</template>

<script>
export default {
  name: 'help',
  props: {
    title: {
      type: String,
      required: true,
    },
    instructions: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.title {
  margin-bottom: 8px;
}

.instruction {
  margin-bottom: 8px;
}

.a-tag-hover:hover {
  cursor: pointer;
}
</style>
