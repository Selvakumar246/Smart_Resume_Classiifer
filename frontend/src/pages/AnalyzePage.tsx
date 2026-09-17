import { CheckCircle2, FileText, LoaderCircle, Sparkles, UploadCloud, X } from 'lucide-react'
import { useMemo, useRef, useState, type DragEvent, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'

const roles = ['Software Engineer', 'Backend Developer', 'Frontend Developer', 'Data Scientist', 'AI Engineer', 'Machine Learning Engineer', 'Cloud Engineer', 'DevOps Engineer', 'Cyber Security', 'Business Analyst', 'Digital Marketing', 'Finance', 'Human Resources', 'Mechanical Engineer', 'Civil Engineer', 'Electrical Engineer']

const stageDetails = [
  { name: 'Reading resume structure', detail: 'Extracting raw text, headings, and section layout...', targetPercent: 20 },
  { name: 'Detecting skills & experience', detail: 'Mapping technical stack, tools, and work history...', targetPercent: 42 },
  { name: 'Ranking career domains', detail: 'Cross-referencing 16 taxonomy role classifications...', targetPercent: 65 },
  { name: 'Scoring ATS readiness', detail: 'Evaluating document layout & bullet impact...', targetPercent: 85 },
  { name: 'Building recommendations', detail: 'Generating tailored skill gaps, projects & interview prep...', targetPercent: 96 },
]

export function AnalyzePage() {
  const [file, setFile] = useState<File | null>(null)
  const [role, setRole] = useState('')
  const [level, setLevel] = useState('entry')
  const [jd, setJd] = useState('')
  const [dragging, setDragging] = useState(false)
  const [loading, setLoading] = useState(false)
  const [stage, setStage] = useState(0)
  const [progress, setProgress] = useState(10)
  const [error, setError] = useState('')
  const inputRef = useRef<HTMLInputElement>(null)
  const navigate = useNavigate()
  const fileInfo = useMemo(() => file ? `${(file.size / 1024 / 1024).toFixed(2)} MB · ${file.name.split('.').pop()?.toUpperCase()}` : '', [file])

  const choose = (selected?: File) => {
    if (!selected) return
    const ext = selected.name.split('.').pop()?.toLowerCase()
    if (!['pdf', 'docx', 'txt'].includes(ext || '')) { setError('Choose a PDF, DOCX, or TXT resume.'); return }
    if (selected.size > 8 * 1024 * 1024) { setError('The maximum file size is 8 MB.'); return }
    setError(''); setFile(selected)
  }
  const drop = (event: DragEvent) => { event.preventDefault(); setDragging(false); choose(event.dataTransfer.files[0]) }
  const submit = async (event: FormEvent) => {
    event.preventDefault(); if (!file) { setError('Upload a resume before continuing.'); return }
    setError(''); setLoading(true); setStage(0); setProgress(15)

    // Smoothly pace stage transitions across the loading lifecycle
    const timer = window.setInterval(() => {
      setStage((current) => {
        const next = Math.min(stageDetails.length - 1, current + 1)
        setProgress(stageDetails[next].targetPercent)
        return next
      })
    }, 1200)

    try {
      const form = new FormData(); form.append('resume', file); form.append('target_role', role); form.append('experience_level', level); form.append('job_description', jd)
      const result = await api.createAnalysis(form)
      setProgress(100)
      setStage(stageDetails.length - 1)
      setTimeout(() => navigate(`/app/results/${result.id}`), 300)
    } catch (caught) { setError(caught instanceof Error ? caught.message : 'Analysis failed.'); setLoading(false) }
    finally { clearInterval(timer) }
  }

  if (loading) return (
    <div className="mx-auto grid min-h-[70vh] max-w-xl place-items-center">
      <div className="w-full text-center">
        <span className="mx-auto grid h-20 w-20 place-items-center rounded-[2rem] bg-gradient-to-br from-blue-600 to-violet-600 text-white shadow-glow">
          <LoaderCircle size={34} className="animate-spin" />
        </span>
        <h2 className="mt-7 font-display text-3xl font-extrabold">Analyzing resume evidence</h2>
        <p className="mt-2 text-sm leading-6 text-slate-500">
          {stageDetails[stage]?.detail || 'Processing resume payload through AI pipeline...'}
        </p>
        
        {/* Progress percentage bar */}
        <div className="mt-6">
          <div className="flex items-center justify-between text-xs font-bold text-slate-500">
            <span>Overall Progress</span>
            <span className="text-blue-600">{progress}%</span>
          </div>
          <div className="mt-2 h-2.5 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-white/[.06]">
            <div 
              className="h-full rounded-full bg-gradient-to-r from-blue-600 to-violet-600 transition-all duration-500 ease-out" 
              style={{ width: `${progress}%` }} 
            />
          </div>
        </div>

        <div className="card mt-8 text-left space-y-1">
          {stageDetails.map((item, index) => (
            <div key={item.name} className="flex items-center gap-3 py-2.5">
              <span className={`grid h-7 w-7 shrink-0 place-items-center rounded-full transition-colors ${
                index < stage ? 'bg-emerald-500 text-white' : index === stage ? 'bg-blue-600 text-white ring-4 ring-blue-100 dark:ring-blue-900/30' : 'bg-slate-100 text-slate-400 dark:bg-white/[.06]'
              }`}>
                {index < stage ? <CheckCircle2 size={15} /> : index === stage ? <LoaderCircle size={14} className="animate-spin" /> : index + 1}
              </span>
              <div className="min-w-0 flex-1">
                <p className={`text-sm font-semibold ${index <= stage ? 'text-slate-900 dark:text-white' : 'text-slate-400'}`}>
                  {item.name}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )

  return <div className="mx-auto max-w-4xl"><div><span className="eyebrow"><Sparkles size={13} /> New analysis</span><h2 className="mt-5 font-display text-3xl font-extrabold sm:text-4xl">Upload once. Understand the whole resume.</h2><p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">Use a clean, text-based resume. The target role and job description improve relevance but are not required.</p></div><form onSubmit={submit} className="mt-8 space-y-6">
    <section className="card"><div className="flex items-center justify-between"><div><p className="text-xs font-bold uppercase tracking-[.13em] text-blue-600">Step 1</p><h3 className="mt-1 font-display text-xl font-bold">Resume file</h3></div><span className="text-xs text-slate-400">PDF · DOCX · TXT</span></div>{file ? <div className="mt-6 flex items-center gap-4 rounded-3xl border border-emerald-200 bg-emerald-50 p-4 dark:border-emerald-500/20 dark:bg-emerald-500/10"><span className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-white text-emerald-600 shadow-sm dark:bg-white/10"><FileText size={22} /></span><div className="min-w-0 flex-1"><p className="truncate text-sm font-bold">{file.name}</p><p className="mt-1 text-xs text-slate-500 dark:text-slate-400">{fileInfo}</p></div><button type="button" onClick={() => setFile(null)} className="grid h-9 w-9 place-items-center rounded-xl text-slate-400 hover:bg-white hover:text-rose-500 dark:hover:bg-white/10" aria-label="Remove file"><X size={18} /></button></div> : <button type="button" onClick={() => inputRef.current?.click()} onDragOver={(e) => { e.preventDefault(); setDragging(true) }} onDragLeave={() => setDragging(false)} onDrop={drop} className={`mt-6 flex min-h-64 w-full flex-col items-center justify-center rounded-3xl border-2 border-dashed p-8 text-center transition ${dragging ? 'border-blue-500 bg-blue-50 dark:bg-blue-500/10' : 'border-slate-200 bg-slate-50 hover:border-blue-300 hover:bg-blue-50/50 dark:border-white/10 dark:bg-white/[.025]'}`}><span className="grid h-14 w-14 place-items-center rounded-2xl bg-white text-blue-600 shadow-soft dark:bg-white/[.07]"><UploadCloud size={26} /></span><p className="mt-5 font-display text-lg font-bold">Drop your resume here</p><p className="mt-2 text-sm text-slate-500">or click to browse from your device</p><span className="mt-4 rounded-full bg-slate-200/60 px-3 py-1 text-[11px] font-semibold text-slate-500 dark:bg-white/[.06]">Maximum 8 MB</span></button>}<input ref={inputRef} type="file" accept=".pdf,.docx,.txt" className="hidden" onChange={(e) => choose(e.target.files?.[0])} /></section>
    <section className="card"><p className="text-xs font-bold uppercase tracking-[.13em] text-blue-600">Step 2</p><h3 className="mt-1 font-display text-xl font-bold">Career context</h3><div className="mt-6 grid gap-5 sm:grid-cols-2"><div><label className="label" htmlFor="role">Target job role <span className="font-normal text-slate-400">(optional)</span></label><select id="role" className="input" value={role} onChange={(e) => setRole(e.target.value)}><option value="">Discover my strongest fit</option>{roles.map((item) => <option key={item}>{item}</option>)}</select></div><div><label className="label" htmlFor="level">Experience level</label><select id="level" className="input" value={level} onChange={(e) => setLevel(e.target.value)}><option value="student">Student</option><option value="entry">Fresher / entry level</option><option value="mid">Mid level</option><option value="senior">Senior level</option><option value="career-switcher">Career switcher</option></select></div></div></section>
    <section className="card"><div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-end"><div><p className="text-xs font-bold uppercase tracking-[.13em] text-blue-600">Step 3</p><h3 className="mt-1 font-display text-xl font-bold">Job description match</h3></div><span className="text-xs text-slate-400">Optional · improves alignment analysis</span></div><label className="sr-only" htmlFor="jd">Job description</label><textarea id="jd" className="input mt-6 min-h-44 resize-y leading-6" value={jd} onChange={(e) => setJd(e.target.value)} placeholder="Paste the responsibilities, requirements, technologies, and preferred qualifications from a real job posting..." /><div className="mt-2 text-right text-xs text-slate-400">{jd.length.toLocaleString()} characters</div></section>
    {error && <div role="alert" className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700 dark:border-rose-500/20 dark:bg-rose-500/10 dark:text-rose-300">{error}</div>}<div className="flex flex-col-reverse justify-end gap-3 sm:flex-row"><button type="button" onClick={() => { setFile(null); setRole(''); setJd(''); setError('') }} className="button-secondary">Clear form</button><button className="button-primary"><Sparkles size={18} /> Run AI analysis</button></div>
  </form></div>
}
