import { ArrowRight, FileClock, Search, Sparkles, Trash2 } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { EmptyState } from '../components/EmptyState'
import { LoadingScreen } from '../components/LoadingScreen'
import { api } from '../services/api'
import type { AnalysisSummary } from '../types'

export function HistoryPage() {
  const [items, setItems] = useState<AnalysisSummary[] | null>(null)
  const [query, setQuery] = useState('')
  const [error, setError] = useState('')
  useEffect(() => { api.analyses().then(setItems).catch((e) => setError(e.message)) }, [])
  const filtered = useMemo(() => (items || []).filter((item) => `${item.filename} ${item.top_category} ${item.target_role}`.toLowerCase().includes(query.toLowerCase())), [items, query])
  const remove = async (id: string) => {
    if (!window.confirm('Delete this analysis permanently?')) return
    try { await api.deleteAnalysis(id); setItems((current) => current?.filter((item) => item.id !== id) || []) }
    catch (caught) { setError(caught instanceof Error ? caught.message : 'Could not delete report.') }
  }
  if (!items && !error) return <LoadingScreen />
  return <div className="mx-auto max-w-7xl"><div className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end"><div><p className="text-sm font-bold text-blue-600">Resume history</p><h2 className="mt-2 font-display text-3xl font-extrabold sm:text-4xl">Every analysis, one searchable timeline</h2><p className="mt-3 text-sm text-slate-500">Reopen reports, compare ATS scores, or remove outdated versions.</p></div><Link to="/app/analyze" className="button-primary"><Sparkles size={17} /> New analysis</Link></div>
    {error && <div className="mt-6 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700 dark:border-rose-500/20 dark:bg-rose-500/10 dark:text-rose-300">{error}</div>}
    {items?.length ? <><div className="mt-8 max-w-md"><label className="sr-only" htmlFor="search-history">Search reports</label><div className="relative"><Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} /><input id="search-history" value={query} onChange={(e) => setQuery(e.target.value)} className="input pl-11" placeholder="Search file or career category" /></div></div><div className="mt-6 overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-soft dark:border-white/10 dark:bg-white/[.035]"><div className="hidden grid-cols-[1.2fr_.9fr_.45fr_.45fr] gap-4 border-b border-slate-200 px-5 py-4 text-[10px] font-bold uppercase tracking-[.15em] text-slate-400 dark:border-white/10 md:grid"><span>Resume</span><span>Classification</span><span>ATS</span><span className="text-right">Actions</span></div>{filtered.map((item) => <article key={item.id} className="grid gap-4 border-b border-slate-100 p-5 last:border-0 dark:border-white/[.06] md:grid-cols-[1.2fr_.9fr_.45fr_.45fr] md:items-center"><div className="flex min-w-0 items-center gap-3"><span className="grid h-11 w-11 shrink-0 place-items-center rounded-2xl bg-blue-50 text-blue-600 dark:bg-blue-500/10"><FileClock size={19} /></span><div className="min-w-0"><p className="truncate text-sm font-bold">{item.filename}</p><p className="mt-1 text-xs text-slate-400">{new Date(item.created_at).toLocaleDateString()} · {item.experience_level}</p></div></div><div><p className="text-sm font-semibold">{item.top_category}</p><p className="mt-1 text-xs text-slate-400">{item.target_role || 'Discovery mode'}</p></div><div><span className={`inline-flex min-w-14 justify-center rounded-full px-3 py-1 text-sm font-extrabold ${item.ats_score >= 80 ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-300' : item.ats_score >= 65 ? 'bg-amber-50 text-amber-700 dark:bg-amber-500/10 dark:text-amber-300' : 'bg-rose-50 text-rose-700 dark:bg-rose-500/10 dark:text-rose-300'}`}>{item.ats_score}</span></div><div className="flex justify-end gap-2"><button onClick={() => remove(item.id)} className="grid h-9 w-9 place-items-center rounded-xl text-slate-400 transition hover:bg-rose-50 hover:text-rose-600 dark:hover:bg-rose-500/10" aria-label={`Delete ${item.filename}`}><Trash2 size={17} /></button><Link to={`/app/results/${item.id}`} className="grid h-9 w-9 place-items-center rounded-xl bg-blue-600 text-white transition hover:bg-blue-700" aria-label={`Open ${item.filename}`}><ArrowRight size={17} /></Link></div></article>)}</div>{!filtered.length && <div className="mt-6 card text-center text-sm text-slate-500">No reports match “{query}”.</div>}</> : <div className="mt-8"><EmptyState /></div>}
  </div>
}
