<template>
  <v-dialog v-model="dialogValue" width="auto">
      <v-card>
        <v-card-text>
          Are you sure you want to delete item:
          <div class="overflow-y-auto mt-2 ml-4 pa-0" style="max-height:200px;">
            <v-card-text v-for="(info, key) in deleteDialogItem" :key="key" class="pa-1">{{ key }} : {{ info }}</v-card-text>
          </div>
        </v-card-text>
        <v-row justify="center" align="center" class="mb-1">
          <v-card-actions>
            <v-btn color="primary" block @click="deleteItem">YES</v-btn>
          </v-card-actions>
          <v-card-actions>
            <v-btn color="primary" block @click="deleteDialog = false; this.$emit('update:deleteDialog', false)">NO</v-btn>
          </v-card-actions>
        </v-row>
      </v-card>
    </v-dialog>
</template>

<script>
export default {
  props:{
    deleteDialog: {
      type: Boolean,
      required: true,
    },
    deleteDialogItem: {
      type: Object,
      required: true,
    }
  },
  data() {
    
  },
  computed: {
    dialogValue: {
      get() {
        return this.deleteDialog;
      },
      set(value) {
        this.$emit('update:deleteDialog', value);
      },
    },
  },
  methods: {
    deleteItem() {
      this.$emit('deleteItem', this.deleteDialogItem);
      this.dialogValue = false;
    }
  }
}
</script>