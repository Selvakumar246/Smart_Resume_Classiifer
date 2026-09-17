import { ArrowLeft, FileQuestion } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Logo } from '../components/Logo'

export function NotFoundPage() {
  return <div className="app-shell mesh-bg grid min-h-screen place-items-center p-5"><div className="max-w-lg text-center"><div className="flex justify-center"><Logo /></div><span className="mx-auto mt-14 grid h-20 w-20 place-items-center rounded-[2rem] bg-blue-50 text-blue-600 dark:bg-blue-500/10"><FileQuestion size={34} /></span><p className="mt-7 font-display text-6xl font-extrabold text-gradient">404</p><h1 className="mt-3 font-display text-2xl font-bold">This page is not part of the career path.</h1><p className="mt-3 text-sm leading-6 text-slate-500">The address may be incorrect or the report may have been removed.</p><Link to="/" className="button-primary mt-7"><ArrowLeft size={17} /> Return home</Link></div></div>
}
