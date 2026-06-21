import { useState } from 'react'
import productsApi from '../api/products.js'
import DataTable from '../components/common/DataTable.jsx'
import Modal from '../components/common/Modal.jsx'
import Spinner from '../components/common/Spinner.jsx'
import Toast from '../components/common/Toast.jsx'
import ProductForm from '../components/products/ProductForm.jsx'
import useProducts from '../hooks/useProducts.js'

export default function Products() {
  const { products, loading, error, reload } = useProducts()
  const [editing, setEditing] = useState(null)
  const [open, setOpen] = useState(false)
  const [toast, setToast] = useState(null)

  const notify = (message, type = 'success') => setToast({ message, type })

  const save = async (data) => {
    try {
      if (editing) await productsApi.update(editing.id, data)
      else await productsApi.create(data)
      setOpen(false)
      setEditing(null)
      await reload()
      notify('Product saved')
    } catch (err) {
      notify(err.response?.data?.detail || 'Save failed', 'error')
    }
  }

  const remove = async (product) => {
    if (!window.confirm(`Delete ${product.name}?`)) return
    try {
      await productsApi.remove(product.id)
      await reload()
      notify('Product deleted')
    } catch {
      notify('Delete failed', 'error')
    }
  }

  const columns = [
    { key: 'name', header: 'Name' },
    { key: 'sku', header: 'SKU' },
    { key: 'price', header: 'Price' },
    { key: 'quantity', header: 'Stock' },
    {
      key: 'actions',
      header: '',
      render: (row) => (
        <div className="flex gap-2">
          <button className="text-slate-600" onClick={() => { setEditing(row); setOpen(true) }}>
            Edit
          </button>
          <button className="text-red-600" onClick={() => remove(row)}>Delete</button>
        </div>
      ),
    },
  ]

  if (loading) return <Spinner />
  if (error) return <p className="text-red-600">Failed to load products.</p>

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Products</h2>
        <button
          className="rounded bg-slate-800 px-4 py-2 text-white"
          onClick={() => { setEditing(null); setOpen(true) }}
        >
          Add product
        </button>
      </div>
      <DataTable columns={columns} rows={products} empty="No products yet." />
      <Modal open={open} title={editing ? 'Edit product' : 'Add product'} onClose={() => setOpen(false)}>
        <ProductForm
          initial={editing && { ...editing, price: String(editing.price), quantity: String(editing.quantity) }}
          onSubmit={save}
          onCancel={() => setOpen(false)}
        />
      </Modal>
      <Toast {...(toast || {})} onClose={() => setToast(null)} />
    </div>
  )
}
