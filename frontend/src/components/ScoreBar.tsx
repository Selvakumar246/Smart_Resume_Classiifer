export function ScoreBar({ label, value }: { label: string; value: number }) {
  return (
    <div>
      <div className="mb-2 flex items-center justify-between text-sm"><span className="font-medium capitalize text-slate-600 dark:text-slate-300">{label.replaceAll('_', ' ')}</span><span className="font-bold">{value}</span></div>
      <div className="h-2 overflow-hidden rounded-full bg-slate-100 dark:bg-white/10"><div className="h-full rounded-full bg-gradient-to-r from-blue-500 to-violet-500 transition-all duration-700" style={{ width: `${value}%` }} /></div>
    </div>
  )
}
