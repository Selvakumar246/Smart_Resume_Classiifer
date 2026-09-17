import { FileSearch } from 'lucide-react'
import { Link } from 'react-router-dom'

export function EmptyState() {
  return <div className="card py-14 text-center"><span className="mx-auto mb-5 grid h-14 w-14 place-items-center rounded-2xl bg-blue-50 text-blue-600 dark:bg-blue-500/10 dark:text-blue-300"><FileSearch /></span><h3 className="font-display text-xl font-bold">No analyses yet</h3><p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">Upload a real resume to classify its strongest career direction, measure ATS readiness, and identify skill gaps.</p><Link to="/app/analyze" className="button-primary mt-6">Analyze your first resume</Link></div>
}
