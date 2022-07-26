<template>
  <v-app>
    <v-parallax
      src="https://preview.redd.it/c3uhsgo1vx541.jpg?auto=webp&s=a45b583ebf921d3ad1649e77ad05e55226140120"
      height="1000"
    >
      <v-row align="center" justify="center">
        <v-col class="text-center" cols="12">
          <h1 class="text-h4 mb-4">Welcome to Beta</h1>

          <v-btn
            color="red"
            class="ma-2 white--text"
            fab
            @click="$auth.loginWith('google')"
          >
            <v-icon dark> mdi-google </v-icon>
          </v-btn>
        </v-col>
      </v-row></v-parallax
    ></v-app
  >
</template>
<script>
export default {
  layout: "empty",
  mounted(){
    console.log(this.$auth.user)
  }
};
</script>