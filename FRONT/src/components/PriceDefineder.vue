<template>
<v-card>
          <v-card-title class="mt-10">
            <span class="text-h5">Calculate Price</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="Input A*"
                    v-model="A"
                    type="number"
                    hide-details
                    :class="{ 'thin-border': A_old !== A, 'no-border': A_old === A }"    
                                  
                  ></v-text-field>
                  <!-- <span v-if="submitClicked && A == null" style="color:red;">{{AAlarm}}</span> -->
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="Input B*"
                    v-model="B"
                    type="number"
                    hide-details
                    :class="{ 'thin-border': B_old !== B, 'no-border': B_old === B }"                  
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="Input C*"
                    v-model="C"
                    type="number"
                    hide-details
                    :class="{ 'thin-border': C_old !== C, 'no-border': C_old === C }"                  
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-select
                    label="Tax*"
                    v-model="Tax"
                    :items="['15%', '20%', '45%', '70%']"
                    hide-details
                    :class="{ 'thin-border': Tax_old !== Tax, 'no-border': Tax_old === Tax }"                  
                  ></v-select>
                </v-col>
              </v-row>
      <v-btn 
        type="submit" 
        block 
        class="mt-10 "
        @click="calculate"
        :disabled="A == null || A == '' || B == null || B == '' || C == null || C == ''"
        >
        Define Price
      </v-btn>
      <v-btn 
        block 
        class="mt-5"
        disabled
        style="color:green;"
        >
        Price: {{result}} $ and {{result*currencyValue}} {{currency}}
      </v-btn>
    </v-container>
  </v-card-text>          
</v-card>
</template>

<script>

export default {
  props:{
    currency: {
      type: String,
      required: true,
    },
    currencyValue: {
      type: Float64Array,
      required: true,
    },
  },
  data() {
    return{
      result:null,
      A:null,
      A_old:null,
      B:null,
      B_old:null,
      C:null,
      C_old:null,
      Tax:'100',
      Tax_old:'100',
    }
  },
  methods:{
    calculate(){
      this.result = (parseFloat(this.A)+parseFloat(this.B)+parseFloat(this.C))*parseInt(this.Tax.replace(/\D/g,''))/100
      this.A_old = this.A
      this.B_old = this.B
      this.C_old = this.C
      this.Tax_old = this.Tax
    }
  }
}
</script>


<style scoped>

.thin-border {
  border-color: yellow;
  border-width: 0.5px;
  border-style: solid;
}

.no-border {
  border-width: 0;
}
</style>
