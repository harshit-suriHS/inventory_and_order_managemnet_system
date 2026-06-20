export default function Toast({ message, type = 'success', onClose }) {
  if (!message) return null
  const color = type === 'error' ? 'bg-red-600' : 'bg-emerald-600'
  return (
    <div className={`fixed bottom-4 right-4 rounded px-4 py-2 text-white shadow ${color}`}>
      <span>{message}</span>
      <button className="ml-3 font-bold" onClick={onClose}>×</button>
    </div>
  )
}
