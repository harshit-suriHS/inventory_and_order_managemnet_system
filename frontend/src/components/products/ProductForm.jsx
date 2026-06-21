import { useState } from 'react'

const EMPTY = { name: '', sku: '', price: '', quantity: '' }

export default function ProductForm({ initial, onSubmit, onCancel }) {
  const [values, setValues] = useState(initial || EMPTY)
  const [errors, setErrors] = useState({})

  const change = (field) => (e) => setValues({ ...values, [field]: e.target.value })

  const validate = () => {
    const next = {}
    if (!values.name.trim()) next.name = 'Name is required'
    if (!values.sku.trim()) next.sku = 'SKU is required'
    if (values.price === '' || Number(values.price) < 0) next.price = 'Price must be ≥ 0'
    if (values.quantity === '' || Number(values.quantity) < 0)
      next.quantity = 'Quantity must be ≥ 0'
    setErrors(next)
    return Object.keys(next).length === 0
  }

  const submit = (e) => {
    e.preventDefault()
    if (!validate()) return
    onSubmit({
      name: values.name.trim(),
      sku: values.sku.trim(),
      price: Number(values.price),
      quantity: Number(values.quantity),
    })
  }

  const field = (name, label, type = 'text') => (
    <label className="block">
      <span className="text-sm text-slate-600">{label}</span>
      <input
        type={type}
        value={values[name]}
        onChange={change(name)}
        className="mt-1 w-full rounded border border-slate-300 px-3 py-2"
      />
      {errors[name] && <span className="text-xs text-red-600">{errors[name]}</span>}
    </label>
  )

  return (
    <form onSubmit={submit} className="space-y-3">
      {field('name', 'Name')}
      {field('sku', 'SKU')}
      {field('price', 'Price', 'number')}
      {field('quantity', 'Quantity', 'number')}
      <div className="flex justify-end gap-2 pt-2">
        <button type="button" onClick={onCancel} className="rounded px-4 py-2 text-slate-600">
          Cancel
        </button>
        <button type="submit" className="rounded bg-slate-800 px-4 py-2 text-white">
          Save
        </button>
      </div>
    </form>
  )
}
