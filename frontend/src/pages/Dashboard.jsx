import DataTable from '../components/common/DataTable.jsx'
import Spinner from '../components/common/Spinner.jsx'
import useDashboard from '../hooks/useDashboard.js'

function StatCard({ label, value }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4">
      <p className="text-sm text-slate-500">{label}</p>
      <p className="text-2xl font-semibold">{value}</p>
    </div>
  )
}

export default function Dashboard() {
  const { data, loading, error } = useDashboard()

  if (loading) return <Spinner />
  if (error || !data) return <p className="text-red-600">Failed to load dashboard.</p>

  const columns = [
    { key: 'name', header: 'Product' },
    { key: 'sku', header: 'SKU' },
    { key: 'quantity', header: 'Stock' },
  ]

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Dashboard</h2>
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard label="Products" value={data.total_products} />
        <StatCard label="Customers" value={data.total_customers} />
        <StatCard label="Orders" value={data.total_orders} />
        <StatCard label="Low stock" value={data.low_stock_products.length} />
      </div>
      <div className="space-y-2">
        <h3 className="font-medium">Low stock products</h3>
        <DataTable columns={columns} rows={data.low_stock_products} empty="All products well stocked." />
      </div>
    </div>
  )
}
