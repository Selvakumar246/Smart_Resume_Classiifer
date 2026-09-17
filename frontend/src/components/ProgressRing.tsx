export function ProgressRing({ value, size = 128, label }: { value: number; size?: number; label?: string }) {
  const radius = 48
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (Math.max(0, Math.min(100, value)) / 100) * circumference
  return (
    <div className="relative inline-grid place-items-center" style={{ width: size, height: size }} role="img" aria-label={`${label || 'Score'} ${value} out of 100`}>
      <svg viewBox="0 0 120 120" className="h-full w-full -rotate-90">
        <circle cx="60" cy="60" r={radius} fill="none" stroke="currentColor" strokeWidth="9" className="text-slate-200 dark:text-white/10" />
        <circle cx="60" cy="60" r={radius} fill="none" stroke="url(#scoreGradient)" strokeWidth="9" strokeLinecap="round" strokeDasharray={circumference} strokeDashoffset={offset} />
        <defs><linearGradient id="scoreGradient"><stop stopColor="#2563eb" /><stop offset="1" stopColor="#7c3aed" /></linearGradient></defs>
      </svg>
      <div className="absolute text-center"><div className="font-display text-3xl font-extrabold">{value}</div><div className="text-[10px] font-bold uppercase tracking-[.18em] text-slate-400">{label || 'Score'}</div></div>
    </div>
  )
}
