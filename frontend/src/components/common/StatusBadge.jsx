const STYLES = {
  active: 'bg-emerald-100 text-emerald-700',
  archived: 'bg-slate-200 text-slate-600',
  cancelled: 'bg-red-100 text-red-700',
}

export default function StatusBadge({ status }) {
  const className = STYLES[status] || 'bg-slate-200 text-slate-600'
  return (
    <span className={`rounded-full px-2 py-0.5 text-xs font-medium capitalize ${className}`}>
      {status}
    </span>
  )
}
