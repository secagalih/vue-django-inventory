import inventoryService from '@/services/inventoryService'
import { ref } from 'vue'


export function useInventory() {
  const items = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchItems = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await inventoryService.getItems()
      items.value = response.data
    } catch (err) {
      error.value = err.message || 'Failed to fetch item'
      console.error('Error fetching items:', err)
    } finally {
      loading.value = false
    }
  }


  return {
    fetchItems,
    items
  }
}