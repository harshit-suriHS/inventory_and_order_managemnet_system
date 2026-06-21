import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import ordersApi from '../api/orders.js'
import DataTable from '../components/common/DataTable.jsx'
import Modal from '../components/common/Modal.jsx'
import Spinner from '../components/common/Spinner.jsx'
import Toast from '../components/common/Toast.jsx'
import OrderForm from '../components/orders/OrderForm.jsx'
import useCustomers from '../hooks/useCustomers.js'
import useOrders from '../hooks/useOrders.js'
import useProducts from '../hooks/useProducts.js'

export default function Orders() {
  const { orders, loading, error, reload } = useOrders()
  const { customers } = useCustomers()
  const { products, reload: reloadProducts } = useProducts()
  const [open, setOpen] = useState(false)
  const [toast, setToast] = useState(null)
  const navigate = useNavigate()

  const notify = (message, type = 'success') => setToast({ message, type })

  const save = async (data) => {
    try {
      await ordersApi.create(data)
      setOpen(false)
      await Promise.all([reload(), reloadProducts()])
      notify('Order created')
    } catch (err) {
      notify(err.response?.data?.detail || 'Order failed', 'error')
    }
  }

  const columns = [
    { key: 'id', header: 'Order #' },
    { key: 'customer_id', header: 'Customer' },
    { key: 'total_amount', header: 'Total' },
    {
      key: 'actions',
      header: '',
      render: (row) => (
        <button className="text-slate-600" onClick={() => navigate(`/orders/${row.id}`)}>
          View
        </button>
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
      <Modal open={open} title="Create order" onClose={() => setOpen(false)}>
        <OrderForm
          customers={customers}
          products={products}
          onSubmit={save}
          onCancel={() => setOpen(false)}
        />
      </Modal>
      <Toast {...(toast || {})} onClose={() => setToast(null)} />
    </div>
  )
}
