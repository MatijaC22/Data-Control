<template>
<v-main>
  <v-container fluid class="pa-1 mt-3">
    <v-card class="pa-1" elevation="2" style="background-image: linear-gradient(to top right, rgba(19,84,122,.8), rgba(128,208,199,.8)), url('../src/assets/images/background3.jpg'); background-size: cover;">

    <div class="clocks-container" :style="mdAndUp ? 'display: flex; align-items: center;' : ''">
      <v-card
        border
        class="mx-auto mb-2"
        :width="mdAndUp ? 400 : 'auto'"
        density="compact"
        color="grey-lighten-5">
        <br>
        <v-card
            class="mx-auto"
            max-width="350"
          >
          <v-list style="text-align:center;">        
            <v-list-item title="Belgium"></v-list-item>
            <v-list-item :title="belgiumTime"></v-list-item>
          </v-list>
        </v-card>
        
        <section section class="clock-container">
          <div class="clock">
            <div class="hour" :style="{ transform: 'rotate(' + BELhourDeg + 'deg)' }"></div>
            <div class="min" :style="{ transform: 'rotate(' + BELminDeg + 'deg)' }"></div>
            <div class="sec" :style="{ transform: 'rotate(' + BELsecDeg + 'deg)' }"></div>
          </div>
          <v-card
            class="mx-auto"
            max-width="350"
          >
            <v-list >
              <v-list-subheader>Office</v-list-subheader>
        
              <v-list-item
                v-for="(item, i) in belgium"
                :key="i"
                :value="item"
                active-color="primary"
              >
                <template v-slot:prepend>
                  <v-icon :icon="item.icon"></v-icon>
                </template>
        
                <v-list-item-title>{{item.text}}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card>
        </section>
      </v-card>
      <v-card
        border
        class="mx-auto mb-2"
        :width="mdAndUp ? 400 : 'auto'"
        density="compact"
        color="grey-lighten-5">
        <br>
        <v-card
            class="mx-auto"
            max-width="350"
          >
          <v-list style="text-align:center;">        
            <v-list-item title="Guatemala"></v-list-item>
            <v-list-item :title="guatemalaTime"></v-list-item>
          </v-list>
        </v-card>
        
        <section class="clock-container">
          <div class="clock">
            <div class="hour" :style="{ transform: 'rotate(' + GUAhourDeg + 'deg)' }"></div>
            <div class="min" :style="{ transform: 'rotate(' + GUAminDeg + 'deg)' }"></div>
            <div class="sec" :style="{ transform: 'rotate(' + GUAsecDeg + 'deg)' }"></div>
          </div>
          <v-card
            class="mx-auto"
            max-width="350"
          >
            <v-list >
              <v-list-subheader>Office</v-list-subheader>
        
              <v-list-item
                v-for="(item, i) in guatemala"
                :key="i"
                :value="item"
                active-color="primary"
              >
                <template v-slot:prepend>
                  <v-icon :icon="item.icon"></v-icon>
                </template>
        
                <v-list-item-title>{{item.text}}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card>
        </section>
      </v-card>
    </div>
    </v-card>
  </v-container>
</v-main>
</template>

<script lang="ts">
import Auth from '@/components/Auth.vue';

import { useDisplay } from 'vuetify'
import { defineComponent } from 'vue';

import axios from 'axios'

export default defineComponent({
  name: 'HomeView',
  components: {
    Auth,
  },
  data() {
    const { xs, mdAndUp, smAndDown } = useDisplay()
    return {

      test:true,
      message: "",
      GUAsecDeg: -90,
      GUAminDeg: -90,
      GUAhourDeg: -90,
      BELsecDeg: -90,
      BELminDeg: -90,
      BELhourDeg: -90,
      guatemalaTime: '',
      belgiumTime: '',
      xs, mdAndUp, smAndDown,
      guatemala: [
        { text: 'Working time: 8:00-16:00', icon: 'mdi-clock' },
        { text: 'Contact: Anna Smith', icon: 'mdi-account' },
        { text: 'Phone number: +372 91 723 4321', icon: 'mdi-phone' },
      ],
      belgium: [
        { text: 'Working time: 8:00-16:00', icon: 'mdi-clock' },
        { text: 'Contact: Sam John', icon: 'mdi-account' },
        { text: 'Phone number: +332 91 723 4321', icon: 'mdi-phone' },
      ],

    };
  },
  mounted() {
    setInterval(() => {
      const date = new Date();

      const optionsGUA = { timeZone: 'America/Guatemala' };
      this.guatemalaTime = date.toLocaleString('en-US', optionsGUA);
      this.GUAsecDeg = (date.getSeconds() / 60) * 360 - 90;
      this.GUAminDeg = (date.getMinutes() / 60) * 360 + 90; // -90
      this.GUAhourDeg = (date.getHours() / 12) * 360 - 60; //- 90

      const optionsBEL = { timeZone: 'Europe/Brussels' };
      this.belgiumTime = date.toLocaleString('en-US', optionsBEL);
      this.BELsecDeg = ((date.getSeconds() + new Date().getTimezoneOffset()*60) / 60) * 360 - 90;
      this.BELminDeg = ((date.getMinutes() + new Date().getTimezoneOffset()) / 60) * 360 - 90;
      this.BELhourDeg = ((date.getHours() + new Date().getTimezoneOffset()/60) / 12) * 360 - 30; //-90
    }, 1000);
  },
});
</script>

<style scoped>

.time-zone {
  text-align:center;
}

.clock-container {
  margin-top: 0px;
  display: inline-block;
}
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}
section {
  height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.container {
  width: 100%;
  height: 100%;
}
.clock {
  height: 400px;
  width: 90%;
  max-width: 500px;
  margin: 0 auto;
  border-radius: 50%;
  position: relative;
  background-image: url(../src/assets/images/clock-no-hands-clipart.png);
  background-position: center;
  background-size: contain;
  background-repeat: no-repeat;
}

.sec {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 30%;
  height: 5px;
  background-color: rgb(0, 0, 0);
  transform-origin: left;
  border-radius: 50%;
  transform: rotate(-90deg);
}

.min {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 25%;
  height: 5px;
  background-color: rgb(0, 0, 0);
  transform-origin: left;
  border-radius: 50%;
  transform: rotate(-90deg);
}

.hour {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 17%;
  height: 5px;
  background-color: rgb(0, 0, 0);
  transform-origin: left;
  border-radius: 50%;
  transform: rotate(-90deg);
}

</style>
