import { useCallback, useEffect, useState } from 'react'
import productsApi from '../api/products.js'

const PAGE_SIZE = 10

export default function useProducts() {
  const [products, setProducts] = useState([])
  const [total, setTotal] = useState(0)
  const [offset, setOffset] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const reload = useCallback(async () => {
    setLoading(true)
    try {
      const data = await productsApi.list({ limit: PAGE_SIZE, offset })
      setProducts(data.items)
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

  return { products, total, limit: PAGE_SIZE, offset, setOffset, loading, error, reload }
}
