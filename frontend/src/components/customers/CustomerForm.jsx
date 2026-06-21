import { useState } from 'react'

const EMPTY = { full_name: '', email: '', phone: '' }
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export default function CustomerForm({ onSubmit, onCancel }) {
  const [values, setValues] = useState(EMPTY)
  const [errors, setErrors] = useState({})

  const change = (field) => (e) => setValues({ ...values, [field]: e.target.value })

  const validate = () => {
    const next = {}
    if (!values.full_name.trim()) next.full_name = 'Name is required'
    if (!EMAIL_RE.test(values.email)) next.email = 'Valid email required'
    if (!values.phone.trim()) next.phone = 'Phone is required'
    setErrors(next)
    return Object.keys(next).length === 0
  }

  const submit = (e) => {
    e.preventDefault()
    if (!validate()) return
    onSubmit({
      full_name: values.full_name.trim(),
      email: values.email.trim(),
      phone: values.phone.trim(),
    })
  }

  const field = (name, label) => (
    <label className="block">
      <span className="text-sm text-slate-600">{label}</span>
      <input
        value={values[name]}
        onChange={change(name)}
        className="mt-1 w-full rounded border border-slate-300 px-3 py-2"
      />
      {errors[name] && <span className="text-xs text-red-600">{errors[name]}</span>}
    </label>
  )

  return (
    <form onSubmit={submit} className="space-y-3">
      {field('full_name', 'Full name')}
      {field('email', 'Email')}
      {field('phone', 'Phone')}
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
