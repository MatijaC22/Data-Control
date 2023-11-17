<template>
  <vee-form @submit="submitData" class="veeform">

              <v-row>
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
                  <v-text-field
                    label="Location"
                    v-model="Location"
                    type="input"
                    hide-details
                  ></v-text-field>
                  <!-- <span v-if="submitClicked && Location == ''" style="color:red;">{{LocationAlarm}}</span> -->
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-select
                    label="Country*"
                    v-model="Country"
                    :items="['Guatemala', 'Mexico', 'Peru', 'Costa Rica']"
                    hide-details
                  ></v-select>
                  <span v-if="submitClicked && !Country.length" style="color:red;">{{CountryAlarm}}</span>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    label="Responsible Name*"
                    v-model="ResponsibleName"
                    type="input"
                    class="mt-4"
                    hide-details
                  ></v-text-field>
                  <span v-if="submitClicked && ResponsibleName == ''" style="color:red;">{{ResponsibleNameAlarm}}</span>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    label="Responsible Email*"
                    v-model="ResponsibleEmail"
                    type="input"
                    class="mt-4"
                    hide-details
                  ></v-text-field>
                  <span v-if="submitClicked && ResponsibleEmail == ''" style="color:red;">{{ResponsibleEmailAlarm}}</span>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    label="Client Name*"
                    v-model="ClientName"
                    type="input"
                    hide-details
                  ></v-text-field>
                  <span v-if="submitClicked && ClientName == ''" style="color:red;">{{ClientNameAlarm}}</span>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-select
                    label="Transport Type*"
                    v-model="TransportType"
                    :items="['Air', 'Land', 'Sea']"
                    class="mt-4"
                    hide-details
                  ></v-select>
                  <span v-if="submitClicked && !TransportType.length" style="color:red;">{{TransportTypeAlarm}}</span>
                </v-col>
                <v-col cols="12" sm="6" >
                  <v-autocomplete
                    :items="['Oil', 'Cooking Oil', 'Greese', 'Cleaning liquid']"
                    label="Product Type*"
                    v-model="ProductType"
                    hint="enter type of the product"
                    class="mt-4"
                    multiple
                    hide-details
                  ></v-autocomplete>
                  <span v-if="submitClicked && !ProductType.length" style="color:red;">{{ProductTypeAlarm}}</span>
                </v-col>
                <!-- here is testing purpose for image carousel -->
                <v-file-input
                    mulitple
                    label="Image*"
                    accept="image/*"
                    @change="handleImageUpload"
                    v-model="selectedImages"
                    type='file'
                  ></v-file-input>
                  <!-- <v-card> -->
                  
                  <div v-if="allImagesNames.length > 0">
                    <h4>Selected Image Names:</h4>
                    <v-list>
                      <v-list-item v-for="(image,i) in allImagesNames" :key="i">
                        <v-list-item-content>
                          {{ image.name }}
                        </v-list-item-content>

                        <v-list-item-icon>
                          <v-icon @click="deleteImage(i)">mdi-delete</v-icon>
                        </v-list-item-icon>
                      </v-list-item>
                    </v-list>
                  </div> 
                <!-- </v-card> -->
                <v-carousel
                  cycle
                  height="400"
                  hide-delimiter-background
                  show-arrows="hover"
                  v-if="uploadedImage.length"
                >
                  <v-carousel-item
                    v-for="(slide, i) in uploadedImage"
                    :src="slide"
                    :key="i"
                    style="object-fit: contain; object-position: center; background-color:black;"
                  >
                  </v-carousel-item>
                </v-carousel>
                
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
import axios from 'axios'

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
      uploadedImage:[],
      selectedImages:null,
      allImages:[],
      allImagesNames:[],
      // loginSchema: {
      //   ref:'required|min:3|max:32',
      //   location:'required',
      //   ResponsibleName: 'required',
      //   clientName: 'required'
      // },
      Reference:toRaw(this.uniqueItem).reference_number != undefined ? toRaw(this.uniqueItem).reference_number : '',
      Location:toRaw(this.uniqueItem).location != undefined ? toRaw(this.uniqueItem).location : '',
      ResponsibleName:toRaw(this.uniqueItem).responsible_name != undefined ? toRaw(this.uniqueItem).responsible_name : '',
      ResponsibleEmail:toRaw(this.uniqueItem).responsible_email != undefined ? toRaw(this.uniqueItem).responsible_email : '',
      ClientName:toRaw(this.uniqueItem).client_name != undefined ? toRaw(this.uniqueItem).client_name : '',
      Country:toRaw(this.uniqueItem).country != undefined ? toRaw(this.uniqueItem).country : [],
      TransportType:toRaw(this.uniqueItem).transport_type != undefined ? toRaw(this.uniqueItem).transport_type : [],
      ProductType:toRaw(this.uniqueItem).product_type != undefined ? toRaw(this.uniqueItem).product_type : [],
      ReferenceAlarm:'Enter container reference!',
      // LocationAlarm:'Enter location!',
      ResponsibleNameAlarm:'Enter supervisor name!',
      ResponsibleEmailAlarm:'Enter supervisor email!',
      ClientNameAlarm:'Enter client name!',
      CountryAlarm: 'Choose country!',
      TransportTypeAlarm: 'Choose type of transport!',
      ProductTypeAlarm: 'Choose at least one option!',
      submitClicked:false,

      


      login_in_submission: false,
      login_show_alert: false,
      login_alert_variant: 'color: white; background-color:#1a1a1a;  border: 1px solid #1a1a1a; box-shadow:0 0 5px rgba(52, 152, 219, .3), 0 0 10px rgba(52, 152, 219, .2), 0 0 15px rgba(52, 152, 219, .1), 0 1px 0 #1a1a1a4',
      login_alert_msg: 'Please wait! Insert is in process.',
    }
  },
  methods:{
    deleteImage(i){
      this.allImagesNames.splice(i,1)
      this.allImages.splice(i,1)
      this.uploadedImage.splice(i,1);
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      //HERE IS MISSING PART OF SENDING IN DATABASE FIND A WAY HOW TO CONNECT IT
      if (file) {
        const reader = new FileReader();

        reader.onload = () => {
          this.allImages.push(this.selectedImages)
          this.allImagesNames.push(event.target.files[0])
          console.log(this.allImages)
          this.uploadedImage.push(reader.result);
        };
        reader.readAsDataURL(file);
      }
    },
    ...mapActions(useCounterStore, ['logout']),

    submitButtonPushed(){
      this.submitClicked = true
    },
    async submitData(values){
      if(
        this.Country.length && 
        this.TransportType.length && 
        this.ProductType.length && 
        this.Reference && 
        this.ResponsibleEmail && 
        this.ResponsibleName && 
        this.ClientName
        ){

        this.login_in_submission = true;
        this.login_show_alert = true;


        const formData = new FormData();
        
                
        formData.append('country', this.Country);
        formData.append('transport_type', this.TransportType);
        formData.append('product_type', Object.values(this.ProductType).join(', '));
        formData.append('reference_number', this.Reference);
        formData.append('location', this.Location);
        formData.append('responsible_name', this.ResponsibleName);
        formData.append('responsible_email', this.ResponsibleEmail);
        formData.append('client_name', this.ClientName);
        
        // console.log(this.Country)
        // console.log(Object.values(this.ProductType).join(', '))
        // console.log(this.ProductType)
        // console.log(this.Reference)
        // console.log(this.Location)
        // console.log(this.ResponsibleName)
        // console.log(this.ResponsibleEmail)
        // console.log(this.ClientName)

        await axios.post(this.BASE_URL+'container/create', formData,
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
            this.login_alert_msg = 'Success! You have inserted new container.';
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
        // this.login_in_submission = true;
        // this.login_show_alert = true;
        // this.login_alert_variant = 'color: white; background-color:#1a1a1a;  border: 1px solid #1a1a1a; box-shadow:0 0 5px rgba(52, 152, 219, .3), 0 0 10px rgba(52, 152, 219, .2), 0 0 15px rgba(52, 152, 219, .1), 0 1px 0 #1a1a1a4';
        // this.login_alert_msg = 'Please wait! We are logging you in.';

        // values['Country'] = this.Country
        // values['TransportType'] = this.TransportType
        // values['ProductType'] = this.ProductType
        // values['Reference'] = this.Reference
        // values['Location'] = this.Location
        // values['ResponsibleName'] = this.ResponsibleName
        // values['ResponsibleEmail'] = this.ResponsibleEmail
        // values['ClientName'] = this.ClientName

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