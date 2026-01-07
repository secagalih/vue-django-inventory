<script setup>
import { useInventory } from '@/composable/useInventory'
import { onMounted, ref } from 'vue'


// const items = [
//   {
//     "id": "4a750e2e-3319-47cd-9f4c-60ac5f239beb",
//     "name": "Test Product",
//     "sku": "TEST-001",
//     "price": "19.99",
//     "stock": 12,
//     "created_at": "2026-01-07T04:00:38.100956Z"
//   },
//   {
//     "id": "2e65f775-9a2f-44d6-87a5-3a15845814e9",
//     "name": "Test Product2",
//     "sku": "TEST-002",
//     "price": "29.99",
//     "stock": 10,
//     "created_at": "2026-01-07T04:37:45.928770Z"
//   },
//   {
//     "id": "84d0f166-af6a-49e9-b16e-67a8e697e798",
//     "name": "Macbook Air M5",
//     "sku": "TEST-004",
//     "price": "1299.99",
//     "stock": 10,
//     "created_at": "2026-01-07T06:07:37.387278Z"
//   },
//   {
//     "id": "9ef1aefb-e17d-4532-95ff-e1e7795d5481",
//     "name": "Macbook Air M3",
//     "sku": "TEST-005",
//     "price": "999.99",
//     "stock": 10,
//     "created_at": "2026-01-07T06:07:53.569228Z"
//   }
// ]

const headers = [
  { title: 'Item Name', align: 'start', key: 'name' },
  { title: 'SKU', align: 'start', key: 'sku' },
  { title: 'Price', align: 'start', key: 'price' },
  { title: 'Stock', align: 'start', key: 'stock' },

]

const dialog = ref(false)
const { items ,fetchItems } = useInventory()


onMounted(() => {
  fetchItems()
})
</script>

<template>
  <main>
    <div class="d-flex justify-end my-4">
      <v-btn @click="dialog = true">
        Add Item
      </v-btn>
    </div>
    <v-data-table :items density="compact" :headers></v-data-table>
    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>
          <span class="text-h5">Add New Item</span>
        </v-card-title>

        <v-card-text>
          <v-text-field label="Item Name" />
          <v-text-field label="SKU" />
          <v-text-field label="Price" type="number" />
          <v-text-field label="Stock" type="number" />
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" @click="dialog = false">
            Cancel
          </v-btn>
          <v-btn color="primary" @click="dialog = false">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </main>
</template>
