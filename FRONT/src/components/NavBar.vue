<template>
  <v-app-bar
    app
    color="teal-darken-4"
    image="../src/assets/images/navbarBackground.jpg"
    fixed
  >
    <template v-slot:image>
      <v-img gradient="to top right, rgba(19,84,122,.8), rgba(128,208,199,.8)"></v-img>
    </template>
      
    <template v-slot:prepend v-if="smAndDown" >
      <v-app-bar-nav-icon variant="text" @click.stop="openNavBar = !openNavBar; searchBarVisible=false;"></v-app-bar-nav-icon>  
    </template>

    <v-avatar image="../src/assets/images/antaresWebp.webp" size="41" style="margin-left:10px;"></v-avatar>

    <!-- <v-app-bar-title>ANTARES PROGRAMMING</v-app-bar-title> -->

    <v-tabs
      v-model="tab"
      color="deep-purple-accent-4"
      align-tabs="end"
      v-if="mdAndUp"
    >
      <router-link to="/" class="routerLink">
        <v-tab :value="1">
              Home
        </v-tab>
      </router-link>
      <!-- <v-tab :value="2" id="menu-activator-posts">
        Posts
        <v-menu activator="#menu-activator-posts" > 
          <v-list style="border-top-left-radius: 0; border-top-right-radius: 0;">
            <v-list-item
              v-for="item in navBarDataPosts"
              :key="item.title"
              :value="item.title"
              :to="item.value"
            >
              <v-list-item-title style="font-size:13px;">{{ item.title }}</v-list-item-title>
            </v-list-item>
            <v-list-item @click="this.showInsertOrUpdateDialog({}, 'insert')"
                        style="border-top-left-radius: 0; border-top-right-radius: 0;"
            >
              <v-list-item-title style="font-size:13px;">INSERT</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-tab> -->
      <v-tab :value="3"  id="menu-activator" v-if="userData.access_level == 1">
        Data
        <v-menu activator="#menu-activator" > 
          <v-list style="border-top-left-radius: 0; border-top-right-radius: 0;">
            <v-list-item
              v-for="item in navBarData"
              :key="item.title"
              :value="item.title"
              :to="item.value"
            >
              <v-list-item-title style="font-size:13px;">{{ item.title }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-tab>
      <!-- <router-link to="/PriceCalculator" class="routerLink" v-if="userData.access_level == 1">
        <v-tab :value="4">
          Calculate
        </v-tab>
      </router-link> -->
    </v-tabs>
          

    <v-spacer v-if="mdAndUp"></v-spacer>    
          
    <v-btn icon v-if="smAndDown" @click="searchBarVisible = !searchBarVisible">
      <v-icon>mdi-magnify</v-icon>
    </v-btn>
    <v-text-field
      v-if="mdAndUp" 
      :loading="loading"
      density="compact"
      variant="solo"
      label="Search Posts"
      append-inner-icon="mdi-magnify"
      single-line
      hide-details
      v-model="search"
      @click:append-inner="onClick"
      @keyup.enter="onClick"
    ></v-text-field>
          

    <!-- NOTIFICATIONS -->
    <div class="overflow-y-visible ml-1">
      <NotificationTab/>
    </div>

    <!-- USER INFO FALLING TAB -->
    <div class="overflow-y-visible mr-1">
      <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props" @click.stop="drawer = !drawer; searchBarVisible=false;">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
  
        
        <v-list>
          <v-list-item
            :prepend-avatar="this.BASE_URL+'images/users/'+userData.image_url"
            :title="userData.name.toUpperCase()+' '+userData.surname.toUpperCase()"
          ></v-list-item>

          <v-divider></v-divider>
  
          <v-list density="compact" nav>
            <v-list-item :to="`/user/${userData.id}?part=info`" prepend-icon="mdi-view-dashboard" title="More Info" value="User Info"></v-list-item>
            <!-- <v-list-item :to="`/user/${userData.user_id}?part=posts`" prepend-icon="mdi-forum" title="User Posts" value="User Posts"></v-list-item> -->
            <v-list-item title="Language" value="Language">
              <template v-slot:prepend>
                <v-avatar image="../src/assets/images/HR.png" size="24" class="mr-8"></v-avatar>
              </template>
            </v-list-item>
            <v-list-item @click="logout" prepend-icon="mdi-logout" to='/' title="Log out" value="Log out"></v-list-item>
          </v-list>
        </v-list>
      </v-menu>
    </div>
  </v-app-bar>


    <!-- SEARCH BAR IN SMALL DEVICE MODE  -->
  <v-text-field
  v-if="smAndDown && searchBarVisible" 
    :loading="loading"
    density="compact"
    variant="solo"
    label="Search Posts"
    append-inner-icon="mdi-magnify"
    class="search-bar"
    single-line
    hide-details
    v-model="search"
    @click:append-inner="onClick"
    @keyup.enter="onClick"
  ></v-text-field>


  <!-- NAVBAR SMALL DEVICE -->
  <v-navigation-drawer
    v-model="openNavBar"
    location="left"
    temporary
    width="300"
  >
    <v-list v-model:opened="open">
      <v-list-item prepend-icon="mdi-home" title="Home" to="/"></v-list-item>
      
      <v-list-group value="Posts" >
        <template v-slot:activator="{ props }">
          <v-list-item
            v-bind="props"
            prepend-icon="mdi-account-multiple-outline"
            title="Posts"
          ></v-list-item>
        </template>

        <v-list-item prepend-icon="mdi-view-dashboard" title="Posts" to="/postsList"></v-list-item>
        <v-list-item prepend-icon="mdi-plus-outline" title="Insert" @click="this.showInsertOrUpdateDialog({}, 'insert')"></v-list-item>

          
      </v-list-group>


      <v-list-group value="Data" v-if="userData.administrator">
        <template v-slot:activator="{ props }">
          <v-list-item
            v-bind="props"
            prepend-icon="mdi-folder"
            title="Data"
          ></v-list-item>
        </template>

        <v-list-group value="All">
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              title="All"
            ></v-list-item>
          </template>

          <v-list-item
            v-for="([title, icon, url], i) in data"
            :key="i"
            :title="title"
            :prepend-icon="icon"
            :value="title"
            :to="url"
          ></v-list-item>
        </v-list-group>
        <v-list-item title="Latest" to="/DataList"/>
      </v-list-group>

      <v-list-item prepend-icon="mdi-plus" title="Calculator" to="/PriceCalculator" v-if="userData.administrator"></v-list-item>
    </v-list>  
  </v-navigation-drawer>


  <InsertOrUpdateDialog 
    :insertOrUpdateDialog="insertOrUpdateDialog"
    @update:insertOrUpdateDialog="insertOrUpdateDialog = $event"
    :insertOrUpdateDialogItem="insertOrUpdateDialogItem"
    @insertOrUpdateItem="handleInsertOrUpdateItem"
    type="POSTS" typeOfDialog="insert"
  />
</template>

<script>
import InsertOrUpdateDialog from '@/components/InsertOrUpdateDialog.vue'

import axios from 'axios'
import { useDisplay } from 'vuetify'
import { defineComponent } from 'vue'

import { useCounterStore } from '@/stores/counter';
import { mapWritableState } from 'pinia'
import { mapState } from 'pinia'

import NotificationTab from '@/components/NotificationTab.vue'

export default defineComponent({
  components:{
    InsertOrUpdateDialog,
    NotificationTab,
  },
  data() {
    const { xs, mdAndUp, smAndDown } = useDisplay()
    return {

      insertOrUpdateDialog: false,
      insertOrUpdateDialogItem:{},

      // SAMO ZA TEST MAKNI TO KAD RJESIS BEFORE ROUTE PROBLEM
      searchResults:[],

      searchBarVisible: false,
      drawer: null,
      openNavBar: null,
      // tab: null,
      loaded: false,
      loading: false,
      userData:JSON.parse(localStorage.getItem('userData')),
      search:'',
      open: ['Users'],
      data: [
        ['Containers', 'mdi-file-outline', '/database/containers'],
        ['Employes', 'mdi-plus-outline', '/database/employes'],
      ],    
      navBarMain: [
        {
          title: 'Home',
          value: '/',
          icon: 'mdi-home'
        },
        {
          title: 'Posts',
          value: '/postsList',
          icon: 'mdi-account-multiple-outline'
        },
        {
          title: 'Data',
          value: '/DataList',
          icon: 'mdi-folder'
        },
      ],
      navBarData: [
        {
          title: 'LATEST',
          value: '/DataList',
          icon: 'mdi-home'
        },
        {
          title: 'CONTAINERS',
          value: '/database/containers',
          icon: 'mdi-account-multiple-outline'
        },
        {
          title: 'EMPLOYES',
          value: '/database/employes',
          icon: 'mdi-folder'
        },
      ],
      navBarDataPosts: [
        {
          title: 'ALL',
          value: '/postsList',
          icon: 'mdi-folder'
        },
      ],
      xs, mdAndUp, smAndDown
    }
  },
  methods: {
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

    async onClick () {
      await axios.get(this.BASE_URL + 'search/post/'+this.search,
        {
          headers: {
            'Authorization':'Bearer ' + localStorage.getItem('access_token'),
            'Accept': 'application/json'
          }
        })
        .then(response => {
          console.log('this is search.', response);
          this.searchQuery = response.data
          this.$router.push('/postsListSearch');
        })
        .catch(error => {
          console.error('There was an error:', error.response.data);
          if(error.response.data.detail == 'Could not validate credentials'){
            this.logout()          
          }
        });
    },
    logout (){
      this.userLoggedIn = false
      this.setAuthToken = null
      this.setAuthTokenType = null
      this.setUserId = null
      this.setUsername = null
      localStorage.removeItem('access_token');
      localStorage.removeItem('email');
    },
  },
  computed:{
    ...mapState(useCounterStore, ['BASE_URL']),
    ...mapWritableState(useCounterStore, [
      'tab',
      'userLoggedIn',
      'setAuthToken',
      'setAuthTokenType',
      'setUserId',
      'setUsername',

      'searchQuery'
    ]),
  },
})
</script>


<style scoped>
.search-bar {
  position: fixed;
  top: 66px;
  left: 0px;
  right: 0;
  margin: 0 auto;
  z-index: 9999;
  width:300px;
  /* height: 56px; */
  border-radius: 10px;
  /* background:white; */
}
/* .routerLink{
     text-decoration: none;
 } */


</style>
