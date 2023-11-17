<template>
      <v-main>
        <v-container fluid class="pa-1 mt-3">
          <!-- <v-card  class="mx-auto bg" elevation="2" style="background-image: url('../src/assets/images/background2.jpg');  background-size: cover;"> -->
          <v-card elevation="2" style="background-image: linear-gradient(to top right, rgba(19,84,122,.8), rgba(128,208,199,.8)), url('../src/assets/images/background3.jpg'); background-size: cover;">
            <v-img height="200px" />
            <!-- <v-img height="200px" src="../src/assets/images/background.jpg" gradient="150deg, rgb(185 224 255 / 58%) 0%, rgb(243 220 246 / 52%) 35%, rgb(223 255 242 / 74%) 74%"> -->
            <!-- </v-img> -->
            <v-row justify="center" >
              <v-col align-self="start" class="d-flex justify-center align-center pa-0" cols="12">
                <v-avatar class="profile avatar-center-heigth avatar-shadow" color="grey" size="164">
                  <v-img v-if="userData.email != undefined" :src="this.BASE_URL+'assets/images/users/'+userData.image_url"></v-img>
                </v-avatar>
              </v-col>
            </v-row>
                <v-list-item color="black" class="profile-text-name mt-8 pt-16 px-1"> 
                  <v-card   
                    color="grey-lighten-5"
                    border
                    class="mt-10"
                    density="compact"> 
                    <v-card-title>
                      User Info
                    </v-card-title>
                    <v-card-text>
                      <v-container v-if="userData.id != undefined">
                        <v-row>
                          <v-col cols="4" sm="2">
                            <strong>Name:</strong>
                          </v-col>
                          <v-col cols="8" sm="10">
                            {{userData.name}}
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col cols="4" sm="2">
                            <strong>Surname:</strong>
                          </v-col>
                          <v-col cols="8" sm="10">
                            {{userData.surname}}
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col cols="4" sm="2">
                            <strong>Email:</strong>
                          </v-col>
                          <v-col cols="8" sm="10">
                            {{userData.email}}
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col cols="4" sm="2">
                            <strong>Date of Birth:</strong>
                          </v-col>
                          <v-col cols="8" sm="10">
                            {{userData.date_of_birth}}
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col cols="4" sm="2">
                            <strong>Nationality:</strong>
                          </v-col>
                          <v-col cols="8" sm="10">
                            {{userData.nationality}}
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col cols="4" sm="2">
                            <strong>Access Level:</strong>
                          </v-col>
                          <v-col cols="8" sm="10">
                            {{userData.access_level}}
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col cols="4" sm="2">
                            <strong>Active:</strong>
                          </v-col>
                          <v-col cols="8" sm="10">
                            {{userData.active}}
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>
                  </v-card>
                </v-list-item>

                <v-item-group selected-class="bg-primary">
                    <v-container class="mb-0 pb-0">
                      <div class="d-flex justify-center mb-0">
                        <v-sheet
                          v-for="(item, index) in items" :key="index"
                          style="margin:10px; background-color: transparent;"
                        >
                          <v-card
                            :class="['align-center', {'bg-primary': index == showPosts }]"
                            dark
                            height="50"
                            width="160"
                            @click="toggle(index);"
                          >
                            <div @click="toggle(index)" class="d-flex align-center justify-center" style="height: 100%;">
                              <div
                                class="text-h6 flex-grow-1 text-center"
                              >
                                {{ item }}
                              </div>
                            </div>
                          </v-card>
                      </v-sheet>
                    </div>   
                  </v-container>
                </v-item-group>

                <div v-if="!showPosts">
                  <UserInfoData/>
                </div>
                <div v-else class="mx-0 mb-1">
                  <PostsData :postList="postList"/>
                </div>

            <!-- <v-row>
              <v-col class="d-flex justify-end align-right pa-2" cols="6">
                <v-btn rounded color="primary" dark>
                  Agendar um Horário
                </v-btn>
              </v-col>
              <v-col class="d-flex justify-left align-left pa-2" cols="6">
                <v-btn rounded color="primary" dark>
                  Contato
                </v-btn>
              </v-col>
            </v-row> -->


          </v-card>
        </v-container>
      </v-main>
</template>


<script>
import axios from 'axios'
import PostsData from '@/components/PostData.vue'
import UserInfoData from '@/components/UserInfoData.vue'

import { useCounterStore } from '@/stores/counter';
import { mapState } from 'pinia'
import { mapActions } from 'pinia'
import { mapWritableState } from 'pinia'


  export default {
    components:{
      PostsData,
      UserInfoData
    },
    data() {
      return{
        showPosts:false,
        items: [
          "Info","Posts"
        ],
        postList:[],
        userData:{},
        page : 0,
        totalNumberOfLinesGiven: false,
      }
    },
    watch: {
      $route(to) {
        const newId = to.params.id;
        // Fetch user data based on the newId
        if(/user\/\d+/.test(window.location.pathname)){
        // if(!isNan(newId)){
          this.getUserData();
          this.totalNumberOfLinesGiven = false
          this.page = 0
          this.postList = []
          this.getUserPosts();
        }
      }
    },
    methods:{
      ...mapActions(useCounterStore, ['logout', 'getUser']),
      toggle(index) {
        if(index == 0){
          this.showPosts = false;
        }
        if(index == 1){
          this.showPosts = true;
          this.getUserPosts();
        }
      },
      formatDate(timestamp) {
        const dateObj = new Date(timestamp);
        const year = dateObj.getFullYear();
        const month = dateObj.getMonth() + 1;
        const date = dateObj.getDate();
        const hours = dateObj.getHours();
        const minutes = dateObj.getMinutes();
        const seconds = dateObj.getSeconds();
        return `${year}-${month}-${date}`;
      },
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
      async getUserPosts(){
        if(this.showPosts){
          
          this.isLoading = true;
            
          if(this.pendingRequest){
            return;
          }

          this.pendingRequest = true;

          this.page = this.page + 1

          let data = {
            page : this.page,
            per_page : 10,
            user_id : parseInt(window.location.pathname.split('/').pop().replace(/\D/g,'')),
          }

          await axios.get(this.BASE_URL + 'post/package', {params:data,
            
              headers: {
                'Authorization':'Bearer ' + localStorage.getItem('access_token'),
                'Accept': 'application/json'
              }
            })
            .then(response => {
              console.log('this is response.', response);
              // this.postList = response.data  
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
      async getUserData(){
        try {
          this.userData = await this.getUser();
        } catch (error) {
          throw error;
        }
      },
    },
    computed:{
      ...mapState(useCounterStore, ['BASE_URL']),
      ...mapWritableState(useCounterStore, ['isLoading']),


    },
    async created() {
            
      await this.getUserData();  
      // console.log(this.userData)
      window.addEventListener('scroll', this.handleScroll);

    },
    beforeUnmount(){
      window.removeEventListener('scroll',this.handleScroll);
    },
  }
</script>


<style>
    .avatar-center-heigth {
      position: absolute;
    }

    .profile-text-name {
      margin-top: 70px;
    }

    .sutitles {
      margin: 5px;
      padding: 16px;
    }
    .upload-btn{
  position: absolute !important;
    z-index: 999;
    top: 121px;
    color: cadetblue;
    background: blueviolet;
    background: rgb(125,198,163);
    background: linear-gradient(50deg, rgba(125,198,163,1) 0%, rgba(35,216,227,1) 72%);
}

.bg{
background: rgb(255,197,185);
background: linear-gradient(0deg, rgba(255,197,185,0.711922268907563) 0%, rgba(220,246,223,0.6671043417366946) 35%, rgba(255,255,255,0.7539390756302521) 74%), url(http://unblast.com/wp-content/uploads/2021/09/Real-Estate-Agent-Illustration.jpg);
}

.avatar-shadow{
box-shadow: 0px 0px 10px 0px rgba(50,12,112,0.75);
-webkit-box-shadow: 0px 0px 10px 0px rgba(50,12,112,0.75);
-moz-box-shadow: 0px 0px 10px 0px rgba(50,12,112,0.75);
}

  </style>
