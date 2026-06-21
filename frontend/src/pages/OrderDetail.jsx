import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import ordersApi from '../api/orders.js'
import DataTable from '../components/common/DataTable.jsx'
import Spinner from '../components/common/Spinner.jsx'

export default function OrderDetail() {
  const { id } = useParams()
  const [order, setOrder] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    ordersApi
      .get(id)
      .then(setOrder)
      .catch(setError)
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <Spinner />
  if (error || !order) return <p className="text-red-600">Order not found.</p>

  const columns = [
    { key: 'product_id', header: 'Product' },
    { key: 'quantity', header: 'Qty' },
    { key: 'unit_price', header: 'Unit price' },
  ]

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Order #{order.id}</h2>
      <p className="text-slate-600">Customer: {order.customer_id}</p>
      <DataTable columns={columns} rows={order.items} empty="No items." />
      <p className="text-right font-medium">Total: {order.total_amount}</p>
    </div>
  )
}
