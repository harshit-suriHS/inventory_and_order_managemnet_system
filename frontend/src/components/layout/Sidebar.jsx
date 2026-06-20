import { NavLink } from 'react-router-dom'

const links = [
  { to: '/', label: 'Dashboard', end: true },
  { to: '/products', label: 'Products' },
  { to: '/customers', label: 'Customers' },
  { to: '/orders', label: 'Orders' },
]

export default function Sidebar() {
  return (
    <nav className="flex gap-1 bg-slate-800 p-3 text-slate-100 md:h-screen md:w-56 md:flex-col">
      <h1 className="mb-2 hidden text-lg font-semibold md:block">Inventory</h1>
      {links.map((link) => (
        <NavLink
          key={link.to}
          to={link.to}
          end={link.end}
          className={({ isActive }) =>
            `rounded px-3 py-2 text-sm ${isActive ? 'bg-slate-600' : 'hover:bg-slate-700'}`
          }
        >
          {link.label}
        </NavLink>
      ))}
    </nav>
  )
}
