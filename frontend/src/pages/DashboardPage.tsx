import { ArrowRight, BarChart3, FileCheck2, Gauge, Sparkles, Target } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { EmptyState } from '../components/EmptyState'
import { LoadingScreen } from '../components/LoadingScreen'
import { useAuth } from '../context/AuthContext'
import { api } from '../services/api'
import type { DashboardData } from '../types'

export function DashboardPage() {
  const { user } = useAuth()
  const [data, setData] = useState<DashboardData | null>(null)
  const [error, setError] = useState('')
  useEffect(() => { api.dashboard().then(setData).catch((e) => setError(e.message)) }, [])
  if (!data && !error) return <LoadingScreen />
  if (error) return <div className="card text-rose-600">{error}</div>
  const chart = [...(data?.recent || [])].reverse().map((item, index) => ({ name: `#${index + 1}`, score: item.ats_score }))
  const stats = [
    { label: 'Total analyses', value: data?.total_analyses || 0, icon: FileCheck2, note: 'Across your workspace' },
    { label: 'Average ATS', value: `${data?.average_ats || 0}/100`, icon: Gauge, note: 'Recent resume health' },
    { label: 'Top direction', value: data?.top_category || 'Not analyzed', icon: Target, note: 'Most frequent classification' },
  ]
  return <div className="mx-auto max-w-7xl"><section className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end"><div><p className="text-sm font-bold text-blue-600">Good to see you, {user?.name.split(' ')[0]}.</p><h2 className="mt-2 font-display text-3xl font-extrabold tracking-tight sm:text-4xl">Your career intelligence workspace</h2><p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">Track resume quality, compare role alignment, and turn each analysis into a focused improvement plan.</p></div></section>
    <section className="mt-8 grid gap-5 md:grid-cols-3">{stats.map(({ label, value, icon: Icon, note }) => <div key={label} className="card"><div className="flex items-start justify-between gap-3"><div><p className="text-sm font-medium text-slate-500">{label}</p><p className={`mt-2 font-display font-extrabold ${label === 'Top direction' ? 'text-xl' : 'text-3xl'}`}>{value}</p><p className="mt-2 text-xs text-slate-400">{note}</p></div><span className="grid h-11 w-11 place-items-center rounded-2xl bg-blue-50 text-blue-600 dark:bg-blue-500/10 dark:text-blue-300"><Icon size={20} /></span></div></div>)}</section>
    {data?.recent.length ? <section className="mt-6 grid gap-6 lg:grid-cols-[1.1fr_.9fr]"><div className="card"><div className="flex items-center justify-between"><div><h3 className="font-display text-xl font-bold">ATS trend</h3><p className="mt-1 text-xs text-slate-400">Your most recent analyses</p></div><BarChart3 className="text-blue-500" size={20} /></div><div className="mt-6 h-64"><ResponsiveContainer width="100%" height="100%"><AreaChart data={chart}><defs><linearGradient id="atsArea" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#2563eb" stopOpacity={0.35}/><stop offset="95%" stopColor="#2563eb" stopOpacity={0}/></linearGradient></defs><XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} /><YAxis domain={[0, 100]} axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} /><Tooltip contentStyle={{ borderRadius: 16, border: '1px solid #e2e8f0' }} /><Area type="monotone" dataKey="score" stroke="#2563eb" strokeWidth={3} fill="url(#atsArea)" /></AreaChart></ResponsiveContainer></div></div><div className="card"><div className="flex items-center justify-between"><div><h3 className="font-display text-xl font-bold">Recent reports</h3><p className="mt-1 text-xs text-slate-400">Continue where you left off</p></div><Link to="/app/history" className="text-xs font-bold text-blue-600">View all</Link></div><div className="mt-5 space-y-3">{data.recent.map((item) => <Link key={item.id} to={`/app/results/${item.id}`} className="group flex items-center gap-3 rounded-2xl border border-slate-200 p-3 transition hover:border-blue-200 hover:bg-blue-50/50 dark:border-white/10 dark:hover:border-blue-500/30 dark:hover:bg-blue-500/5"><span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-slate-100 text-slate-500 dark:bg-white/[.06]"><FileCheck2 size={18} /></span><div className="min-w-0 flex-1"><p className="truncate text-sm font-bold">{item.filename}</p><p className="truncate text-xs text-slate-400">{item.category}</p></div><span className="text-sm font-extrabold text-blue-600">{item.ats_score}</span><ArrowRight size={16} className="text-slate-300 transition group-hover:translate-x-1 group-hover:text-blue-500" /></Link>)}</div></div></section> : <div className="mt-8"><EmptyState /></div>}
  </div>
}
