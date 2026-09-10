import { ArrowRight, BookOpenCheck, Network } from 'lucide-react'

const steps = [
  ['01', 'Compare curricula'],
  ['02', 'Run adaptive diagnostic'],
  ['03', 'Locate prerequisite gaps'],
  ['04', 'Build minimum bridge path'],
  ['05', 'Reassess readiness'],
]

function App() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-950">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <a className="flex items-center gap-3" href="#top" aria-label="GapMap home">
            <span className="grid size-10 place-items-center rounded-xl bg-blue-700 text-white">
              <Network size={21} />
            </span>
            <span>
              <strong className="block text-lg">GapMap</strong>
              <span className="block text-xs text-slate-500">Learning recovery workspace</span>
            </span>
          </a>
          <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-bold text-blue-800 ring-1 ring-blue-200">
            SIH prototype
          </span>
        </div>
      </header>

      <main id="top">
        <section className="mx-auto grid max-w-7xl gap-12 px-6 py-16 lg:grid-cols-2 lg:items-center lg:py-24">
          <div>
            <p className="mb-5 inline-flex items-center gap-2 rounded-full bg-teal-50 px-3 py-1 text-sm font-semibold text-teal-800 ring-1 ring-teal-200">
              <BookOpenCheck size={16} /> Curriculum transition support
            </p>
            <h1 className="text-4xl font-black tracking-[-0.04em] sm:text-6xl">
              Find the prerequisite, not just the wrong answer.
            </h1>
            <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-600">
              GapMap compares curricula, runs a short adaptive diagnostic and builds the minimum teacher-reviewed path back to classroom readiness.
            </p>
            <div className="mt-9 flex flex-wrap gap-3">
              <button className="inline-flex items-center gap-2 rounded-xl bg-blue-700 px-5 py-3 font-bold text-white shadow-lg shadow-blue-700/20 hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-200" type="button">
                Start diagnostic <ArrowRight size={18} />
              </button>
              <button className="rounded-xl border border-slate-300 bg-white px-5 py-3 font-bold text-slate-800 hover:border-blue-300 hover:text-blue-800 focus:outline-none focus:ring-4 focus:ring-slate-200" type="button">
                Teacher workspace
              </button>
            </div>
            <p className="mt-4 text-sm text-slate-500">Prototype scope: Class 8 to 9 mathematics, English and Hindi</p>
          </div>

          <div className="rounded-[2rem] border border-slate-200 bg-white p-7 shadow-2xl shadow-slate-300/40">
            <p className="text-sm font-bold uppercase tracking-[0.15em] text-blue-700">Sample gap map</p>
            <h2 className="mt-2 text-2xl font-extrabold">Linear equations</h2>
            <div className="mt-7 space-y-3">
              <div className="concept mastered"><span>Integer operations</span><strong>Mastered</strong></div>
              <div className="concept gap"><span>Negative numbers</span><strong>Root gap</strong></div>
              <div className="concept language"><span>Algebra vocabulary</span><strong>Language evidence</strong></div>
              <div className="concept target"><span>Linear equations</span><strong>Destination</strong></div>
            </div>
          </div>
        </section>

        <section className="border-y border-slate-200 bg-white py-14">
          <div className="mx-auto max-w-7xl px-6">
            <p className="text-sm font-bold uppercase tracking-[0.15em] text-blue-700">Recovery workflow</p>
            <h2 className="mt-2 text-3xl font-black tracking-tight">A focused path to the current classroom</h2>
            <ol className="mt-9 grid gap-4 md:grid-cols-5">
              {steps.map(([number, label]) => (
                <li className="rounded-2xl border border-slate-200 bg-slate-50 p-5" key={number}>
                  <span className="text-sm font-black text-blue-700">{number}</span>
                  <h3 className="mt-4 font-extrabold">{label}</h3>
                </li>
              ))}
            </ol>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
