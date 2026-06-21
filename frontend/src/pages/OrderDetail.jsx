import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import ordersApi from '../api/orders.js'
import DataTable from '../components/common/DataTable.jsx'
import Spinner from '../components/common/Spinner.jsx'
import StatusBadge from '../components/common/StatusBadge.jsx'
import Toast from '../components/common/Toast.jsx'

export default function OrderDetail() {
  const { id } = useParams()
  const [order, setOrder] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [toast, setToast] = useState(null)

  useEffect(() => {
    ordersApi
      .get(id)
      .then(setOrder)
      .catch(setError)
      .finally(() => setLoading(false))
  }, [id])

  const cancel = async () => {
    if (!window.confirm(`Cancel order #${order.id}? Stock will be restored.`)) return
    try {
      await ordersApi.remove(order.id)
      setOrder(await ordersApi.get(order.id))
      setToast({ message: 'Order cancelled', type: 'success' })
    } catch (err) {
      setToast({ message: err.response?.data?.detail || 'Cancel failed', type: 'error' })
    }
  }

  if (loading) return <Spinner />
  if (error || !order) return <p className="text-red-600">Order not found.</p>

  const columns = [
    { key: 'product', header: 'Product', render: (row) => row.product.name },
    { key: 'sku', header: 'SKU', render: (row) => row.product.sku },
    { key: 'quantity', header: 'Qty' },
    { key: 'unit_price', header: 'Unit price' },
  ]

  return (
    <div className="space-y-4">
      <Link to="/orders" className="text-sm text-slate-600 hover:text-slate-900">
        ← Back to orders
      </Link>
      <div className="flex items-center justify-between">
        <h2 className="flex items-center gap-2 text-xl font-semibold">
          Order #{order.id}
          <StatusBadge status={order.status} />
        </h2>
        {order.status === 'active' && (
          <button className="rounded bg-red-600 px-4 py-2 text-white" onClick={cancel}>
            Cancel order
          </button>
        )}
      </div>
      <p className="text-slate-600">Customer: {order.customer.full_name}</p>
      <DataTable columns={columns} rows={order.items} empty="No items." />
      <p className="text-right font-medium">Total: {order.total_amount}</p>
      <Toast {...(toast || {})} onClose={() => setToast(null)} />
    </div>
  )
}
