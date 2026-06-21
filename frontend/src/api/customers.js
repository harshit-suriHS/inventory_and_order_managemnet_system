import api from './client.js'

const customersApi = {
  list: (params) => api.get('/customers', { params }).then((r) => r.data),
  create: (data) => api.post('/customers', data).then((r) => r.data),
  update: (id, data) => api.put(`/customers/${id}`, data).then((r) => r.data),
  remove: (id) => api.delete(`/customers/${id}`),
}

export default customersApi
