import apiClient from "./api";

export default {

  getItems() {
    return apiClient.get('/products/')
  },

  createItem(data) {
    return apiClient.post('/products/create/', data)
  },

  updateItem({id, data}) {
    return apiClient.post(`/products/update/${id}`, data)
  },

  deleteItem({id}) {
    return apiClient.post(`/products/delete/${id}`)
  }

}