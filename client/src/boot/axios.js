import Vue from 'vue'
import axios from 'axios'

export const apiEndpoint = 'https://ns3017873.ip-149-202-86.eu'

const apiClient = axios.create({
  baseURL: `${apiEndpoint}/api/`
})

Vue.prototype.$axios = apiClient

export default apiClient
