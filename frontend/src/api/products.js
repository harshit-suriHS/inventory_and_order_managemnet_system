import api from './client.js'

const productsApi = {
  list: (params) => api.get('/products', { params }).then((r) => r.data),
  create: (data) => api.post('/products', data).then((r) => r.data),
  update: (id, data) => api.put(`/products/${id}`, data).then((r) => r.data),
  remove: (id) => api.delete(`/products/${id}`),
}

export default productsApi
