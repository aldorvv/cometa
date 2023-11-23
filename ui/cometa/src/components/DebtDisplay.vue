<!-- DebtDisplay.vue -->

<template>
    <div class="debt-display">
      <h4 class="apple-font">{{ response }}</h4>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      response: {
        type: Object,
        required: true,
      },
    },
  };
  </script>
  
  <style scoped>
  .debt-display {
    margin-top: 16px; /* Add some spacing from the dropdown */
    font-family: 'San Francisco', sans-serif;
  }
  
  .debt-display pre {
    padding: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #fff;
    overflow-x: auto;
  }

  .apple-font {
  font-family: 'San Francisco', sans-serif;
  margin-left: 10px;
}
  </style>
  