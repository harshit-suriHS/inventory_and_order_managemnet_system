import api from './client.js'

const dashboardApi = {
  get: () => api.get('/dashboard').then((r) => r.data),
}

export default dashboardApi
