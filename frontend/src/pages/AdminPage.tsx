import { Activity, BarChart3, BrainCircuit, ShieldCheck, UsersRound } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import { LoadingScreen } from '../components/LoadingScreen'
import { useAuth } from '../context/AuthContext'
import { api } from '../services/api'

type Overview = { users: number; analyses: number; feedback: number; average_ats: number; system_health: string; model: string; accuracy_note: string }

export function AdminPage() {
  const { user } = useAuth()
  const [data, setData] = useState<Overview | null>(null)
  const [error, setError] = useState('')
  useEffect(() => { if (user?.is_admin) api.adminOverview().then(setData).catch((e) => setError(e.message)) }, [user])
  if (!user?.is_admin) return <Navigate to="/app" replace />
  if (!data && !error) return <LoadingScreen message="Loading platform health" />
  if (error) return <div className="card text-rose-600">{error}</div>
  if (!data) return null
  const cards = [
    { label: 'Registered users', value: data.users, icon: UsersRound },
    { label: 'Resume analyses', value: data.analyses, icon: BarChart3 },
    { label: 'Feedback messages', value: data.feedback, icon: Activity },
    { label: 'Average ATS score', value: data.average_ats, icon: Activity },
    { label: 'System health', value: data.system_health, icon: ShieldCheck },
  ]
  return <div className="mx-auto max-w-6xl"><div><p className="text-sm font-bold text-blue-600">Administration</p><h2 className="mt-2 font-display text-3xl font-extrabold sm:text-4xl">Platform health and model governance</h2><p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">A compact operations view for usage, service health, and the active classifier.</p></div><section className="mt-8 grid gap-5 sm:grid-cols-2 xl:grid-cols-5">{cards.map(({ label, value, icon: Icon }) => <div key={label} className="card"><span className="grid h-11 w-11 place-items-center rounded-2xl bg-blue-50 text-blue-600 dark:bg-blue-500/10"><Icon size={20} /></span><p className="mt-5 text-xs font-bold uppercase tracking-[.13em] text-slate-400">{label}</p><p className="mt-2 font-display text-2xl font-extrabold capitalize">{value}</p></div>)}</section><section className="mt-6 grid gap-6 lg:grid-cols-[.8fr_1.2fr]"><div className="card"><div className="flex items-center gap-3"><BrainCircuit className="text-violet-600" /><h3 className="font-display text-xl font-bold">Active model</h3></div><p className="mt-5 rounded-2xl bg-slate-50 p-4 font-mono text-sm dark:bg-white/[.035]">{data.model}</p><p className="mt-4 text-xs leading-5 text-slate-500">Drop a validated trained artifact at the configured MODEL_PATH to switch inference from the taxonomy baseline to the supervised pipeline.</p></div><div className="card"><h3 className="font-display text-xl font-bold">Accuracy governance</h3><div className="mt-5 rounded-2xl border border-amber-200 bg-amber-50 p-5 text-sm leading-6 text-amber-900 dark:border-amber-500/20 dark:bg-amber-500/10 dark:text-amber-200">{data.accuracy_note}</div><div className="mt-5 grid gap-3 sm:grid-cols-3">{['Holdout evaluation', 'Per-class F1', 'Drift monitoring'].map((item) => <div key={item} className="rounded-2xl border border-slate-200 p-4 text-center text-xs font-bold dark:border-white/10">{item}</div>)}</div></div></section></div>
}
