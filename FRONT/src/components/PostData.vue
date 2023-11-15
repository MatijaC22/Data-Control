<template>
  <v-row justify="center" style="padding-top:12px;">
    <v-card
      v-for="post in postList"
      :key="post.id"
      border
      class="mb-4"
      density="compact"
      variant="text"
      style="background-color:white;"
      :width="800"
      
    >
      <v-list-item :title="post.user.name.toUpperCase() + ' ' + post.user.last_name.toUpperCase()" :subtitle="'Ref: ' + post.reference_number" value="Card details">
        <template v-slot:prepend>
          <router-link :to="'/user/' + post.user.id + '?part=info'" @click="tab=0">
            <v-avatar :image="this.BASE_URL+'images/users/'+post.user.image_url" size="38" class="mr-4"></v-avatar>
          </router-link>
        </template>
      </v-list-item>

      
      <v-img 
        :src="this.BASE_URL+'images/posts/'+post.reference_number+'/'+post.image_url.split(',')[0]" 
        height="328"
        style="object-fit: contain; object-position: center; border: 1px solid gray; background-color:black;"
      ></v-img>

      <v-card-text>
        {{post.description}}
      </v-card-text>

      <template v-slot:actions>
        <v-btn color="primary" variant="text" :to="'/post/' + post.id" @click="tab=0">View More</v-btn>
        <v-btn color="primary" variant="text">See in Map</v-btn>
      </template>
    </v-card>
  </v-row>
</template>


<script>
import { useCounterStore } from '@/stores/counter';
import { mapWritableState } from 'pinia'
import { mapState } from 'pinia'


export default {
  props:{
    postList: {
      type: Array,
      required: true,
    },
  },
  data() {
    return{
    }
  },
  computed:{
    ...mapWritableState(useCounterStore, ['tab']),
    ...mapState(useCounterStore, ['BASE_URL']),

  },
  methods:{
  }
}
</script>

<style scoped>

</style>