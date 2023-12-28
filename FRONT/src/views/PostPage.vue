<template>
<v-main>
  <v-container fluid class="pa-1 mt-3">
    <v-card class="pa-1" elevation="2" style="background-image: linear-gradient(to top right, rgba(19,84,122,.8), rgba(128,208,199,.8)), url('../src/assets/images/background3.jpg'); background-size: cover;">
      <v-row justify="center" style="padding-top:12px;">
        <v-card
          v-if="post.id != undefined"
          :key="post.id"
          border
          class="mb-4"
          density="compact"
          variant="text"
          style="background-color:white;"
          width="800"
        >
          <v-list-item :title="post.user.name.toUpperCase() + ' ' + post.user.last_name.toUpperCase()" :subtitle="'Ref: ' + post.reference_number" value="Card details">
            <template v-slot:prepend>
              <router-link :to="'/user/' + post.user.id + '?part=info'" @click="tab=0">
                <v-avatar :image="this.BASE_URL+'images/users/'+post.user.image_url" :to="'/user/' + post.userId + '?part=info'" size="38" class="mr-4"></v-avatar>
              </router-link>
            </template>
          </v-list-item>
          
          <v-carousel
            cycle
            height="400"
            hide-delimiter-background
            show-arrows="hover"
            
          >
            <v-carousel-item
              v-for="(slide, i) in post.image_url.split(',').slice(0, -1)"
              :src="this.BASE_URL+'images/posts/'+post.reference_number+'/'+slide"
              :key="i"
              style="object-fit: contain; object-position: center; background-color:black;"
            >
            </v-carousel-item>
          </v-carousel>

          <v-card-text>
            {{post.description}}
          </v-card-text>

          <v-card border
            density="compact"
            title="Messages"
            variant="text"
            class="mx-2"
            >
            <v-card-text class="overflow-y-auto" style="max-height:500px;">
              <v-timeline density="compact" align="start" >
                <v-timeline-item
                  v-for="comment in comments"
                  :key="comment.id"
                  :dot-color="comment.email ==  email ? 'deep-purple-lighten-1' : 'green'"
                  size="x-small"
                >

                  <div>
                    <div class="mb-4">
                      <div class="font-weight-normal">
                        <strong>{{ comment.name }} {{ comment.last_name }}</strong>
                         | {{ comment.email }} | Date: {{ formatDate(comment.last_modify) }} 
                      </div>
                      <div>{{ comment.text }}</div>
                    </div>
                    <v-btn v-if="comment.email == email" icon size="small" @click="deleteComment(comment)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </div>

                </v-timeline-item>
              </v-timeline>
            </v-card-text>
             <v-row >
              <v-col cols="8" class="pl-10 pr-0">
                <v-text-field v-model="message" label="Add Comment" prepend-icon="mdi-message" ></v-text-field>
              </v-col>
              <v-col cols="4">
                <v-btn @click="LeaveComment" color="primary" height="56">Comment</v-btn>
              </v-col>
            </v-row>
          </v-card>
          
          <v-card
          :key="post.id"
          border
          class="mb-4 mt-1 mx-2"
          density="compact"
          title="Tank Details"
          variant="text"
          style="background-color:white;"
          max-width="800"
        >

          <v-card-text class="overflow-y-auto ml-8 pa-0" style="height:200px;" v-if="containerInfo != undefined">
            <v-simple-table >
              <tbody>
                <tr>
                  <td><strong>Ref:</strong></td>
                  <td>{{containerInfo.reference_number}}</td>
                </tr>
                <tr>
                  <td><strong>Country:</strong></td>
                  <td>{{containerInfo.country}}</td>
                </tr>
                <tr>
                  <td><strong>Size:</strong></td>
                  <td>23 - manual import</td>
                </tr>
                <tr>
                  <td><strong>Weight:</strong></td>
                  <td>88 - manual import</td>
                </tr>
                <tr>
                  <td><strong>Client:</strong></td>
                  <td>{{containerInfo.client_name}}</td>
                </tr>
                <tr>
                  <td><strong>Country:</strong></td>
                  <td>{{containerInfo.country}}</td>
                </tr>
                <tr>
                  <td><strong>Delivery:</strong></td>
                  <td>21/12/2025 - manual import</td>
                </tr>
                <tr>
                  <td><strong>Delivery Company:</strong></td>
                  <td>Meverick - manual import</td>
                </tr>
                <tr>
                  <td><strong>Delivery Type:</strong></td>
                  <td>{{containerInfo.transport_type}}</td>
                </tr>
                <tr>
                  <td><strong>Product Type:</strong></td>
                  <td>{{containerInfo.product_type}}</td>
                </tr>
                <tr>
                  <td><strong>Responsible Name:</strong></td>
                  <td>{{containerInfo.responsible_name}}</td>
                </tr>
                <tr>
                  <td><strong>Responsible Email:</strong></td>
                  <td>{{containerInfo.responsible_email}}</td>
                </tr>
                <tr>
                  <td><strong>Location of Delivery:</strong></td>
                  <td>Somalia - manual import</td>
                </tr>
                <tr>
                  <td><strong>Contact:</strong></td>
                  <td>234 234 324234 - manual import</td>
                </tr>
                <tr>
                  <td><strong>Email:</strong></td>
                  <td>tank@tank.com - manual import</td>
                </tr>
              </tbody>
            </v-simple-table>
          </v-card-text>
        </v-card>
          
          <template v-slot:actions>
            <v-btn color="primary" variant="text">See in Map</v-btn>

            <v-btn color="primary" variant="text" @click="this.showInsertOrUpdateDialog(post, 'update')">Update</v-btn>

            <!-- OVDJE STAVI ITEM DA BUDE SVE OD OVOG POSTA -->
            <v-btn color="primary" variant="text" @click="this.showDeleteDialog(item)">Delete</v-btn>
          </template>
        </v-card>
      </v-row>               
    </v-card>      
  </v-container>
</v-main>
<DeleteDialog 
    :deleteDialog="deleteDialog"
    @update:deleteDialog="deleteDialog = $event"
    :deleteDialogItem="deleteDialogItem"
    @deleteItem="handleDeleteItem"
  />
  <InsertOrUpdateDialog 
    :insertOrUpdateDialog="insertOrUpdateDialog"
    @update:insertOrUpdateDialog="insertOrUpdateDialog = $event"
    :uniqueItem="chosenItem"
    @insertOrUpdateItem="handleInsertOrUpdateItem"
    type="POSTS" 
    typeOfDialog="update"
  />
</template>

<script>
import DeleteDialog from '@/components/DeleteItemDialog.vue'
import InsertOrUpdateDialog from '@/components/InsertOrUpdateDialog.vue'

import axios from 'axios'
import { useCounterStore } from '@/stores/counter';
import { mapState } from 'pinia'
import { mapActions } from 'pinia'
export default {
  components:{
    InsertOrUpdateDialog,
    DeleteDialog,
  },
  data() {
    return{
      deleteDialog: false,
      deleteDialogItem:{},
      insertOrUpdateDialog: false,
      insertOrUpdateDialogItem:{},

      post:{},
      comments:[],
      file: null,
      message:'',
      email:null,
      containerInfo:null,
    }
  },
  methods:{
    ...mapActions(useCounterStore, ['logout']),

    showDeleteDialog(item) {
      console.log('ssad')
      this.deleteDialogItem = item;
      this.deleteDialog = true;
      console.log(this.deleteDialog)
    },
    handleDeleteItem(item) {
      // Do something with item here
      console.log('delete');
      console.log(item);
    },
    showInsertOrUpdateDialog(item,typeOfDialog){
      this.typeOfDialog = typeOfDialog;
      this.insertOrUpdateDialogItem = item;
      this.insertOrUpdateDialog = true;
    },
    handleInsertOrUpdateItem(item) {
      // Do something with item here
      console.log(this.typeOfDialog);
      console.log(this.insertOrUpdateDialogItem);
      console.log(item);
      window.location.reload();
    },
    async LeaveComment() {
      let data = {
        "text": this.message,
        "post_id": this.post.id,
        "post_owner_email": this.post.user.email
      }
      console.log(data)

      await axios.post(this.BASE_URL + 'comment', data,
      {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization':'Bearer ' + localStorage.getItem('access_token'),
        }
      })
        .then(response => {
          console.log(response.data);
          window.location.reload();

        })
        .catch(error => {
          console.error(error);
          if(error.response.data.detail == 'Could not validate credentials'){
            this.logout()          
          }
        });
    },
    async deleteComment(comment){
      
      console.log(localStorage.getItem('access_token'))
      axios.post(this.BASE_URL + 'comment/delete/' + comment.id, '',
      {
        headers: {
          'Authorization':'Bearer ' + localStorage.getItem('access_token'),
          'Accept': 'application/json'
        }
      })
        .then(response => {
          console.log(response.data);
          window.location.reload();

        })
        .catch(error => {
          console.error(error);
          if(error.response.data.detail == 'Could not validate credentials'){
            this.logout()          
          }
        });
    },
    formatDate(timestamp) {
      const dateObj = new Date(timestamp);
      const year = dateObj.getFullYear();
      const month = dateObj.getMonth() + 1;
      const date = dateObj.getDate();
      const hours = dateObj.getHours();
      const minutes = dateObj.getMinutes();
      const seconds = dateObj.getSeconds();
      return `${year}-${month}-${date} ${hours}:${minutes}:${seconds}`;
    }
  },
  computed:{
    ...mapState(useCounterStore, ['BASE_URL', 'setUsername'])
  },
  async created(){
      this.email=localStorage.getItem('email')
    
      const url = window.location.href;
      const parts = url.split('/');
      const id = parts.pop()

      await axios.get(this.BASE_URL + 'post/' + id,
      {
          headers: {
            'Authorization':'Bearer ' + localStorage.getItem('access_token'),
            'Accept': 'application/json'
          }
      })
      .then(response => {
        console.log('this is post.', response);
        
        this.post = response.data  
        this.post.description = this.post.description.toUpperCase() 
        
        this.comments = response.data.comments
        console.log(this.comments)
      })
      .catch(error => {
        console.error('There was an error:', error.response.data);
        if(error.response.data.detail == 'Could not validate credentials'){
          this.logout()          
        }
      });


      await axios.get(this.BASE_URL + 'container/reference/' + this.post.reference_number,
      {
          headers: {
            'Authorization':'Bearer ' + localStorage.getItem('access_token'),
            'Accept': 'application/json'
          }
      })
      .then(response => {
        console.log('this is container.', response);
        
        this.containerInfo = response.data  
      })
      .catch(error => {
        console.error('There was an error:', error.response.data);
        if(error.response.data.detail == 'Could not validate credentials'){
          this.logout()          
        }
      });
  }
}
</script>

<style scoped>

</style>