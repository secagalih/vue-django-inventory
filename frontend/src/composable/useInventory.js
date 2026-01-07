import inventoryService from '@/services/inventoryService'

export function useInventory() {
  const fetchItems = async () => {
    const response = await inventoryService.getItems()
    return response.data
  }

  const addItems = async (data) => {
    const response = await inventoryService.createItem(data)
    return response.data
  }

  const updateItem = async ({ data, id }) => {
    const response = await inventoryService.updateItem({ id: id, data: data })
    return response.data

  }

  const deleteItem = async ({ id }) => {
    const response = await inventoryService.deleteItem({ id: id, })
    return response.data

  }

  return { fetchItems, addItems, updateItem, deleteItem }
}