import apiClient  from "./api";

export default {

  getItems(){
    return apiClient.get('/products/')
  }

}