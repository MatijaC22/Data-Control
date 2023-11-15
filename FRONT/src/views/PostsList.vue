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
        <div v-if="postList.length == 0 && isLoading == false">YOU DONT HAVE POSTS</div>
        <div v-else-if="postList.length != 0"><PostData :postList="postList"/></div>
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
      pendingRequest: false,
      page:0,
      totalNumberOfLinesGiven:false,
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
        if(!this.totalNumberOfLinesGiven){
          this.getPosts();
        }
      }
    },
    async getPosts(){
      
      this.isLoading = true;
            
      if(this.pendingRequest){
        return;
      }

      this.pendingRequest = true;

      this.page = this.page + 1

      let data = {
        page : this.page,
        per_page : 1,
        // user_id:1
      }

      await axios.get(this.BASE_URL + 'post/package',{params:data,
        
          headers: {
            'Authorization':'Bearer ' + localStorage.getItem('access_token'),
            'Accept': 'application/json'
          }
      })
      .then(response => {
          console.log('this is response.', response);
          this.postList = this.postList.length ? this.postList.concat(response.data.data) : response.data.data
          if(response.data.actual_page==response.data.total_number_of_pages){
            this.totalNumberOfLinesGiven = true
          }   
      })
      .catch(error => {
          console.error('There was an error:', error.response.data);
          if(error.response.data.detail == 'Could not validate credentials'){
            this.logout()          
          }
      });

      this.pendingRequest = false;
      this.isLoading = false;
    }
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