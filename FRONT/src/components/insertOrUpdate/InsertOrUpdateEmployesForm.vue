<template>
  <vee-form @submit="submitData" class="veeform">
              <v-row>
                <v-col cols="12" sm="6" md="4">
                  <v-checkbox 
                    label="Active"
                    v-model="Active"
                    type="input"
                    hide-details
                  ></v-checkbox>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="AccessLevel"
                    v-model="AccessLevel"
                    type="number"
                    min="0"
                    hide-details                                  
                  ></v-text-field>
                  <span v-if="submitClicked && isNaN(AccessLevel)" style="color:red;">{{AccessLevelAlarm}}</span>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="Password*"
                    v-model="Password"
                    type="input"
                    hide-details
                  ></v-text-field>
                  <span v-if="submitClicked && Password == ''" style="color:red;">{{PasswordAlarm}}</span>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="Email*"
                    v-model="Email"
                    type="input"
                    hide-details
                  ></v-text-field>
                  <span v-if="submitClicked && Email == ''" style="color:red;">{{EmailAlarm}}</span>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="Name*"
                    v-model="Name"
                    type="input"
                    hide-details
                  ></v-text-field>
                  <span v-if="submitClicked && Name == ''" style="color:red;">{{NameAlarm}}</span>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="Surname*"
                    v-model="Surname"
                    type="input"
                    hide-details
                  ></v-text-field>
                  <span v-if="submitClicked && Surname == ''" style="color:red;">{{SurnameAlarm}}</span>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-select
                    label="Nationality*"
                    v-model="Nationality"
                    :items="['Croatian', 'German', 'Polish', 'Italian']"
                    hide-details
                  ></v-select>
                  <span v-if="submitClicked && !Nationality.length" style="color:red;">{{NationalityAlarm}}</span>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    v-model="DateOfBirth"
                    label="Date of Birth"
                    type="date"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-file-input
                    mulitple
                    label="Image*"
                    accept="image/*"
                    @change="handleImageUpload"
                    v-model="selectedImages"
                    type='file'
                  ></v-file-input>

                  <img v-if="uploadedImage" :src="uploadedImage" alt="Uploaded Image" style="max-width: 250px; margin-left:40px;">
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
      Id: toRaw(this.uniqueItem).id != undefined ? toRaw(this.uniqueItem).id : null,
      Name:toRaw(this.uniqueItem).name != undefined ? toRaw(this.uniqueItem).name : '',
      Surname:toRaw(this.uniqueItem).surname != undefined ? toRaw(this.uniqueItem).surname : '', 
      Password:toRaw(this.uniqueItem).password != undefined ? toRaw(this.uniqueItem).password : '',
      Email:toRaw(this.uniqueItem).email != undefined ? toRaw(this.uniqueItem).email : '',
      DateOfBirth: toRaw(this.uniqueItem).date_of_birth != undefined ? new Date(toRaw(this.uniqueItem).date_of_birth).toISOString().split('T')[0] : null,
      ImageUrl:toRaw(this.uniqueItem).image_url != undefined ? toRaw(this.uniqueItem).image_url : '',
      Nationality:toRaw(this.uniqueItem).nationality != undefined ? toRaw(this.uniqueItem).nationality : '',
      AccessLevel:toRaw(this.uniqueItem).access_level != undefined ? toRaw(this.uniqueItem).access_level : 0,
      Active:toRaw(this.uniqueItem).active != undefined ? toRaw(this.uniqueItem).active : false,
      
      NameAlarm:'Enter user first name!',
      AccessLevelAlarm:'Enter number!',
      EmailAlarm:'Enter user email!',
      SurnameAlarm:'Enter user last name!',
      NationalityAlarm:'Enter user nationality!',
      PasswordAlarm:'Enter user password!',
      submitClicked:false,
      
      selectedImages: [],    
      uploadedImage: null, // Base64-encoded image data


      login_in_submission: false,
      login_show_alert: false,
      login_alert_variant: 'color: white; background-color:#1a1a1a; border: 1px solid #1a1a1a; box-shadow:0 0 5px rgba(52, 152, 219, .3), 0 0 10px rgba(52, 152, 219, .2), 0 0 15px rgba(52, 152, 219, .1), 0 1px 0 #1a1a1a4',
      login_alert_msg: 'Please wait! Employ is getting inserted.',
    }
  },
  methods:{
    ...mapActions(useCounterStore, ['logout','updateUser','insertUser','uploadImage']),
    
    submitButtonPushed(){
      this.submitClicked = true
    },
    async submitData(values){
      if(this.Nationality && this.Name && this.DateOfBirth && this.Surname && this.Email && this.Password){

        this.login_in_submission = true;
        this.login_show_alert = true;

        let userData = {
          id: this.Id,
          active: this.Active,
          access_level: this.AccessLevel,
          email: this.Email,
          name: this.Name,
          surname: this.Surname,
          image_url: 'asstes/images/users/'+this.Email,
          nationality: this.Nationality,
          password: this.Password,
          date_of_birth: new Date(this.DateOfBirth).toISOString()//'2023-11-14T17:39:10.528Z'
        }
        // console.log(userData)

       
        let image_name = this.Email
        if(this.Id){
          this.updateUser(userData)
          
          if(this.ImageUrl == '' && this.selectedImages){
            
            this.uploadImage(image_name, this.selectedImages)
          }
        }else{
          this.insertUser(userData)
          
          if(this.ImageUrl == '' && this.selectedImages){
  
            this.uploadImage(image_name, this.selectedImages)
          }
        }
                        
        setTimeout(()=>{
          this.$emit('closeWindow',userData);
          if(!this.Id){
            window.location.reload();
          }
        },1000)



        // this.login_in_submission = true;
        // this.login_show_alert = true;
        // this.login_alert_variant = 'color: white; background-color:#1a1a1a;  border: 1px solid #1a1a1a; box-shadow:0 0 5px rgba(52, 152, 219, .3), 0 0 10px rgba(52, 152, 219, .2), 0 0 15px rgba(52, 152, 219, .1), 0 1px 0 #1a1a1a4';
        // this.login_alert_msg = 'Please wait! We are logging you in.';
      }
      
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      // selectedImages = file.name
      // console.log('file')
      // console.log(file.name)
      // console.log(file.type)
      if (file) {
        const reader = new FileReader();

        reader.onload = () => {
          this.uploadedImage = reader.result;
        };
        reader.readAsDataURL(file);
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
      return new Proxy(this.uniqueItem,{});
    },
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