<template>
<v-main>
  <v-container fluid class="pa-1  mt-3">
    
    <v-card 
      class="pa-1" 
      elevation="2" 
      style="background-image: linear-gradient(to top right, rgba(19,84,122,.8), rgba(128,208,199,.8)), 
              url('../src/assets/images/background3.jpg'); 
              background-size: cover;
              min-height:100vh;">
            

      <!-- <v-row justify="center" style="padding-top:12px;"> -->
        <div v-if="searchQuery.length == 0 && isLoading == false">YOU DONT HAVE POSTS</div>
        <div v-else-if="searchQuery.length != 0"><PostData :postList="searchQuery"/></div>
      <!-- </v-row> -->
      <div class="is-loading-bar has-text-centered"  style="text-align:center;" v-bind:class="{'is-loading': this.isLoading }">
        <div class="lds-dual-ring"></div>
      </div>
    </v-card>
  </v-container>
</v-main>
</template>

<script>

import axios from 'axios'

import { defineComponent } from 'vue';
import PostData from '@/components/PostData.vue'
import { useCounterStore } from '@/stores/counter';
import { mapState } from 'pinia'
import { mapWritableState } from 'pinia'
import { mapActions } from 'pinia'


export default defineComponent({
  name:'PostsList',
  components:{
    PostData
  },
  data(){
    return{
      postList:[],
      pendingRequest: false
    }
  },
  computed:{
    ...mapState(useCounterStore, ['BASE_URL']),
    ...mapWritableState(useCounterStore, ['isLoading', 'searchQuery']),

  },
  async created(){
      this.getPosts();
      
      window.addEventListener('scroll', this.handleScroll);
  },
  beforeUnmount(){
    window.removeEventListener('scroll',this.handleScroll);
  },
  methods:{
    ...mapActions(useCounterStore, ['logout']),

    handleScroll(){
      const { scrollTop, clientHeight, scrollHeight } = document.documentElement;
      const bottomOfWindow = Math.round(scrollTop) + clientHeight === scrollHeight;

      if( bottomOfWindow){
        console.log('bottom of window')
        this.getPosts();
      }
    },
  },      
})
</script>


<style scoped>

.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}
.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #20c5b5;
  border-color: #20c5b5 transparent #20c5b5 transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.is-loading-bar {
  height: 0;
  overflow: hidden;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;
}
.is-loading {
  height: 80px;
}
</style>