<script>
export default {
  name: "SpanInvalid",
  props: {
    textSpan: {
      type: String,
      default: null,
      required: true
    },

    isView: {
      type: Boolean,
      default: false,
      required: true,
    }
  }
}
</script>

<template>
  <span v-if="isView" class="span-style">{{this.textSpan}}</span>
</template>

<style scoped lang="scss">
.span-style {
  font-size: 18px;
  color: green;
  width: 100%;
  text-align: center;
  display: block;
  padding-left: 0.5rem;
}
</style>