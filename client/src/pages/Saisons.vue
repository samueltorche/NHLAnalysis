<template>
  <button @click="test">Call server</button>
</template>

<script>
  import axios from 'axios';

  export default {
    name: "Saisons",
    data() {
      return {}
    },
    methods: {
      test() {
        console.log(this.$serverUrl);
        axios.get(this.$serverUrl + '/').then(response => {
          console.log(response.data);
        }).catch(error => {
          console.log(error);
        });
      }
    }
  }
</script>

<style scoped>

</style>
