import { BarChart3, BrainCircuit, FileSearch, Gauge, MessageSquareText, Route, ShieldCheck, Sparkles } from 'lucide-react'

export const features = [
  { icon: BrainCircuit, title: 'Career classification', text: 'Rank the five career domains most supported by your resume and show the evidence behind each prediction.' },
  { icon: Gauge, title: 'Transparent ATS scoring', text: 'See formatting, keyword, skill, project, experience, education, grammar, and section-level scores.' },
  { icon: FileSearch, title: 'Job description match', text: 'Compare resume language with a target role, identify matched and missing keywords, and improve alignment.' },
  { icon: Route, title: 'Skill-gap roadmap', text: 'Prioritize missing skills by urgency, difficulty, estimated learning time, and a practical learning sequence.' },
  { icon: Sparkles, title: 'Resume improvements', text: 'Find weak bullets, strengthen action language, and add measurable evidence without inventing achievements.' },
  { icon: MessageSquareText, title: 'Interview preparation', text: 'Generate technical, behavioral, HR, project, and role-specific questions grounded in your resume.' },
  { icon: BarChart3, title: 'Career intelligence', text: 'Turn the analysis into role-aligned project, certification, and portfolio recommendations.' },
  { icon: ShieldCheck, title: 'Privacy-conscious architecture', text: 'JWT authentication, isolated user history, validation, file limits, and deployment-ready API boundaries.' },
]

export const faqs = [
  ['Does the AI guarantee a job?', 'No. It provides structured decision support. Hiring depends on role requirements, evidence, interviews, market conditions, and human judgment.'],
  ['Is the prediction really accurate?', 'The included baseline is transparent and functional. Production accuracy must be measured with a representative labeled dataset, held-out testing, drift monitoring, and human review.'],
  ['Which files are supported?', 'PDF, DOCX, and TXT are supported, up to the configured file-size limit. Text-based PDFs work best.'],
  ['Does it invent skills or achievements?', 'No. Recommendations use placeholders when a measurable outcome is missing, so users can add only truthful evidence.'],
]
