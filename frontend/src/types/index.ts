export type User = {
  id: string
  name: string
  email: string
  plan: string
  is_admin: boolean
  created_at: string
}

export type AuthResponse = { access_token: string; token_type: string; user: User }

export type ClassificationItem = {
  category: string
  confidence: number
  reason: string
  evidence: string[]
}

export type SkillGap = {
  skill: string
  priority: string
  difficulty: string
  estimated_learning_time: string
  roadmap: string[]
}

export type AnalysisResult = {
  summary: {
    word_count: number
    detected_skills_count: number
    sections_found: number
    contact: { emails: string[]; phones: string[]; github: string[]; linkedin: string[]; urls: string[] }
  }
  classification: {
    top_categories: ClassificationItem[]
    confidence_quality: string
    disclaimer: string
  }
  ats: {
    overall_score: number
    scores: Record<string, number>
    deductions: string[]
    sections: Record<string, boolean>
  }
  skills: { detected: string[]; gaps: SkillGap[] }
  job_match: null | {
    match_score: number
    semantic_similarity: number
    matched_keywords: string[]
    missing_keywords: string[]
    missing_soft_skills: string[]
    suggestions: string[]
  }
  improvements: {
    bullet_rewrites: { original: string; improved: string }[]
    action_verbs: string[]
    recommendations: string[]
  }
  career_insights: {
    recommended_role: string
    recommended_projects: string[]
    recommended_certifications: string[]
    roadmap: string[]
    salary_note: string
  }
  interview: Record<string, string[]>
}

export type AnalysisDetail = {
  id: string
  filename: string
  target_role: string
  experience_level: string
  result: AnalysisResult
  created_at: string
}

export type AnalysisSummary = {
  id: string
  filename: string
  target_role: string
  experience_level: string
  top_category: string
  ats_score: number
  created_at: string
}

export type DashboardData = {
  total_analyses: number
  average_ats: number
  top_category: string
  plan: string
  recent: { id: string; filename: string; category: string; ats_score: number; created_at: string }[]
}
