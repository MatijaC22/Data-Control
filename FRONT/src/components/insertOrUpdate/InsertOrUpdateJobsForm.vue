<template>
  <vee-form @submit="submitData" class="veeform">

              <v-row>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="ReferenceNumber*"
                    v-model="ReferenceNumber"
                    type="input"
                    hide-details
                  ></v-text-field>
                  <span v-if="submitClicked && ReferenceNumberAlarm == ''" style="color:red;">{{ReferenceNumberAlarm}}</span>

                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="Worker id*"
                    v-model="UserId"
                    type="number"
                    min="1"
                    hide-details
                  ></v-text-field>
                  <!-- <span v-if="submitClicked && UserIdAlarm == ''" style="color:red;">{{UserIdAlarm}}</span> -->
                </v-col>
                
                
                <!-- <v-row>
                  <v-col cols="12" sm="6" >
                    <v-file-input
                      mulitple
                      label="Image*"
                      accept="image/*"
                      @change="handleImageUpload"
                      v-model="selectedImages"
                      type='file'
                    ></v-file-input>
                  </v-col>
                  
                  <v-col cols="12" sm="6" >
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
                  </v-col>
                </v-row>
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
                </v-carousel> -->
                
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
      uploadedImage:[],
      selectedImages:null,
      allImages:[],
      allImagesNames:[],
      
      Id:toRaw(this.uniqueItem).id != undefined ? toRaw(this.uniqueItem).id : null,
      ReferenceNumber:toRaw(this.uniqueItem).reference_number != undefined ? toRaw(this.uniqueItem).reference_number : '',
      UserId:toRaw(this.uniqueItem).user_id != undefined ? toRaw(this.uniqueItem).user_id : 1,
      LastModify:toRaw(this.uniqueItem).last_modify != undefined ? toRaw(this.uniqueItem).last_modify : null,
      CreatedAt:toRaw(this.uniqueItem).created_at != undefined ? toRaw(this.uniqueItem).created_at : null,
      
      ReferenceNumberAlarm:'Enter job reference!',
      // UserIdAlarm:'Enter worker id!',
      
      submitClicked:false,

      login_in_submission: false,
      login_show_alert: false,
      login_alert_variant: 'color: white; background-color:#1a1a1a;  border: 1px solid #1a1a1a; box-shadow:0 0 5px rgba(52, 152, 219, .3), 0 0 10px rgba(52, 152, 219, .2), 0 0 15px rgba(52, 152, 219, .1), 0 1px 0 #1a1a1a4',
      login_alert_msg: 'Please wait! Insert is in process.',
    }
  },
  methods:{
    // deleteImage(i){
    //   this.allImagesNames.splice(i,1)
    //   this.allImages.splice(i,1)
    //   this.uploadedImage.splice(i,1);
    // },
    // handleImageUpload(event) {
    //   const file = event.target.files[0];
    //   //HERE IS MISSING PART OF SENDING IN DATABASE FIND A WAY HOW TO CONNECT IT
    //   if (file) {
    //     const reader = new FileReader();

    //     reader.onload = () => {
    //       this.allImages.push(this.selectedImages)
    //       this.allImagesNames.push(event.target.files[0])
    //       console.log(this.allImages)
    //       this.uploadedImage.push(reader.result);
    //     };
    //     reader.readAsDataURL(file);
    //   }
    // },
    ...mapActions(useCounterStore, ['logout','updateJob','insertJob']),

    submitButtonPushed(){
      this.submitClicked = true
    },
    async submitData(values){
      if (this.ReferenceNumber){

        this.login_in_submission = true;
        this.login_show_alert = true;

        let userData = {
          id: this.Id,
          reference_number: this.ReferenceNumber,
          last_modify:this.LastModify,
          created_at:this.CreatedAt,
          user_id: this.UserId,
        }

        if(this.Id){

          this.updateJob(userData)
        }else{

          this.insertJob(userData)
        }
          
        setTimeout(()=>{
          this.$emit('closeWindow',userData);
          if(!this.Id){
            window.location.reload();
          }
        },1000) 
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