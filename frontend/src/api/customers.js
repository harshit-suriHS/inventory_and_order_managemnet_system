import api from './client.js'

const customersApi = {
  list: () => api.get('/customers').then((r) => r.data),
  create: (data) => api.post('/customers', data).then((r) => r.data),
  remove: (id) => api.delete(`/customers/${id}`),
}

export default customersApi
