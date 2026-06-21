import { useCallback, useEffect, useState } from 'react'
import ordersApi from '../api/orders.js'

const PAGE_SIZE = 10

export default function useOrders() {
  const [orders, setOrders] = useState([])
  const [total, setTotal] = useState(0)
  const [offset, setOffset] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const reload = useCallback(async () => {
    setLoading(true)
    try {
      const data = await ordersApi.list({ limit: PAGE_SIZE, offset })
      setOrders(data.items)
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

  return { orders, total, limit: PAGE_SIZE, offset, setOffset, loading, error, reload }
}
