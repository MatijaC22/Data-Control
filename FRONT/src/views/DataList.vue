<template>
<v-main>
  <v-container fluid class="pa-1 mt-3">
    <!-- <v-card elevation="2" style="background-image: url('../src/assets/images/background2.jpg');  background-size: cover;"> -->
<v-card class="pa-1" elevation="2" style="background-image: linear-gradient(to top right, rgba(19,84,122,.8), rgba(128,208,199,.8)), url('../src/assets/images/background3.jpg'); background-size: cover;">

    <v-card color="grey-lighten-5"
                    border
                    class="mb-2"
                    density="compact">
    <DataTable :dataItems="containersList" :dataItemsHeaders="containersListHeaders" name="CONTAINERS"/>
    <br>
    </v-card>
    <br><br>
    <v-card color="grey-lighten-5"
                    border
                    class="mb-2"
                    density="compact">
    <DataTable :dataItems="employesList" :dataItemsHeaders="employesListHeaders" name="EMPLOYES"/>
    <br>
    </v-card>
    <br><br>
    <v-card color="grey-lighten-5"
                    border
                    density="compact">
    <DataTable :dataItems="dataItems" :dataItemsHeaders="dataItemsHeaders" name="Something third"/>
    <br>
    </v-card>
    </v-card>

  </v-container>
</v-main>
</template>

<script>
import DataTable from '@/components/DataTable.vue'
export default {
  components:{
    DataTable
  },
  data() {
    return{
    containersListHeaders:['id','reference_number','location','country','responsible_name','responsible_email','client_name','transport_type','product_type','last_modify','created_at','View','Action'],
    containersList : [
  {
    id: 1,
    reference_number: '3224301',
    location: 'San Miguel',
    country: 'Bolivia',
    responsible_name: 'Mark',
    responsible_email: 'luka@gmail.com',
    client_name: 'Sin Xaio Hel',
    transport_type: 'Sea',
    product_type: 'Oil',
    last_modify: '07/15/2020',
    created_at: '07/15/2020',
  },
  {
    id: 2,
    reference_number: '5678912',
    location: 'New York',
    country: 'United States',
    responsible_name: 'John',
    responsible_email: 'john@gmail.com',
    client_name: 'ABC Company',
    transport_type: 'Air',
    product_type: 'Electronics',
    last_modify: '09/20/2021',
    created_at: '09/20/2021',
  }
    ],

    employesListHeaders:['id','legalFirstName','legalMiddleName','legalLastName','email','password','age','Position','View','Action'],
    employesList: [
      {
        id:'4',
        legalFirstName:'Matija',
        legalMiddleName:'Marin',
        legalLastName:'Corak',
        email:'matija@gmail.com',
        password:'*****',
        age:'30-54',
        Position:'Driver',
      },
      {
        id:'5',
        legalFirstName:'Pero',
        legalMiddleName:'Marin',
        legalLastName:'Corak',
        email:'matija@gmail.com',
        password:'*****',
        age:'30-54',
        Position:'Driver',
      }
    ],
      dataItemsHeaders:['name','surname','country','lastModify','url','View','Action'],
      dataItems: [
        {
          name: 'Frozen Yogurt',
          surname: 'Krazy',
          country: 'Croatia',
          lastModify: '15/10/2023',
          url:'/post/Ref34856'
        },
        {
          name: 'Ice cream sandwich',
          surname: 'Frozy',
          country: 'Croatia',
          lastModify: '15/10/2023', 
          url:'/user/1'
        },
        {
          name: 'Eclair',
          surname: 'Frozy',
          country: 'Croatia',
          lastModify: '15/10/2021',
          url:'/post/3'
        }
      ],
    }
  },
}
</script>


<style scoped>

</style>