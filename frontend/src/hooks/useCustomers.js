import { useCallback, useEffect, useState } from 'react'
import customersApi from '../api/customers.js'

const PAGE_SIZE = 10

export default function useCustomers() {
  const [customers, setCustomers] = useState([])
  const [total, setTotal] = useState(0)
  const [offset, setOffset] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const reload = useCallback(async () => {
    setLoading(true)
    try {
      const data = await customersApi.list({ limit: PAGE_SIZE, offset })
      setCustomers(data.items)
      setTotal(data.total)
      setError(null)
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
  }, [offset])

  useEffect(() => {
    reload()
  }, [reload])

  return { customers, total, limit: PAGE_SIZE, offset, setOffset, loading, error, reload }
}
