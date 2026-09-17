import { ArrowRight, BookOpenCheck, BriefcaseBusiness, FolderGit2, Route, Sparkles } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { EmptyState } from '../components/EmptyState'
import { LoadingScreen } from '../components/LoadingScreen'
import { api } from '../services/api'
import type { AnalysisDetail, AnalysisSummary } from '../types'

export function CareerInsightsPage() {
  const [latest, setLatest] = useState<AnalysisDetail | null | undefined>(undefined)
  const [error, setError] = useState('')
  useEffect(() => {
    api.analyses().then(async (items: AnalysisSummary[]) => setLatest(items.length ? await api.analysis(items[0].id) : null)).catch((e) => setError(e.message))
  }, [])
  if (latest === undefined && !error) return <LoadingScreen />
  if (error) return <div className="card text-rose-600">{error}</div>
  if (!latest) return <div className="mx-auto max-w-5xl"><EmptyState /></div>
  const insights = latest.result.career_insights
  return <div className="mx-auto max-w-6xl"><div className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end"><div><p className="text-sm font-bold text-blue-600">Based on your latest analysis</p><h2 className="mt-2 font-display text-3xl font-extrabold sm:text-4xl">A focused path toward {insights.recommended_role}</h2><p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">Recommendations are derived from the detected evidence and gaps in {latest.filename}.</p></div><Link to={`/app/results/${latest.id}`} className="button-secondary">Open full report <ArrowRight size={17} /></Link></div>
    <section className="mt-8 grid gap-5 md:grid-cols-3"><div className="card md:col-span-2"><div className="flex items-center gap-3"><span className="grid h-11 w-11 place-items-center rounded-2xl bg-blue-50 text-blue-600 dark:bg-blue-500/10"><Route size={20} /></span><h3 className="font-display text-xl font-bold">Six-week roadmap</h3></div><div className="mt-6 space-y-4">{insights.roadmap.map((step, index) => <div key={step} className="flex gap-4"><span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-blue-600 text-sm font-bold text-white">{index + 1}</span><div className="pt-1.5 text-sm leading-6 text-slate-600 dark:text-slate-300">{step}</div></div>)}</div></div><div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-blue-600 to-violet-700 p-6 text-white shadow-glow"><Sparkles className="absolute right-5 top-5 opacity-40" /><p className="text-xs font-bold uppercase tracking-[.14em] text-blue-100">Target direction</p><h3 className="mt-3 font-display text-3xl font-extrabold">{insights.recommended_role}</h3><p className="mt-4 text-sm leading-6 text-blue-100">Build evidence first: one deployed project, clear documentation, and measurable outcomes.</p></div></section>
    <section className="mt-5 grid gap-5 md:grid-cols-2"><div className="card"><div className="flex items-center gap-3"><FolderGit2 className="text-violet-600" /><h3 className="font-display text-xl font-bold">Recommended projects</h3></div><div className="mt-5 space-y-3">{insights.recommended_projects.map((item) => <div key={item} className="flex gap-3 rounded-2xl bg-slate-50 p-4 text-sm leading-6 dark:bg-white/[.035]"><BriefcaseBusiness className="mt-1 shrink-0 text-blue-600" size={17} />{item}</div>)}</div></div><div className="card"><div className="flex items-center gap-3"><BookOpenCheck className="text-emerald-600" /><h3 className="font-display text-xl font-bold">Certification strategy</h3></div><div className="mt-5 space-y-3">{insights.recommended_certifications.map((item) => <div key={item} className="rounded-2xl bg-slate-50 p-4 text-sm leading-6 dark:bg-white/[.035]">{item}</div>)}<p className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-xs leading-5 text-amber-800 dark:border-amber-500/20 dark:bg-amber-500/10 dark:text-amber-200">{insights.salary_note}</p></div></div></section>
  </div>
}
