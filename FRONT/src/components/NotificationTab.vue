<template>
  <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" class="text-none" stacked @click.stop="notification = !notification; searchBarVisible=false;">
            <v-badge :content="notificationNotReaded" :color="notificationNotReaded != 0 ? 'error' : ''">
              <v-icon>mdi-bell-outline</v-icon>
            </v-badge>
          </v-btn>
        </template>
  
        <v-list v-if="notificationList != undefined" >  
          <v-list density="compact" nav>
            <v-list-item  v-for="notification in notificationList" 
                          :key="notification" 
                          :to="'/post/'+notification.post.id" 
                          :prepend-icon="this.BASE_URL+'images/users/'+notification.comment_owner_image" 
                          :title="notification.comment_owner_name + ' ' + notification.comment_owner_last_name" 
                          subtitle="commented"
                          value="User Info"
                          @click="updateNotificationStatus(notification.id)"
                          :class="{
                            'unread-notification': !notification.is_read,
                            'read-notification': notification.is_read
                          }">
                          <template v-slot:prepend>
                            <v-avatar :image="this.BASE_URL+'images/users/'+notification.comment_owner_image" size="34" class="mr-8"></v-avatar>
                          </template>
                          {{notification.post.reference_number}}
                          
            </v-list-item>
            <!-- <v-list-item to="/user/1?part=posts" prepend-icon="mdi-forum" title="User Posts" value="User Posts"></v-list-item> -->
            <!-- <v-list-item title="Language" value="Language">
              <template v-slot:prepend>
                <v-avatar image="../src/assets/images/ES.png" size="24" class="mr-8"></v-avatar>
              </template>
            </v-list-item>
            <v-list-item @click="logout" prepend-icon="mdi-logout" to='/' title="Log out" value="Log out"></v-list-item> -->
          </v-list>
        </v-list>
      </v-menu>
</template>

<script>
import { mapState } from 'pinia'
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';
import { mapActions } from 'pinia'

export default{

  data() {
    return {
      notificationNotReaded:0,
      notificationList:[],
      notification:null,
      
    }
  },
  methods: {
    ...mapActions(useCounterStore, ['logout']),
    async getNotifications(){
      
      await axios.get(this.BASE_URL + 'notification/'+localStorage.getItem('email'),
      {
        headers: {
          'Authorization':'Bearer ' + localStorage.getItem('access_token'),
          'Accept': 'application/json'
        }
      })
      .then(response => {
        console.log('this are notifications.', response);
        this.notificationList = response.data  
      })
      .catch(error => {
        console.error('There was an error:', error.response.data);
        if(error.response.data.detail == 'Could not validate credentials'){
          this.logout()          
        }
      });

      let i=0
      this.notificationList.forEach(function(e){
        if(!e.is_read){
          i++
        }
      }) 
      this.notificationNotReaded=i   
        
    },
    async updateNotificationReadStatus(id){
      await axios.post(this.BASE_URL + 'notification/update/'+id,{},
        {
          headers: {
            'Authorization':'Bearer ' + localStorage.getItem('access_token'),
            'Accept': 'application/json'
          }
        })
        .then(response => {
          console.log('this is update of the notification.', response);
          this.notificationList = response.data     
        })
        .catch(error => {
          console.error('There was an error:', error.response.data);
          if(error.response.data.detail == 'Could not validate credentials'){
            this.logout()          
          }
        });
    },
    async updateNotificationStatus(id){
      await this.updateNotificationReadStatus(id)
      this.getNotifications();  
      
    }
  },
  computed:{
    ...mapState(useCounterStore, ['BASE_URL']),
  },
  async created(){
      this.getNotifications();         
  },
}
</script>

<style scoped>
.unread-notification {
  background-color: rgba(255, 0, 0, 0.1); /* Example background color for unread notifications */
}

.read-notification {
  background-color: rgba(0, 255, 0, 0.1); /* Example background color for read notifications */
}
</style>