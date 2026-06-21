export default function DataTable({ columns, rows, empty = 'No records.' }) {
  if (!rows.length) return <p className="text-slate-500">{empty}</p>
  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white">
      <table className="min-w-full text-sm">
        <thead className="bg-slate-100 text-left">
          <tr>
            {columns.map((col) => (
              <th key={col.key} className="px-4 py-2 font-medium">{col.header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id} className="border-t border-slate-100">
              {columns.map((col) => (
                <td key={col.key} className="px-4 py-2">
                  {col.render ? col.render(row) : row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
