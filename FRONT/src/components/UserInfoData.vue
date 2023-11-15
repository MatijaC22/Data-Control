<template>
  <v-card
                border
                class="mx-1 mb-2"
                density="compact"
                color="grey-lighten-5"
                >

               <v-timeline class="ma-2" align="start">
                <v-timeline-item
                  v-for="(item, i) in items"
                  :key="i"
                  :dot-color="item.color"
                  :icon="item.icon"
                  fill-dot
                >
                  <v-card>
                    <v-card-title :class="['text-h6', `bg-${item.color}`]">
                      {{ item.title }}
                    </v-card-title>
                    <v-card-text class="bg-white text--primary">
                      <p>Lorem ipsum dolor sit amet, no nam oblique veritus. Commune scaevola imperdiet nec ut, sed euismod convenire principes at. Est et nobis iisque percipit, an vim zril disputando voluptatibus, vix an salutandi sententiae.</p>
                      <v-btn
                        :color="item.color"
                        variant="outlined"
                      >
                        Modify
                      </v-btn>
                    </v-card-text>
                  </v-card>
                </v-timeline-item>
              </v-timeline>
            </v-card>
</template>

<script>
export default {
  data() {
    return{
      items: [
        {
          color: 'red-lighten-2',
          icon: 'mdi-star',
          title: 'Education'
        },
        {
          color: 'purple-lighten-2',
          icon: 'mdi-book-variant',
          title: 'Experience'
        },
        {
          color: 'green-lighten-1',
          icon: 'mdi-airballoon',
          title: 'Family'
        },
        {
          color: 'indigo-lighten-2',
          icon: 'mdi-layers-triple',
          title: 'Notes'
        },
      ],
    }
  },
}
</script>

<style scoped>

</style>