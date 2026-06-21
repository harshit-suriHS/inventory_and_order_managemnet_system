export default function Pagination({ total, limit, offset, onChange }) {
  const start = total === 0 ? 0 : offset + 1
  const end = Math.min(offset + limit, total)

  return (
    <div className="flex items-center justify-between py-2 text-sm text-slate-600">
      <span>
        Showing {start}–{end} of {total}
      </span>
      <div className="flex gap-2">
        <button
          className="rounded border border-slate-300 px-3 py-1 disabled:opacity-40"
          disabled={offset === 0}
          onClick={() => onChange(Math.max(0, offset - limit))}
        >
          Prev
        </button>
        <button
          className="rounded border border-slate-300 px-3 py-1 disabled:opacity-40"
          disabled={offset + limit >= total}
          onClick={() => onChange(offset + limit)}
        >
          Next
        </button>
      </div>
    </div>
  )
}
