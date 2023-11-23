<!-- DropdownMenu.vue -->

<template>
  <div class="dropdown">
    <div class="dropdown-header" @click="toggleDropdown">
      {{ selectedOption ? selectedOption : '¿Quién va a pagar?' }}
    </div>
    <ul v-if="isOpen" class="dropdown-options">
      <li v-for="(option, index) in options" :key="index" @click="handleSelect(option)">
        {{ option }}
      </li>
    </ul>
  </div>

</template>

<script>
export default {
  data() {
    return {
      selectedOption: null,
      isOpen: false,
    };
  },
  props: {
    options: {
      type: Array,
      required: true,
    },
  },
  methods: {
    handleSelect(option) {
      this.selectedOption = option;
      this.$emit('select', option);
      this.isOpen = false;
    },
    toggleDropdown() {
      this.isOpen = !this.isOpen;
    },
  },
};
</script>

<style scoped>
/* Apple's San Francisco font */
@import url('https://fonts.googleapis.com/css2?family=San+Francisco&display=swap');

/* Component styles using the Apple font */
.dropdown {
  position: relative;
  display: inline-block;
  font-family: 'San Francisco', sans-serif; /* Use the Apple font */
}

.dropdown-header {
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  width: 200px; /* Set a fixed width for the dropdown header */
}

.dropdown-options {
  list-style: none;
  padding: 0;
  margin: 0;
  border-radius: 0 0 4px 4px;
  position: absolute;
  top: 100%;
  left: 0;
  background-color: #fff;
  max-height: 150px;
  overflow-y: auto;
  width: 200px; /* Set a fixed width for the dropdown options */
}
.dropdown-options li {
  padding: 8px;
  cursor: pointer;
  font-family: 'San Francisco', sans-serif;
}
.dropdown-options li:hover {
  background-color: #f0f0f0;
}
</style>
