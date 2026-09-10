import { useEffect, useMemo, useState } from 'react'
import type { FormEvent } from 'react'
import {
  ArrowRight,
  BookOpenCheck,
  BriefcaseBusiness,
  Check,
  ChevronRight,
  CircleHelp,
  Clock3,
  FileCheck2,
  Globe2,
  GraduationCap,
  Languages,
  LifeBuoy,
  Map,
  Menu,
  MessageCircleMore,
  Network,
  PauseCircle,
  School,
  Search,
  ShieldCheck,
  Sparkles,
  Upload,
  UserRound,
  X,
} from 'lucide-react'

import './App.css'
import {
  checkApiHealth,
  createSupportCase,
  listSupportCases,
  type SupportCase,
} from './api'

type RequestKind = {
  id: string
  title: string
  description: string
  icon: typeof School
  tone: string
}

const requestKinds: RequestKind[] = [
  {
    id: 'school-change',
    title: 'School or board change',
    description: 'Help me adjust to a different syllabus or teaching sequence.',
    icon: School,
    tone: 'blue',
  },
  {
    id: 'language',
    title: 'Language difficulty',
    description: 'I understand the topic, but the new academic language is unfamiliar.',
    icon: Languages,
    tone: 'violet',
  },
  {
    id: 'learning-break',
    title: 'Learning interruption',
    description: 'An absence or study break has affected my current readiness.',
    icon: PauseCircle,
    tone: 'amber',
  },
  {
    id: 'higher-education',
    title: 'College or programme change',
    description: 'Compare courses, competencies, credits and prerequisite depth.',
    icon: GraduationCap,
    tone: 'teal',
  },
  {
    id: 'study-abroad',
    title: 'Study-abroad preparation',
    description: 'Understand academic readiness and required supporting evidence.',
    icon: Globe2,
    tone: 'coral',
  },
  {
    id: 'unsure',
    title: 'I am not sure',
    description: 'Describe the situation and let the support workflow classify it.',
    icon: CircleHelp,
    tone: 'slate',
  },
]

const updates = [
  {
    title: 'Course evidence reviewed',
    text: 'Three verified B.Pharm courses were added to the comparison.',
    time: '10 minutes ago',
    icon: FileCheck2,
  },
  {
    title: 'One clarification requested',
    text: 'A detailed mathematics course outline would improve the equivalence review.',
    time: 'Action needed',
    icon: MessageCircleMore,
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
  status: 'gap_analysis',
  status_label: 'Gap comparison',
  progress_stage: 3,
  is_demo: true,
  created_at: '',
  updated_at: '',
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
  const [createdReference, setCreatedReference] = useState('')
  const [requestError, setRequestError] = useState('')
  const [submissionMode, setSubmissionMode] = useState<'api' | 'offline'>('api')
  const [apiStatus, setApiStatus] = useState<'connecting' | 'connected' | 'offline'>('connecting')
  const [supportCases, setSupportCases] = useState<SupportCase[]>([])

  const selectedRequest = useMemo(
    () => requestKinds.find((item) => item.id === selectedKind) ?? requestKinds[0],
    [selectedKind],
  )

  const activeCase = supportCases[0] ?? fallbackCase
  const progressStage = Math.min(Math.max(activeCase.progress_stage, 1), 5)
  const progressPercent = ((progressStage - 1) / 4) * 100
  const stageClass = (stage: number) =>
    stage < progressStage ? 'done' : stage === progressStage ? 'current' : ''

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

  return (
    <div className="app-shell">
      <div className="support-ribbon">
        <div className="page-width ribbon-inner">
          <span><ShieldCheck size={15} /> Supportive, evidence-led guidance</span>
          <span className="ribbon-note">For students, families, educators and counsellors</span>
          <span><Languages size={15} /> English · हिन्दी support</span>
        </div>
      </div>

      <header className="site-header">
        <div className="page-width header-inner">
          <a className="brand" href="#top" aria-label="GapMap home">
            <span className="brand-mark"><Network size={22} /></span>
            <span>
              <strong>GapMap</strong>
              <small>Education continuity support</small>
            </span>
          </a>

          <nav className={mobileOpen ? 'main-nav mobile-visible' : 'main-nav'} aria-label="Main navigation">
            <a href="#support">Get support</a>
            <a href="#workspace">My workspace</a>
            <a href="#how-it-works">How it works</a>
            <a href="#resources">Resources</a>
          </nav>

          <div className="header-actions">
            <span className={`api-indicator ${apiStatus}`} title="Django API connection status">
              <span />
              {apiStatus === 'connected' ? 'API connected' : apiStatus === 'offline' ? 'Demo offline' : 'Connecting'}
            </span>
            <button
              className="text-button desktop-action"
              type="button"
              onClick={() => document.getElementById('workspace')?.scrollIntoView({ behavior: 'smooth' })}
            >
              <Search size={17} /> Track a request
            </button>
            <button className="primary-button compact" type="button" onClick={() => openRequest()}>
              Raise a support request
            </button>
            <button
              className="menu-button"
              type="button"
              aria-label="Toggle navigation"
              aria-expanded={mobileOpen}
              onClick={() => setMobileOpen((value) => !value)}
            >
              {mobileOpen ? <X /> : <Menu />}
            </button>
          </div>
        </div>
      </header>

      <main id="top">
        <section className="hero-section">
          <div className="hero-glow glow-one" />
          <div className="hero-glow glow-two" />
          <div className="page-width hero-grid">
            <div className="hero-copy">
              <span className="eyebrow"><LifeBuoy size={17} /> Academic transition support</span>
              <h1>Your learning should not restart when your education changes.</h1>
              <p>
                Tell us what changed. GapMap helps organise your concern, review your learning evidence,
                identify only the gaps that matter and create a clear support path.
              </p>
              <div className="hero-actions">
                <button className="primary-button" type="button" onClick={() => openRequest()}>
                  Raise a support request <ArrowRight size={18} />
                </button>
                <a className="secondary-button" href="#workspace">
                  View demo workspace
                </a>
              </div>
              <div className="trust-row">
                <span><Check size={16} /> No unnecessary roadmap</span>
                <span><Check size={16} /> Sources remain visible</span>
                <span><Check size={16} /> Human-review ready</span>
              </div>
            </div>

            <div className="hero-journey" aria-label="Support journey preview">
              <div className="journey-heading">
                <div>
                  <span className="mini-label">A support journey, not a generic test</span>
                  <h2>From concern to a clear next step</h2>
                </div>
                <span className="live-badge"><span /> Demo journey</span>
              </div>

              <div className="journey-path">
                <div className="journey-line" />
                <div className="journey-step active">
                  <span className="step-node"><MessageCircleMore size={19} /></span>
                  <div><small>01</small><strong>Share the situation</strong><p>What changed, and where are you blocked?</p></div>
                </div>
                <div className="journey-step">
                  <span className="step-node"><FileCheck2 size={19} /></span>
                  <div><small>02</small><strong>Review evidence</strong><p>Courses, assessments, documents and goals.</p></div>
                </div>
                <div className="journey-step">
                  <span className="step-node"><Network size={19} /></span>
                  <div><small>03</small><strong>Locate the actual gap</strong><p>Curriculum, mastery, language or evidence.</p></div>
                </div>
                <div className="journey-step">
                  <span className="step-node"><Map size={19} /></span>
                  <div><small>04</small><strong>Receive a support path</strong><p>Learn, diagnose, verify or request review.</p></div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="support-section" id="support">
          <div className="page-width">
            <div className="section-heading split-heading">
              <div>
                <span className="eyebrow soft">Start with your situation</span>
                <h2>What would you like help with?</h2>
                <p>You do not need to know the technical name of the gap before asking for support.</p>
              </div>
              <button className="text-link" type="button" onClick={() => openRequest('unsure')}>
                Help me choose <ChevronRight size={17} />
              </button>
            </div>

            <div className="support-grid">
              {requestKinds.map((item) => {
                const Icon = item.icon
                return (
                  <button
                    className="support-card"
                    data-tone={item.tone}
                    type="button"
                    key={item.id}
                    onClick={() => openRequest(item.id)}
                  >
                    <span className="support-icon"><Icon size={22} /></span>
                    <span className="support-card-copy">
                      <strong>{item.title}</strong>
                      <span>{item.description}</span>
                    </span>
                    <ChevronRight className="card-arrow" size={19} />
                  </button>
                )
              })}
            </div>
          </div>
        </section>

        <section className="workspace-section" id="workspace">
          <div className="page-width">
            <div className="section-heading split-heading workspace-title">
              <div>
                <span className="eyebrow soft"><BriefcaseBusiness size={16} /> Learner workspace</span>
                <h2>One place to understand and follow your case</h2>
              </div>
              <span className="demo-label">Synthetic learner · Reviewed demo data</span>
            </div>

            <div className="workspace-layout">
              <article className="case-card primary-case">
                <div className="case-card-top">
                  <div>
                    <span className="case-reference">CASE {activeCase.reference}</span>
                    <h3>{activeCase.title}</h3>
                    <p>{activeCase.requester_name || 'Learner'} · {activeCase.category_label}</p>
                  </div>
                  <span className="status-pill amber"><Clock3 size={14} /> {activeCase.status_label}</span>
                </div>

                <div className="route-card">
                  <div><small>Current programme</small><strong>{activeCase.source_label || 'To be reviewed'}</strong><span>{activeCase.source_location || 'Location not added'}</span></div>
                  <span className="route-arrow"><ArrowRight /></span>
                  <div><small>Destination</small><strong>{activeCase.destination_label || 'To be confirmed'}</strong><span>{activeCase.destination_location || 'Location not added'}</span></div>
                </div>

                <div className="progress-block">
                  <div className="progress-copy"><strong>Support progress</strong><span>{progressStage} of 5 stages</span></div>
                  <div className="progress-track"><span style={{ width: `${progressPercent}%` }} /></div>
                  <ol className="progress-labels">
                    <li className={stageClass(1)}>Request received</li>
                    <li className={stageClass(2)}>Evidence reviewed</li>
                    <li className={stageClass(3)}>Gap comparison</li>
                    <li className={stageClass(4)}>Support roadmap</li>
                    <li className={stageClass(5)}>Readiness review</li>
                  </ol>
                </div>

                <div className="case-actions">
                  <button className="primary-button" type="button">Continue gap review <ArrowRight size={17} /></button>
                  <button className="secondary-button" type="button"><Upload size={17} /> Add evidence</button>
                </div>
              </article>

              <aside className="workspace-side">
                <article className="side-card">
                  <div className="side-card-heading"><div><span className="mini-label">Latest activity</span><h3>Updates on your case</h3></div><MessageCircleMore size={20} /></div>
                  <div className="updates-list">
                    {updates.map((update) => {
                      const Icon = update.icon
                      return (
                        <div className="update-item" key={update.title}>
                          <span className="update-icon"><Icon size={17} /></span>
                          <div><strong>{update.title}</strong><p>{update.text}</p><small>{update.time}</small></div>
                        </div>
                      )
                    })}
                  </div>
                </article>

                <article className="side-card help-card">
                  <span className="help-icon"><UserRound size={22} /></span>
                  <div><span className="mini-label">Need help explaining it?</span><h3>Talk through your situation</h3><p>A student, parent or educator can raise the request. You can add academic evidence later.</p></div>
                  <button className="text-link" type="button" onClick={() => openRequest('unsure')}>Describe my issue <ArrowRight size={16} /></button>
                </article>
              </aside>
            </div>
          </div>
        </section>

        <section className="how-section" id="how-it-works">
          <div className="page-width how-grid">
            <div className="how-copy">
              <span className="eyebrow soft"><Sparkles size={16} /> Explainable by design</span>
              <h2>Support begins with listening, not assigning another course.</h2>
              <p>GapMap first classifies the concern. It then separates learning needs from language, documentation and institution-level decisions.</p>
              <a className="text-link" href="#workspace">See a reviewed case <ArrowRight size={16} /></a>
            </div>
            <div className="principle-grid">
              <article><BookOpenCheck size={22} /><strong>Academic need</strong><p>Diagnose only the uncertain competency.</p></article>
              <article><Languages size={22} /><strong>Language access</strong><p>Support terminology without reteaching known concepts.</p></article>
              <article><FileCheck2 size={22} /><strong>Evidence support</strong><p>Show what document or course detail is still needed.</p></article>
              <article><ShieldCheck size={22} /><strong>Human decision</strong><p>Keep admission and official equivalence with authorised institutions.</p></article>
            </div>
          </div>
        </section>
      </main>

      <footer id="resources">
        <div className="page-width footer-inner">
          <div className="brand footer-brand"><span className="brand-mark"><Network size={20} /></span><span><strong>GapMap</strong><small>Education continuity support</small></span></div>
          <p>Prototype guidance only. GapMap does not make admission, licensing or official credit-transfer decisions.</p>
          <button className="secondary-button" type="button" onClick={() => openRequest()}>Raise a request</button>
        </div>
      </footer>

      {requestOpen && (
        <div className="modal-backdrop" role="presentation" onMouseDown={() => setRequestOpen(false)}>
          <section
            className="request-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="request-title"
            onMouseDown={(event) => event.stopPropagation()}
          >
            <button className="modal-close" type="button" aria-label="Close request form" onClick={() => setRequestOpen(false)}><X size={21} /></button>
            {!submitted ? (
              <form onSubmit={submitRequest}>
                <span className="eyebrow soft"><LifeBuoy size={16} /> Learning continuity request</span>
                <h2 id="request-title">Tell us what changed.</h2>
                <p className="modal-intro">Start with the situation. Documents and detailed academic evidence can be added after the request is created.</p>

                <label className="field-label" htmlFor="request-kind">What do you need help with?</label>
                <select id="request-kind" value={selectedKind} onChange={(event) => setSelectedKind(event.target.value)}>
                  {requestKinds.map((item) => <option key={item.id} value={item.id}>{item.title}</option>)}
                </select>
                <div className="selection-help"><selectedRequest.icon size={17} /><span>{selectedRequest.description}</span></div>

                <fieldset>
                  <legend>I am raising this as a</legend>
                  <div className="choice-row">
                    {['Student', 'Parent or guardian', 'Educator or counsellor'].map((item) => (
                      <button className={role === item ? 'choice active' : 'choice'} type="button" key={item} onClick={() => setRole(item)}>{item}</button>
                    ))}
                  </div>
                </fieldset>

                <label className="field-label" htmlFor="requester-name">Your name <span>(optional)</span></label>
                <input
                  id="requester-name"
                  value={requesterName}
                  onChange={(event) => setRequesterName(event.target.value)}
                  placeholder="Name of student, parent or educator"
                />

                <div className="field-row">
                  <div>
                    <label className="field-label" htmlFor="source-label">Current school or programme</label>
                    <input id="source-label" value={sourceLabel} onChange={(event) => setSourceLabel(event.target.value)} placeholder="e.g. PCI B.Pharm" />
                  </div>
                  <div>
                    <label className="field-label" htmlFor="destination-label">Destination goal</label>
                    <input id="destination-label" value={destinationLabel} onChange={(event) => setDestinationLabel(event.target.value)} placeholder="e.g. Master of Data Science" />
                  </div>
                </div>

                <label className="field-label" htmlFor="issue-summary">Briefly describe the difficulty</label>
                <textarea
                  id="issue-summary"
                  value={summary}
                  onChange={(event) => setSummary(event.target.value)}
                  placeholder="For example: I completed B.Pharm in India and need to understand whether I am ready for a Data Science master's programme..."
                  rows={4}
                  required
                />

                <label className="upload-zone" htmlFor="evidence-upload">
                  <Upload size={20} />
                  <span><strong>Add supporting evidence later</strong><small>Transcript, syllabus, assessment or programme link</small></span>
                  <span className="optional-label">Optional</span>
                </label>
                <input className="visually-hidden" id="evidence-upload" type="file" />

                <div className="privacy-note"><ShieldCheck size={17} /><span>Prototype mode: requests are sent to the local GapMap Django API. Do not enter sensitive personal data.</span></div>
                {requestError && <p className="form-error" role="alert">{requestError}</p>}
                <button className="primary-button full-button" type="submit" disabled={submitting}>
                  {submitting ? 'Submitting…' : 'Create support request'} {!submitting && <ArrowRight size={17} />}
                </button>
              </form>
            ) : (
              <div className="success-state">
                <span className="success-icon"><Check size={28} /></span>
                <span className="eyebrow soft">Request created</span>
                <h2 id="request-title">You do not need to solve the whole problem alone.</h2>
                <p>Your request has been organised as <strong>{selectedRequest.title}</strong>. The next step is to add the source and destination details.</p>
                <div className="reference-box">
                  <span>Reference number</span>
                  <strong>{createdReference}</strong>
                  <small>{submissionMode === 'api' ? 'Stored by the GapMap API' : 'Backend unavailable · saved in local demo mode'}</small>
                </div>
                {submissionMode === 'offline' && <p className="offline-note">Start Django on port 8000 and submit again to store the request in the backend.</p>}
                <button
                  className="primary-button full-button"
                  type="button"
                  onClick={() => {
                    setRequestOpen(false)
                    setTimeout(() => document.getElementById('workspace')?.scrollIntoView({ behavior: 'smooth' }), 0)
                  }}
                >
                  Open my workspace <ArrowRight size={17} />
                </button>
              </div>
            )}
          </section>
        </div>
      )}
    </div>
  )
}

export default App
