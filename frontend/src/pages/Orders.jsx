import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import customersApi from '../api/customers.js'
import ordersApi from '../api/orders.js'
import productsApi from '../api/products.js'
import DataTable from '../components/common/DataTable.jsx'
import Modal from '../components/common/Modal.jsx'
import Pagination from '../components/common/Pagination.jsx'
import Spinner from '../components/common/Spinner.jsx'
import StatusBadge from '../components/common/StatusBadge.jsx'
import Toast from '../components/common/Toast.jsx'
import OrderForm from '../components/orders/OrderForm.jsx'
import useOrders from '../hooks/useOrders.js'

export default function Orders() {
  const { orders, total, limit, offset, setOffset, loading, error, reload } = useOrders()
  const [open, setOpen] = useState(false)
  const [toast, setToast] = useState(null)
  const [formProducts, setFormProducts] = useState([])
  const [formCustomers, setFormCustomers] = useState([])
  const navigate = useNavigate()

  const notify = (message, type = 'success') => setToast({ message, type })

  const loadFormOptions = async () => {
    const [pd, cd] = await Promise.all([
      productsApi.list({ limit: 100, offset: 0 }),
      customersApi.list({ limit: 100, offset: 0 }),
    ])
    // Only active customers/products can be used on a new order.
    setFormProducts(pd.items.filter((p) => p.status === 'active'))
    setFormCustomers(cd.items.filter((c) => c.status === 'active'))
  }

  useEffect(() => {
    loadFormOptions()
  }, [])

  const save = async (data) => {
    try {
      await ordersApi.create(data)
      setOpen(false)
      await Promise.all([reload(), loadFormOptions()])
      notify('Order created')
    } catch (err) {
      notify(err.response?.data?.detail || 'Order failed', 'error')
    }
  }

  const cancel = async (order) => {
    if (!window.confirm(`Cancel order #${order.id}? Stock will be restored.`)) return
    try {
      await ordersApi.remove(order.id)
      await Promise.all([reload(), loadFormOptions()])
      notify('Order cancelled')
    } catch (err) {
      notify(err.response?.data?.detail || 'Cancel failed', 'error')
    }
  }

  const columns = [
    { key: 'id', header: 'Order #' },
    { key: 'customer', header: 'Customer', render: (row) => row.customer.full_name },
    { key: 'total_amount', header: 'Total' },
    { key: 'status', header: 'Status', render: (row) => <StatusBadge status={row.status} /> },
    {
      key: 'actions',
      header: '',
      render: (row) => (
        <div className="flex gap-3">
          <button className="text-slate-600" onClick={() => navigate(`/orders/${row.id}`)}>
            View
          </button>
          {row.status === 'active' && (
            <button className="text-red-600" onClick={() => cancel(row)}>Cancel</button>
          )}
        </div>
      ),
    },
  ]

  if (loading) return <Spinner />
  if (error) return <p className="text-red-600">Failed to load orders.</p>

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Orders</h2>
        <button className="rounded bg-slate-800 px-4 py-2 text-white" onClick={() => setOpen(true)}>
          Create order
        </button>
      </div>
      <DataTable columns={columns} rows={orders} empty="No orders yet." />
      <Pagination total={total} limit={limit} offset={offset} onChange={setOffset} />
      <Modal open={open} title="Create order" onClose={() => setOpen(false)}>
        <OrderForm
          customers={formCustomers}
          products={formProducts}
          onSubmit={save}
          onCancel={() => setOpen(false)}
        />
      </Modal>
      <Toast {...(toast || {})} onClose={() => setToast(null)} />
    </div>
  )
}
