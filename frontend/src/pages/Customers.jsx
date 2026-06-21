import { useState } from 'react'
import customersApi from '../api/customers.js'
import DataTable from '../components/common/DataTable.jsx'
import Modal from '../components/common/Modal.jsx'
import Pagination from '../components/common/Pagination.jsx'
import Spinner from '../components/common/Spinner.jsx'
import StatusBadge from '../components/common/StatusBadge.jsx'
import Toast from '../components/common/Toast.jsx'
import CustomerForm from '../components/customers/CustomerForm.jsx'
import useCustomers from '../hooks/useCustomers.js'

export default function Customers() {
  const { customers, total, limit, offset, setOffset, loading, error, reload } = useCustomers()
  const [open, setOpen] = useState(false)
  const [toast, setToast] = useState(null)

  const notify = (message, type = 'success') => setToast({ message, type })

  const save = async (data) => {
    try {
      await customersApi.create(data)
      setOpen(false)
      await reload()
      notify('Customer saved')
    } catch (err) {
      notify(err.response?.data?.detail || 'Save failed', 'error')
    }
  }

  const archive = async (customer) => {
    if (!window.confirm(`Archive ${customer.full_name}?`)) return
    try {
      await customersApi.remove(customer.id)
      await reload()
      notify('Customer archived')
    } catch (err) {
      notify(err.response?.data?.detail || 'Archive failed', 'error')
    }
  }

  const restore = async (customer) => {
    try {
      await customersApi.update(customer.id, {
        full_name: customer.full_name,
        email: customer.email,
        phone: customer.phone,
        status: 'active',
      })
      await reload()
      notify('Customer restored')
    } catch (err) {
      notify(err.response?.data?.detail || 'Restore failed', 'error')
    }
  }

  const columns = [
    { key: 'full_name', header: 'Name' },
    { key: 'email', header: 'Email' },
    { key: 'phone', header: 'Phone' },
    { key: 'status', header: 'Status', render: (row) => <StatusBadge status={row.status} /> },
    {
      key: 'actions',
      header: '',
      render: (row) =>
        row.status === 'archived' ? (
          <button className="text-emerald-600" onClick={() => restore(row)}>Restore</button>
        ) : (
          <button className="text-red-600" onClick={() => archive(row)}>Archive</button>
        ),
    },
  ]

  if (loading) return <Spinner />
  if (error) return <p className="text-red-600">Failed to load customers.</p>

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Customers</h2>
        <button className="rounded bg-slate-800 px-4 py-2 text-white" onClick={() => setOpen(true)}>
          Add customer
        </button>
      </div>
      <DataTable columns={columns} rows={customers} empty="No customers yet." />
      <Pagination total={total} limit={limit} offset={offset} onChange={setOffset} />
      <Modal open={open} title="Add customer" onClose={() => setOpen(false)}>
        <CustomerForm onSubmit={save} onCancel={() => setOpen(false)} />
      </Modal>
      <Toast {...(toast || {})} onClose={() => setToast(null)} />
    </div>
  )
}
