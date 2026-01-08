<script setup>
import { useInventory } from '@/composable/useInventory'
import { onMounted, ref } from 'vue'


const headers = [
  { title: 'Item Name', align: 'start', key: 'name' },
  { title: 'SKU', align: 'start', key: 'sku' },
  { title: 'Price', align: 'start', key: 'price' },
  { title: 'Stock', align: 'start', key: 'stock' },
  { title: 'Action', key: 'action' }

]

const dialog = ref(false)
const { fetchItems, addItems, deleteItem, updateItem } = useInventory()
const items = ref([])
const loading = ref(false)
const isEdit = ref(false)
const formData = ref({
  id: null,
  name: '',
  sku: '',
  price: 0,
  stock: 0,
})

const handleEdit = (item) => {
  dialog.value = true
  isEdit.value = true
  formData.value = {
    id: item.id,
    name: item.name,
    sku: item.sku,
    price: item.price,
    stock: item.stock,
  }
}

const handleAdd = () => {
  dialog.value = true
  isEdit.value = false
  formData.value = {
    id: null,
    name: '',
    sku: '',
    price: 0,
    stock: 0,
  }
}

const handleSave = async () => {
  try {
    loading.value = true
    if (isEdit.value) {
      await updateItem({
        id: formData.value.id,
        data: {
          name: formData.value.name,
          sku: formData.value.sku,
          price: formData.value.price,
          stock: formData.value.stock
        }
      })
    } else {
      await addItems({
        name: formData.value.name,
        sku: formData.value.sku,
        price: formData.value.price,
        stock: formData.value.stock
      })
    }

  } catch (error) {
    console.error('Failed to save item:', error)
    alert('Failed to save item. Please try again.')
  } finally {

    items.value = await fetchItems()
    loading.value = false
    dialog.value = false
  }

}


const handleDelete = async (item) => {
  if (!confirm(`Are you sure you want to delete "${item.name}"?`)) {
    return
  }
  try {
    loading.value = true
    await deleteItem({ id: item.id })
    items.value = await fetchItems()
  } catch (error) {
    alert('Failed to delete item:', error)
  } finally {
    loading.value = false
  }
}


onMounted(async () => {
  loading.value = true
  items.value = await fetchItems()
  loading.value = false
})
</script>

<template>
  <div v-if="loading" class="text-center my-4">
    <v-progress-circular color="primary" indeterminate></v-progress-circular>
  </div>
  <main v-else>
    <div class="d-flex justify-end my-4">
      <v-btn @click="handleAdd()">
        Add Item
      </v-btn>
    </div>

    <v-data-table :items="items" density="compact" :headers>
      <template v-slot:item.action="{ item }">
        <v-row>
          <v-btn @click="handleEdit(item)">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn @click="handleDelete(item)">
            <v-icon>mdi-trash-can</v-icon>
          </v-btn>
        </v-row>
      </template>
    </v-data-table>
    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>
          <span class="text-h5">Add New Item</span>
        </v-card-title>

        <v-card-text>
          <v-text-field label="Item Name" v-model="formData.name" />
          <v-text-field label="SKU" v-model="formData.sku" />
          <v-text-field label="Price" type="number" v-model="formData.price" />
          <v-text-field label="Stock" type="number" v-model="formData.stock" />
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" @click="dialog = false">
            Cancel
          </v-btn>
          <v-btn color="primary" @click="handleSave()">
            {{ isEdit ? "Update" : 'Save' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </main>
</template>
