<template>
  <vee-form @submit="submitData" class="veeform">

    <v-row>
      <v-col cols="12" sm="6" md="4">
        <v-text-field
          label="Description*"
          v-model="Description"
          type="input"
          hide-details
        ></v-text-field>
        <span v-if="submitClicked && Description == ''" style="color:red;">{{DescriptionAlarm}}</span>
      </v-col>
      <v-col cols="12" sm="6" md="4">
        <v-text-field
          label="Reference*"
          v-model="Reference"
          type="input"
          hide-details
        ></v-text-field>
        <span v-if="submitClicked && Reference == ''" style="color:red;">{{ReferenceAlarm}}</span>
      </v-col>
      <v-col cols="12" sm="6" md="4">
        <v-file-input
          multiple
          label="Image"
          accept="image/*"
          v-model="selectedImages"
        ></v-file-input>
      </v-col>
    </v-row>


    <v-btn 
      type="submit" 
      block 
      class="mt-10 submit"
      @click="submitButtonPushed"
      :disabled="login_in_submission"
      >
      Submit

    </v-btn>
  </vee-form>

  <br>
  <div v-if="login_show_alert" :style="login_alert_variant" style="text-align:center;">
    {{ login_alert_msg }}
  </div>
</template>

<script>
import { toRaw } from 'vue';
import axios from 'axios';

import { useCounterStore } from '@/stores/counter';
import { mapState } from 'pinia'
import { mapActions } from 'pinia'
export default {
  props:{
    uniqueItem: {
      type: Object,
      required: true,
    },
    type: {
      type: String,
      required: true,
    }
  },
  data() {
    return{
      
      selectedImages: [],

      // Title:toRaw(this.uniqueItem).Title != undefined ? toRaw(this.uniqueItem).Title : '',
      Description:toRaw(this.uniqueItem).description != undefined ? toRaw(this.uniqueItem).description : '',
      Reference:toRaw(this.uniqueItem).reference_number != undefined ? toRaw(this.uniqueItem).reference_number : '',
      // TitleAlarm:'Enter post title!',
      DescriptionAlarm:'Enter post description!',
      ReferenceAlarm:'Enter post reference!',
      
      submitClicked:false,

      


      login_in_submission: false,
      login_show_alert: false,
      login_alert_variant: 'color: white; background-color:#1a1a1a;  border: 1px solid #1a1a1a; box-shadow:0 0 5px rgba(52, 152, 219, .3), 0 0 10px rgba(52, 152, 219, .2), 0 0 15px rgba(52, 152, 219, .1), 0 1px 0 #1a1a1a4',
      login_alert_msg: 'Please wait! Insert is in process.',
    }
  },
  methods:{
    ...mapActions(useCounterStore, ['logout']),

    submitButtonPushed(){
      this.submitClicked = true
    },
    async submitData(values){

      
      if(this.Reference && this.Description){
        
        this.login_in_submission = true;
        this.login_show_alert = true;
        
        const formData = new FormData();
        
        for (let i = 0; i < this.selectedImages.length; i++) {
          const file = this.selectedImages[i];
          formData.append('images', file);
        }
        
        formData.append('reference', this.Reference);
        formData.append('description', this.Description);
        console.log(formData)

        await axios.post(this.BASE_URL+'post/create', formData,
        {
          headers: {
            'Authorization':'Bearer ' + localStorage.getItem('access_token'),
            'Accept': 'application/json',
            'Content-Type': 'multipart/form-data' 
          }
        })
          .then(response => {
            // Handle the response from the backend
            console.log('Form submitted successfully', response.data);
            this.login_in_submission = true;
            this.login_alert_variant = 'color: white; background-color:#339933; border: 1px solid #339933; box-shadow: 0 0 5px rgba(0,255,0,.3), 0 0 10px rgba(0,255,0,.2), 0 0 15px rgba(0,255,0,.1), 0 1px 0 #339933;';
            this.login_alert_msg = 'Success! You have inserted new post.';
          })
          .catch(error => {
            // Handle errors
            console.error('Error submitting form', error);
            if(error.response.data.detail == 'Could not validate credentials'){
              this.logout()          
            }
            this.login_in_submission = true;
            this.login_alert_variant = 'color: white; background-color:#990000;  border: 1px solid #990000;  box-shadow: 0 0 5px rgba(255,0,0,.3), 0 0 10px rgba(255,0,0,.2), 0 0 15px rgba(255,0,0,.1), 0 1px 0 #990000';
            this.login_alert_msg = error.response.data.detail;
            return
          });

          
          setTimeout(()=>{
            window.location.reload();
          },5000)
        // window.location.reload();
        // this.login_in_submission = true;
        // this.login_show_alert = true;
        // this.login_alert_variant = 'color: white; background-color:#1a1a1a;  border: 1px solid #1a1a1a; box-shadow:0 0 5px rgba(52, 152, 219, .3), 0 0 10px rgba(52, 152, 219, .2), 0 0 15px rgba(52, 152, 219, .1), 0 1px 0 #1a1a1a4';
        // this.login_alert_msg = 'Please wait! We are logging you in.';

        // values['Title'] = this.Title
        // values['Description'] = this.Description
        // values['Reference'] = this.Reference

        // this.$emit('update:insertOrUpdateItem', values);
        // this.$emit("enter-in-db", values);

        // console.log(values)
      }
      
    }
  },
  created(){
    console.log(toRaw(this.uniqueItem))

    // console.log(this.uniqueItem)
  },
  computed: {
    ...mapState(useCounterStore, ['BASE_URL']),

    myProxy() {
      console.log(new Proxy(this.uniqueItem,{}))
      return new Proxy(this.uniqueItem,{}
      //  {
      //   get(target, key) {
      //     console.log(`Getting ${key} value: ${target[key]}`);
      //     return target[key];
      //   },
      //   set(target, key, value) {
      //     console.log(`Setting ${key} value: ${value}`);
      //     target[key] = value;
      //     return true;
      //   }
      // }
      );
    }
  }
}
</script>


<style lang="scss" scoped>
@import url('https://fonts.googleapis.com/css?family=Poppins&display=swap');

.text{
  font-size: 30px;
  color: white;
  font-weight: 600;
  letter-spacing: 2px;
  // text-align:center;
}
// .veeform{
//   margin-top: 10px;
// }
.veeform .field{
  margin-top: 20px;
  display: flex;
}
.field .fas{
  height: 50px;
  width: 60px;
  color: #868686;
  font-size: 20px;
  line-height: 50px;
  border-bottom: 1px solid #444;
  border-right: none;
  border-radius: 5px 0 0 5px;
  background: linear-gradient(#333,#222);
}
.field .veeinput,.veeform button{
  height: 50px;
  width: 100%;
  outline: none;
  font-size: 16px;
  color: #bbb;
  padding: 0 15px;
  border-radius: 0 5px 5px 0;
  border-bottom: 1px solid #bbb;
  caret-color: #3399cc;
  // background: linear-gradient(#333,#222);
  // background: linear-gradient(#bbb, #ddd);
  background: linear-gradient(#F8F8F8	, #F8F8F8);
  // background: linear-gradient(#DDD, #BBB);
  // background: linear-gradient(hsl(0, 0%, 50%), hsl(0, 0%, 30%));




}
.veeinput:focus {
  color: #3399cc;
  box-shadow: 0 0 5px rgba(0, 191, 255, 0.2),
              inset 0 0 5px rgba(0, 191, 255, 0.1);
  // background: linear-gradient(#333933, #222922);
  animation: glow .8s ease-out infinite alternate;
}

@keyframes glow {
  0% {
    border-color: #3399cc;
    // box-shadow: 0 0 5px rgba(0, 191, 255, 0.2),
    //             inset 0 0 5px rgba(0, 0, 0, 0.1);
  }
  100% {
    border-color: #99ccff;
    // box-shadow: 0 0 20px rgba(0, 191, 255, 0.6),
    //             inset 0 0 10px rgba(0, 191, 255, 0.4);
  }
}

.submit{
  margin-top: 30px;
  border-radius: 5px!important;
  font-weight: 600;
  letter-spacing: 1px;
  cursor: pointer;
}
.submit:hover{
  color: #3399cc;
  border: 1px solid #3399cc;
  box-shadow: 0 0 5px rgba(0, 191, 255, 0.3),
              0 0 10px rgba(0, 191, 255, 0.2),
              0 0 15px rgba(0, 191, 255, 0.1);
}

</style>