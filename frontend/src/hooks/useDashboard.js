import { useEffect, useState } from 'react'
import dashboardApi from '../api/dashboard.js'

export default function useDashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    dashboardApi
      .get()
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false))
  }, [])

  return { data, loading, error }
}
