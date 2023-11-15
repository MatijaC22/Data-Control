<template>
<div>
  
  <v-card border density="compact" :title="name" variant="text">
    <tr style="min-width:100%;">
      <div style="display:flex; align-items:center;">
        <div style="flex-grow: 1;">
          <v-text-field
              :loading="loading"
              density="compact"
              variant="solo-filled"
              label="Search"
              append-inner-icon="mdi-magnify"
              single-line
              hide-details
              style="min-width:230px; margin: 0 10px 0 15px;"
              v-model="search"
            >
          </v-text-field>
        </div>
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn
              color="primary"
              v-bind="props"
              style="margin-bottom:0px;"
              height="42"
              class="mr-2"
              v-if="this.$route.fullPath.includes('database')"
            >
              Filter
            </v-btn>
          </template>
          <v-card border
            density="compact"
            variant="text"
          >
          </v-card>
        </v-menu> 
        <v-btn
          color="primary"
          v-bind="props"
          style="margin-bottom:0px;"
          height="42"
          @click="this.exportExcel(this.filteredItems)"
        >
          Download
        </v-btn>         
        <v-btn
          color="primary"
          v-bind="props"
          height="42"
          class="ml-2"
          @click="this.showInsertOrUpdateDialog({}, 'insert')"
        >
          INSERT
        </v-btn>
    </div>
  </tr>

  <!-- <br> -->
 

  <!-- height je sada 63.5vh ali treba viit kako to nastimati korektno -->
  <v-table
    fixed-header
    height="63.5vh"
    density="compact"
    class="mt-2"
  >
  <thead>
    <tr>
      <th class="text-left"
        v-for="(title, index) in dataItemsHeaders"
        :key="index"
      >
        {{ title }}
      </th>
    </tr>
  </thead>
    <tbody>
      <tr v-for="(item, index) in paginatedItems" :key="index">
        <td v-for="(value, key) in item" :key="key" :style="`max-width:300px; color: ${key=='last_modify' && isOlderThan30Days(item.last_modify) ? 'red' : 'black'}`">{{ (key.indexOf('last_modify') != (-1) || key.indexOf('created_at')  != (-1)) ? formatDate(value) : value }}</td>
        <td>
          <div v-if="name == 'CONTAINERS'" @click="copyContainersDetails(item)" style="color:black; cursor:pointer;">
            Copy
          </div>
          <router-link v-if="name == 'EMPLOYES'" :to="'/user/'+item.id" class="routerLink" style="color:black;">
            View
          </router-link>
        </td>
        <td>
          <v-btn icon size="small" class="mr-1 my-1" @click="this.showDeleteDialog(item)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
          <v-btn icon  @click="this.showInsertOrUpdateDialog(item, 'update')" size="small" class="my-1">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </td>
      </tr>           
    </tbody>
  </v-table>

  <div class="text-center">
    <v-pagination
      size="small"
      v-model="currentPage"
      :length="totalPages"
      rounded="circle"
    ></v-pagination>
  </div>

  </v-card>
  </div>

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
      :type="name" 
      :typeOfDialog="typeOfDialog"
    />


</template>

<script>

import moment from 'moment';
import InsertOrUpdateDialog from '@/components/InsertOrUpdateDialog.vue'
import DeleteDialog from '@/components/DeleteItemDialog.vue'

import xlsx from 'xlsx/dist/xlsx.full.min';


import { useCounterStore } from '@/stores/counter';
import { mapState } from 'pinia'
import { mapActions } from 'pinia'

export default {
  components:{
    InsertOrUpdateDialog,
    DeleteDialog,
  },
  props: {
    dataItems: {
      type: Array,
      required: true,
    },
    dataItemsHeaders: {
      type: Array,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
  },
  data() {
    return{
      //VIDI STO S TIM TO SAM STAVIO SAMO DA ZAUSTAVIM WARNINGE
      props:null,
      loading:null,

      checkboxes: [],
      search: '',
      list: this.dataItems,
      currentPage: 1,
      itemsPerPage: 10,
      insertOrUpdateDialog: false,
      chosenItem:{},
      deleteDialog: false,
      deleteDialogItem:{},
      typeOfDialog:'insert',
    }
  },
  computed: {
    filteredItems(){
      console.log(this.list)
      return this.list.filter((data) => {
        const values = Object.values(data)
        return values.some((value) => {
          return String(value).toLowerCase().includes(this.search.toLowerCase())
        })
      })
    },
    totalPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage);
    },
    paginatedItems() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.filteredItems.slice(startIndex, endIndex);
    },
  },
  methods:{
    ...mapActions(useCounterStore, ['deleteUser']),

    formatDate(timestamp) {
      const dateObj = new Date(timestamp);
      const year = dateObj.getFullYear();
      const month = dateObj.getMonth() + 1;
      const date = dateObj.getDate();
      const hours = dateObj.getHours();
      const minutes = dateObj.getMinutes();
      const seconds = dateObj.getSeconds();
      return `${year}-${month}-${date}`;
    },
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage -= 1;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage += 1;
      }
    },
    isOlderThan30Days(dateStr) {
      const today = moment();
      const date = moment(dateStr, 'DD/MM/YYYY');
      const daysDifference = today.diff(date, 'days');
      return daysDifference > 30;
    },
    showInsertOrUpdateDialog(item,typeOfDialog){
      this.typeOfDialog = typeOfDialog;
      this.chosenItem = item;
      this.insertOrUpdateDialog = true;
    },
    handleInsertOrUpdateItem(item) {
      
      const orderedItem = {};
      this.dataItemsHeaders.forEach(key => {
        if (item.hasOwnProperty(key)) {
          orderedItem[key] = item[key];
        }
      });

      const existingItemIndex = this.list.findIndex(itemLine => itemLine.id === orderedItem.id);

      if (existingItemIndex !== -1) {
        this.list[existingItemIndex] = orderedItem;
      } else {
        this.list.push(orderedItem);
      }
      // window.location.reload();

    },
    showDeleteDialog(item) {
      this.deleteDialogItem = item;
      this.deleteDialog = true;
    },
    handleDeleteItem(item) {
      // Do something with item here
      console.log('delete');
      console.log(item);
      if(this.name == 'EMPLOYES'){
        this.deleteUser(item.id)
      }else{
        console.log('NOT FINISHED YET')
      }

      this.list = this.list.filter(itemLine => itemLine.id !== item.id);
    },
    exportExcel(data){
      const XLSX = xlsx
      const workbook = XLSX.utils.book_new();
      const worksheet = XLSX.utils.json_to_sheet(data);
      XLSX.utils.book_append_sheet(workbook, worksheet, "framework")
      XLSX.writeFile(workbook, this.name + '.xlsx')
    },
    copyContainersDetails(item){
      const textToCopy = `Container details: reference_number: ${item.reference_number}; country: ${item.country}; responsible name contact: ${item.responsible_email}; `;

      navigator.clipboard.writeText(textToCopy)
        .then(() => {
          console.log('Text copied to clipboard');
          // Optionally, you can show a success message or perform any other action here
        })
        .catch((error) => {
          console.error('Unable to copy text to clipboard:', error);
          // Optionally, you can show an error message or perform any other action here
        });
    }
    
  }
}
</script>


<style scoped>

</style>