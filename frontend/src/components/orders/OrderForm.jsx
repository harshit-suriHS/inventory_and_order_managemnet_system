import { useMemo, useState } from 'react'

export default function OrderForm({ customers, products, onSubmit, onCancel }) {
  const [customerId, setCustomerId] = useState('')
  const [lines, setLines] = useState([{ product_id: '', quantity: '1' }])
  const [error, setError] = useState('')

  const productById = useMemo(
    () => Object.fromEntries(products.map((p) => [String(p.id), p])),
    [products],
  )

  const total = useMemo(
    () =>
      lines.reduce((sum, line) => {
        const product = productById[line.product_id]
        const qty = Number(line.quantity) || 0
        return sum + (product ? Number(product.price) * qty : 0)
      }, 0),
    [lines, productById],
  )

  const updateLine = (index, field, value) => {
    const next = lines.slice()
    next[index] = { ...next[index], [field]: value }
    setLines(next)
  }

  const addLine = () => setLines([...lines, { product_id: '', quantity: '1' }])
  const removeLine = (index) => setLines(lines.filter((_, i) => i !== index))

  const submit = (e) => {
    e.preventDefault()
    if (!customerId) return setError('Select a customer')
    const items = lines
      .filter((l) => l.product_id && Number(l.quantity) > 0)
      .map((l) => ({ product_id: Number(l.product_id), quantity: Number(l.quantity) }))
    if (!items.length) return setError('Add at least one product')
    setError('')
    onSubmit({ customer_id: Number(customerId), items })
  }

  return (
    <form onSubmit={submit} className="space-y-3">
      <label className="block">
        <span className="text-sm text-slate-600">Customer</span>
        <select
          value={customerId}
          onChange={(e) => setCustomerId(e.target.value)}
          className="mt-1 w-full rounded border border-slate-300 px-3 py-2"
        >
          <option value="">Select…</option>
          {customers.map((c) => (
            <option key={c.id} value={c.id}>{c.full_name}</option>
          ))}
        </select>
      </label>

      <div className="space-y-2">
        {lines.map((line, index) => (
          <div key={index} className="flex gap-2">
            <select
              value={line.product_id}
              onChange={(e) => updateLine(index, 'product_id', e.target.value)}
              className="flex-1 rounded border border-slate-300 px-2 py-2"
            >
              <option value="">Product…</option>
              {products.map((p) => (
                <option key={p.id} value={p.id}>{p.name} (stock {p.quantity})</option>
              ))}
            </select>
            <input
              type="number"
              min="1"
              value={line.quantity}
              onChange={(e) => updateLine(index, 'quantity', e.target.value)}
              className="w-20 rounded border border-slate-300 px-2 py-2"
            />
            {lines.length > 1 && (
              <button type="button" className="text-red-600" onClick={() => removeLine(index)}>×</button>
            )}
          </div>
        ))}
        <button type="button" className="text-sm text-slate-600" onClick={addLine}>
          + Add line
        </button>
      </div>

      <p className="text-right font-medium">Total: {total.toFixed(2)}</p>
      {error && <p className="text-sm text-red-600">{error}</p>}

      <div className="flex justify-end gap-2 pt-2">
        <button type="button" onClick={onCancel} className="rounded px-4 py-2 text-slate-600">
          Cancel
        </button>
        <button type="submit" className="rounded bg-slate-800 px-4 py-2 text-white">
          Create order
        </button>
      </div>
    </form>
  )
}
