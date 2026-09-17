import { BarChart3, ChevronRight, FileClock, LayoutDashboard, LogOut, Menu, Settings, ShieldCheck, Sparkles, UserRound, X } from 'lucide-react'
import { useState } from 'react'
import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom'
import { Logo } from '../components/Logo'
import { ThemeToggle } from '../components/ThemeToggle'
import { useAuth } from '../context/AuthContext'

const baseNav = [
  { to: '/app', label: 'Overview', icon: LayoutDashboard, end: true },
  { to: '/app/analyze', label: 'New analysis', icon: Sparkles },
  { to: '/app/history', label: 'Resume history', icon: FileClock },
  { to: '/app/insights', label: 'Career insights', icon: BarChart3 },
  { to: '/app/profile', label: 'Profile & plan', icon: UserRound },
]

export function DashboardLayout() {
  const [open, setOpen] = useState(false)
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const nav = user?.is_admin ? [...baseNav, { to: '/app/admin', label: 'Admin console', icon: ShieldCheck, end: false }] : baseNav
  const current = nav.find((item) => item.end ? location.pathname === item.to : location.pathname.startsWith(item.to))
  const signOut = () => { logout(); navigate('/') }

  return (
    <div className="app-shell">
      {open && <button aria-label="Close menu" className="fixed inset-0 z-40 bg-slate-950/40 backdrop-blur-sm lg:hidden" onClick={() => setOpen(false)} />}
      <aside className={`fixed inset-y-0 left-0 z-50 flex w-[280px] flex-col border-r border-slate-200 bg-white/95 p-5 backdrop-blur-xl transition-transform dark:border-white/10 dark:bg-[#0b0f19]/95 lg:translate-x-0 ${open ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="flex items-center justify-between"><Logo /><button className="grid h-10 w-10 place-items-center rounded-xl lg:hidden" onClick={() => setOpen(false)} aria-label="Close navigation"><X size={20} /></button></div>
        <nav className="mt-9 space-y-1.5" aria-label="Dashboard navigation">
          {nav.map(({ to, label, icon: Icon, end }) => <NavLink key={to} to={to} end={end} onClick={() => setOpen(false)} className={({ isActive }) => `group flex items-center gap-3 rounded-2xl px-3.5 py-3 text-sm font-semibold transition ${isActive ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-950 dark:text-slate-300 dark:hover:bg-white/[0.06] dark:hover:text-white'}`}><Icon size={18} /><span>{label}</span><ChevronRight size={15} className="ml-auto opacity-0 transition group-hover:opacity-70" /></NavLink>)}
        </nav>
        <div className="mt-auto">
          <div className="mb-4 rounded-2xl bg-gradient-to-br from-blue-600 to-violet-700 p-4 text-white shadow-glow"><p className="text-xs font-bold uppercase tracking-[.15em] text-blue-100">Current plan</p><p className="mt-1 font-display text-xl font-bold capitalize">{user?.plan}</p><p className="mt-1 text-xs leading-5 text-blue-100">Free includes three analyses each month.</p></div>
          <button onClick={signOut} className="flex w-full items-center gap-3 rounded-2xl px-3.5 py-3 text-sm font-semibold text-slate-500 transition hover:bg-rose-50 hover:text-rose-600 dark:hover:bg-rose-500/10"><LogOut size={18} /> Sign out</button>
        </div>
      </aside>
      <div className="lg:pl-[280px]">
        <header className="sticky top-0 z-30 border-b border-slate-200/80 bg-slate-50/85 backdrop-blur-xl dark:border-white/10 dark:bg-[#080b13]/85">
          <div className="flex h-20 items-center gap-4 px-4 sm:px-6 lg:px-8">
            <button onClick={() => setOpen(true)} className="grid h-10 w-10 place-items-center rounded-xl border border-slate-200 bg-white lg:hidden dark:border-white/10 dark:bg-white/[0.04]" aria-label="Open navigation"><Menu size={20} /></button>
            <div><p className="text-xs font-semibold uppercase tracking-[.13em] text-slate-400">Workspace</p><h1 className="font-display text-lg font-bold">{current?.label || 'Analysis results'}</h1></div>
            <div className="ml-auto flex items-center gap-3"><ThemeToggle /><button className="hidden h-10 items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 text-sm font-semibold text-slate-600 sm:flex dark:border-white/10 dark:bg-white/[0.04] dark:text-slate-300"><Settings size={17} /> Settings</button><div className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-blue-100 to-violet-100 text-sm font-bold text-blue-700 dark:from-blue-500/20 dark:to-violet-500/20 dark:text-blue-300">{user?.name?.slice(0, 1).toUpperCase()}</div></div>
          </div>
        </header>
        <main className="px-4 py-6 sm:px-6 sm:py-8 lg:px-8"><Outlet /></main>
      </div>
    </div>
  )
}
