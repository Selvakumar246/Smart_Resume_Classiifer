import { FileCheck2 } from 'lucide-react'
import { Link } from 'react-router-dom'

export function Logo({ compact = false }: { compact?: boolean }) {
  return (
    <Link to="/" className="inline-flex items-center gap-3" aria-label="Smart Resume Classification home">
      <img src="/icon.png" alt="Smart Resume Logo" className="h-10 w-10 rounded-2xl object-cover shadow-md shadow-blue-500/20" />
      {!compact && <span className="font-display text-[15px] font-extrabold leading-tight tracking-tight text-slate-950 dark:text-white">Smart Resume<br /><span className="text-blue-600 dark:text-blue-400">Classification</span></span>}
    </Link>
  )
}
