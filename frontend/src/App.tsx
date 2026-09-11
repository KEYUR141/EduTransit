import { useEffect, useMemo, useState } from 'react'
import type { FormEvent } from 'react'
import {
  ArrowRight,
  Check,
  ChevronRight,
  CircleHelp,
  FileText,
  Globe2,
  GraduationCap,
  Languages,
  Menu,
  MessageSquare,
  Network,
  PauseCircle,
  School,
  ShieldCheck,
  Upload,
  UserRound,
  X,
} from 'lucide-react'

import './App.css'
import {
  analyseSupportCase,
  checkApiHealth,
  createSupportCase,
  listSupportCases,
  type RagAnalysis,
  type SupportCase,
} from './api'

type RequestKind = {
  id: string
  title: string
  description: string
  icon: typeof School
}

const requestKinds: RequestKind[] = [
  {
    id: 'school-change',
    title: 'School or board change',
    description: 'Compare a syllabus, sequence or grade transition.',
    icon: School,
  },
  {
    id: 'language',
    title: 'Language difficulty',
    description: 'Separate subject understanding from academic language.',
    icon: Languages,
  },
  {
    id: 'learning-break',
    title: 'Learning interruption',
    description: 'Find what changed after an absence or study break.',
    icon: PauseCircle,
  },
  {
    id: 'higher-education',
    title: 'Programme transition',
    description: 'Compare competencies, prerequisites and evidence.',
    icon: GraduationCap,
  },
  {
    id: 'study-abroad',
    title: 'Study abroad',
    description: 'Review academic readiness and external requirements.',
    icon: Globe2,
  },
  {
    id: 'unsure',
    title: 'Something else',
    description: 'Describe the situation without choosing a category.',
    icon: CircleHelp,
  },
]

const fallbackCase: SupportCase = {
  id: 0,
  reference: 'GM-2048',
  title: 'B.Pharm to Master of Data Science',
  requester_name: 'Ananya Rao',
  requester_role: 'student',
  category: 'study-abroad',
  category_label: 'Study-abroad preparation',
  summary: 'Understand academic readiness for a Master of Data Science programme.',
  source_label: 'PCI B.Pharm',
  source_location: 'India',
  destination_label: 'Master of Data Science',
  destination_location: 'UBC, Canada',
  status: 'instructor_review',
  status_label: 'Instructor review',
  progress_stage: 2,
  analysis_confidence_score: 0.55,
  analysis_confidence_level: 'medium',
  review_required: true,
  review_route: 'instructor_review',
  analysis_snapshot: {},
  analysed_at: '',
  is_demo: true,
  created_at: '',
  updated_at: '',
}

const stages = [
  'Request received',
  'Evidence review',
  'Gap comparison',
  'Support roadmap',
  'Readiness review',
]

function routeLabel(route?: SupportCase['review_route']) {
  if (route === 'specialist_escalation') return 'Specialist escalation'
  if (route === 'instructor_review') return 'Instructor review'
  if (route === 'provisional_guidance') return 'Provisional guidance'
  return 'Awaiting analysis'
}

function App() {
  const [requestOpen, setRequestOpen] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)
  const [selectedKind, setSelectedKind] = useState('study-abroad')
  const [role, setRole] = useState('Student')
  const [summary, setSummary] = useState('')
  const [requesterName, setRequesterName] = useState('')
  const [sourceLabel, setSourceLabel] = useState('')
  const [destinationLabel, setDestinationLabel] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [analysing, setAnalysing] = useState(false)
  const [createdReference, setCreatedReference] = useState('')
  const [requestError, setRequestError] = useState('')
  const [analysisError, setAnalysisError] = useState('')
  const [submissionMode, setSubmissionMode] = useState<'api' | 'offline'>('api')
  const [apiStatus, setApiStatus] = useState<'connecting' | 'connected' | 'offline'>(
    'connecting',
  )
  const [supportCases, setSupportCases] = useState<SupportCase[]>([])

  const selectedRequest = useMemo(
    () => requestKinds.find((item) => item.id === selectedKind) ?? requestKinds[0],
    [selectedKind],
  )
  const SelectedIcon = selectedRequest.icon
  const activeCase = supportCases[0] ?? fallbackCase
  const confidence = activeCase.analysis_confidence_score ?? 0
  const confidencePercent = Math.round(confidence * 100)
  const analysis = activeCase.analysis_snapshot as RagAnalysis | undefined
  const evidence = Array.isArray(analysis?.results) ? analysis.results.slice(0, 2) : []

  useEffect(() => {
    let cancelled = false
    Promise.all([checkApiHealth(), listSupportCases()])
      .then(([, cases]) => {
        if (cancelled) return
        setSupportCases(cases)
        setApiStatus('connected')
      })
      .catch(() => {
        if (!cancelled) setApiStatus('offline')
      })
    return () => {
      cancelled = true
    }
  }, [])

  const openRequest = (kind?: string) => {
    if (kind) setSelectedKind(kind)
    setSubmitted(false)
    setCreatedReference('')
    setRequestError('')
    setRequestOpen(true)
  }

  const submitRequest = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (summary.trim().length < 15) {
      setRequestError('Please describe the situation in at least 15 characters.')
      return
    }
    setSubmitting(true)
    setRequestError('')
    const requesterRole =
      role === 'Student' ? 'student' : role === 'Parent or guardian' ? 'parent' : 'educator'
    try {
      const created = await createSupportCase({
        title:
          sourceLabel && destinationLabel
            ? `${sourceLabel} to ${destinationLabel}`
            : selectedRequest.title,
        requester_name: requesterName.trim(),
        requester_role: requesterRole,
        category: selectedKind,
        summary: summary.trim(),
        source_label: sourceLabel.trim(),
        source_location: '',
        destination_label: destinationLabel.trim(),
        destination_location: '',
      })
      setSupportCases((cases) => [created, ...cases])
      setCreatedReference(created.reference)
      setSubmissionMode('api')
      setApiStatus('connected')
    } catch {
      setCreatedReference(`LOCAL-${Date.now().toString().slice(-6)}`)
      setSubmissionMode('offline')
      setApiStatus('offline')
    } finally {
      setSubmitting(false)
      setSubmitted(true)
    }
  }

  const runAnalysis = async () => {
    if (!activeCase.id) {
      setAnalysisError('Create a request first to run evidence analysis.')
      return
    }
    setAnalysing(true)
    setAnalysisError('')
    try {
      const result = await analyseSupportCase(activeCase.id)
      setSupportCases((cases) => [
        result.case,
        ...cases.filter((item) => item.id !== result.case.id),
      ])
      setApiStatus('connected')
    } catch (error) {
      setAnalysisError(error instanceof Error ? error.message : 'Analysis could not be completed.')
    } finally {
      setAnalysing(false)
    }
  }

  return (
    <div className="app-shell" id="top">
      <div className="system-line">
        <div className="portal-width system-line-inner">
          <span>GapMap education continuity portal</span>
          <span className={`connection-state ${apiStatus}`}>
            <i /> {apiStatus === 'connected' ? 'System available' : apiStatus === 'offline' ? 'Demo mode' : 'Connecting'}
          </span>
        </div>
      </div>

      <header className="site-header">
        <div className="portal-width header-grid">
          <a className="brand" href="#top" aria-label="GapMap home">
            <span className="brand-symbol"><Network size={19} /></span>
            <strong>gapmap</strong>
          </a>
          <nav className={mobileOpen ? 'main-nav open' : 'main-nav'} aria-label="Main navigation">
            <a href="#workspace">Workspace</a>
            <a href="#support">Support directory</a>
            <a href="#method">How it works</a>
          </nav>
          <div className="header-actions">
            <button className="quiet-button" type="button" onClick={() => openRequest('unsure')}>
              Ask for help
            </button>
            <button className="pill-button small" type="button" onClick={() => openRequest()}>
              Open a case <ArrowRight size={15} />
            </button>
            <button
              className="menu-button"
              type="button"
              aria-label="Toggle navigation"
              aria-expanded={mobileOpen}
              onClick={() => setMobileOpen((value) => !value)}
            >
              {mobileOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>
        </div>
      </header>

      <main>
        <section className="hero-section">
          <div className="portal-width hero-grid">
            <div>
              <p className="mono-label">EDUCATION CONTINUITY / CASE SUPPORT</p>
              <h1>Find what is missing.<br />Keep what you already know.</h1>
            </div>
            <div className="hero-intro">
              <p>
                A support portal for students changing schools, programmes, languages or countries.
                Evidence is compared before a roadmap is suggested.
              </p>
              <button className="pill-button" type="button" onClick={() => openRequest()}>
                <span className="button-dot" /> Raise a support request
              </button>
              <span className="hero-note">Sources visible · confidence explained · people in control</span>
            </div>
          </div>
          <div className="portal-width signal-strip" aria-label="GapMap principles">
            <span>01 / describe the change</span>
            <span>02 / compare evidence</span>
            <span>03 / review uncertainty</span>
            <span>04 / build the next step</span>
          </div>
        </section>

        <section className="portal-section" id="workspace">
          <div className="portal-width portal-heading">
            <div>
              <p className="mono-label">LEARNER WORKSPACE</p>
              <h2>Your active case</h2>
            </div>
            <p>One case file. Every source, question and decision stays in context.</p>
          </div>

          <div className="portal-width portal-grid">
            <aside className="directory" id="support">
              <p className="column-title">Support directory</p>
              <div className="directory-list">
                {requestKinds.map((item, index) => {
                  const Icon = item.icon
                  return (
                    <button type="button" key={item.id} onClick={() => openRequest(item.id)}>
                      <span className="directory-index">0{index + 1}</span>
                      <span className="directory-icon"><Icon size={17} /></span>
                      <span><strong>{item.title}</strong><small>{item.description}</small></span>
                      <ChevronRight size={16} />
                    </button>
                  )
                })}
              </div>
              <div className="directory-help">
                <MessageSquare size={18} />
                <p><strong>Not sure where it belongs?</strong> Describe the change in your own words.</p>
                <button type="button" onClick={() => openRequest('unsure')}>Start without a category</button>
              </div>
            </aside>

            <article className="case-file">
              <div className="case-file-head">
                <div>
                  <p className="mono-label">CASE {activeCase.reference}</p>
                  <h3>{activeCase.title || activeCase.category_label}</h3>
                  <p className="case-owner">{activeCase.requester_name || 'Learner'} · {activeCase.category_label}</p>
                </div>
                <span className="status-label"><i /> {activeCase.status_label}</span>
              </div>

              <div className="transition-row">
                <div><span>Current education</span><strong>{activeCase.source_label || 'Evidence pending'}</strong><small>{activeCase.source_location || 'Location not added'}</small></div>
                <ArrowRight size={18} />
                <div><span>Intended destination</span><strong>{activeCase.destination_label || 'Goal not confirmed'}</strong><small>{activeCase.destination_location || 'Location not added'}</small></div>
              </div>

              <section className="analysis-panel" aria-label="Evidence confidence">
                <div className="confidence-readout">
                  <p className="column-title">Evidence confidence</p>
                  <strong>{activeCase.analysis_confidence_level === 'not_analysed' || activeCase.analysis_confidence_level == null ? '—' : `${confidencePercent}%`}</strong>
                  <span>{activeCase.analysis_confidence_level?.replace('_', ' ') || 'Not analysed'}</span>
                </div>
                <div className="confidence-detail">
                  <div className="meter"><span style={{ width: `${confidencePercent}%` }} /></div>
                  <p>
                    This measures the quality of retrieved evidence—not admission, credit or eligibility.
                  </p>
                  <dl>
                    <div><dt>Review route</dt><dd>{routeLabel(activeCase.review_route)}</dd></div>
                    <div><dt>Human review</dt><dd>{activeCase.review_required ? 'Required' : 'Not yet required'}</dd></div>
                    <div><dt>Evidence found</dt><dd>{analysis?.count ?? 'Run analysis'}</dd></div>
                  </dl>
                </div>
              </section>

              {evidence.length > 0 && (
                <section className="evidence-list" aria-label="Retrieved evidence">
                  <p className="column-title">Retrieved evidence</p>
                  {evidence.map((item) => (
                    <div key={item.chunk_id}>
                      <FileText size={16} />
                      <span><strong>{item.citation.title}</strong><small>{item.text}</small></span>
                      <em>{Math.round(item.score * 100)}%</em>
                    </div>
                  ))}
                </section>
              )}

              <div className="case-actions">
                <button className="pill-button" type="button" onClick={runAnalysis} disabled={analysing}>
                  {analysing ? 'Comparing evidence…' : activeCase.analysed_at ? 'Run analysis again' : 'Run evidence analysis'}
                  {!analysing && <ArrowRight size={16} />}
                </button>
                <button className="line-button" type="button"><Upload size={16} /> Add evidence</button>
              </div>
              {analysisError && <p className="inline-error" role="alert">{analysisError}</p>}
            </article>

            <aside className="case-desk">
              <p className="column-title">Case desk</p>
              <div className="desk-status">
                <span className="desk-avatar"><UserRound size={19} /></span>
                <div><small>Assigned support</small><strong>{activeCase.review_required ? 'Instructor review queue' : 'GapMap case desk'}</strong></div>
              </div>
              <div className="desk-block">
                <span>What happens next</span>
                <p>{activeCase.review_required ? 'An instructor checks uncertain matches and requests only the evidence still needed.' : 'Run evidence analysis to identify the smallest useful next step.'}</p>
              </div>
              <ol className="stage-list">
                {stages.map((stage, index) => (
                  <li key={stage} className={index + 1 <= activeCase.progress_stage ? 'active' : ''}>
                    <span>{String(index + 1).padStart(2, '0')}</span>{stage}
                  </li>
                ))}
              </ol>
              <button className="desk-link" type="button" onClick={() => openRequest('unsure')}>
                Message the case desk <ArrowRight size={15} />
              </button>
            </aside>
          </div>
        </section>

        <section className="method-section" id="method">
          <div className="portal-width method-grid">
            <div><p className="mono-label">WHY GAPMAP</p><h2>Guidance that can say<br />“we need more evidence.”</h2></div>
            <div className="method-point"><span>01</span><strong>Evidence before inference</strong><p>Academic claims remain connected to reviewed sources.</p></div>
            <div className="method-point"><span>02</span><strong>Confidence with limits</strong><p>Weak and novel matches move to an instructor instead of becoming a confident answer.</p></div>
            <div className="method-point"><span>03</span><strong>One useful route</strong><p>Learn, verify, diagnose or escalate—without assigning unnecessary courses.</p></div>
          </div>
        </section>
      </main>

      <footer>
        <div className="portal-width footer-grid">
          <a className="brand" href="#top"><span className="brand-symbol"><Network size={17} /></span><strong>gapmap</strong></a>
          <p>Prototype guidance only. Official admission, licensing and credit decisions remain with authorised institutions.</p>
          <button className="line-button inverse" type="button" onClick={() => openRequest()}>Open a case</button>
        </div>
      </footer>

      {requestOpen && (
        <div className="modal-backdrop" role="presentation" onMouseDown={() => setRequestOpen(false)}>
          <section className="request-modal" role="dialog" aria-modal="true" aria-labelledby="request-title" onMouseDown={(event) => event.stopPropagation()}>
            <div className="modal-head">
              <p className="mono-label">NEW SUPPORT CASE</p>
              <button type="button" aria-label="Close request form" onClick={() => setRequestOpen(false)}><X size={19} /></button>
            </div>
            {!submitted ? (
              <form onSubmit={submitRequest}>
                <h2 id="request-title">Tell us what changed.</h2>
                <p className="modal-intro">Use plain language. Academic evidence can be added after the case is created.</p>

                <label htmlFor="request-kind">Type of support</label>
                <select id="request-kind" value={selectedKind} onChange={(event) => setSelectedKind(event.target.value)}>
                  {requestKinds.map((item) => <option key={item.id} value={item.id}>{item.title}</option>)}
                </select>
                <div className="selection-note"><SelectedIcon size={16} /> {selectedRequest.description}</div>

                <fieldset>
                  <legend>I am a</legend>
                  <div className="choice-row">
                    {['Student', 'Parent or guardian', 'Educator or counsellor'].map((item) => (
                      <button className={role === item ? 'choice active' : 'choice'} type="button" key={item} onClick={() => setRole(item)}>{item}</button>
                    ))}
                  </div>
                </fieldset>

                <label htmlFor="requester-name">Your name <span>optional</span></label>
                <input id="requester-name" value={requesterName} onChange={(event) => setRequesterName(event.target.value)} placeholder="Name" />

                <div className="field-grid">
                  <div><label htmlFor="source-label">Current school or programme</label><input id="source-label" value={sourceLabel} onChange={(event) => setSourceLabel(event.target.value)} placeholder="e.g. PCI B.Pharm" /></div>
                  <div><label htmlFor="destination-label">Destination goal</label><input id="destination-label" value={destinationLabel} onChange={(event) => setDestinationLabel(event.target.value)} placeholder="e.g. MSc Data Science" /></div>
                </div>

                <label htmlFor="issue-summary">Briefly describe the difficulty</label>
                <textarea id="issue-summary" value={summary} onChange={(event) => setSummary(event.target.value)} placeholder="What changed, and what are you trying to understand?" rows={5} required />

                <div className="form-note"><ShieldCheck size={16} /> Prototype mode. Do not enter sensitive personal information.</div>
                {requestError && <p className="inline-error" role="alert">{requestError}</p>}
                <button className="pill-button full" type="submit" disabled={submitting}>{submitting ? 'Submitting…' : 'Create support request'} {!submitting && <ArrowRight size={16} />}</button>
              </form>
            ) : (
              <div className="success-state">
                <span className="success-mark"><Check size={25} /></span>
                <p className="mono-label">REQUEST CREATED</p>
                <h2 id="request-title">Your case desk is ready.</h2>
                <p>The request is organised as <strong>{selectedRequest.title}</strong>. You can now add evidence and run the first comparison.</p>
                <div className="reference-row"><span>Reference</span><strong>{createdReference}</strong><small>{submissionMode === 'api' ? 'Stored in GapMap' : 'Local demo only'}</small></div>
                <button className="pill-button full" type="button" onClick={() => { setRequestOpen(false); setTimeout(() => document.getElementById('workspace')?.scrollIntoView({ behavior: 'smooth' }), 0) }}>Open workspace <ArrowRight size={16} /></button>
              </div>
            )}
          </section>
        </div>
      )}
    </div>
  )
}

export default App
