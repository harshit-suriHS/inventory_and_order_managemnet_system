import { Route, Routes } from 'react-router-dom'
import Layout from './components/layout/Layout.jsx'
import Customers from './pages/Customers.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Products from './pages/Products.jsx'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/products" element={<Products />} />
        <Route path="/customers" element={<Customers />} />
      </Routes>
    </Layout>
  )
}
