import { useEffect, useRef, useState } from 'react'
import { Box, Rotate3D, X } from 'lucide-react'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

import { getEmbeddingMap, type EmbeddingMapPoint, type EmbeddingMapResponse } from './api'
import './EmbeddingMap.css'

const palette: Record<string, number> = {
  learner_evidence: 0x151515,
  destination_requirement: 0x78a91f,
  transition_context: 0x64748b,
}

const colorFor = (section: string) => palette[section.toLowerCase().replace(/\s+/g, '_')] ?? 0x9a6bdb

export function EmbeddingMap({ open, onClose }: { open: boolean; onClose: () => void }) {
  const mountRef = useRef<HTMLDivElement>(null)
  const [data, setData] = useState<EmbeddingMapResponse | null>(null)
  const [selected, setSelected] = useState<EmbeddingMapPoint | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!open || data) return
    getEmbeddingMap().then(setData).catch((reason: unknown) => {
      setError(reason instanceof Error ? reason.message : 'The embedding map could not be loaded.')
    })
  }, [open, data])

  useEffect(() => {
    if (!open) return
    const closeOnEscape = (event: KeyboardEvent) => event.key === 'Escape' && onClose()
    window.addEventListener('keydown', closeOnEscape)
    return () => window.removeEventListener('keydown', closeOnEscape)
  }, [open, onClose])

  useEffect(() => {
    const mount = mountRef.current
    if (!open || !mount || !data?.points.length) return

    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0xf7f8f4)
    scene.fog = new THREE.FogExp2(0xf7f8f4, 0.027)
    const camera = new THREE.PerspectiveCamera(48, 1, 0.1, 100)
    camera.position.set(12, 9, 16)
    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    mount.appendChild(renderer.domElement)

    const controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    controls.autoRotate = !window.matchMedia('(prefers-reduced-motion: reduce)').matches
    controls.autoRotateSpeed = 0.35
    controls.minDistance = 5
    controls.maxDistance = 34

    const geometry = new THREE.BufferGeometry()
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(data.points.flatMap((p) => [p.x, p.y, p.z]), 3))
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(data.points.flatMap((p) => {
      const color = new THREE.Color(colorFor(p.section))
      return [color.r, color.g, color.b]
    }), 3))
    const material = new THREE.PointsMaterial({ size: 0.24, vertexColors: true, sizeAttenuation: true })
    const cloud = new THREE.Points(geometry, material)
    scene.add(cloud)

    const groups = new Map<string, EmbeddingMapPoint[]>()
    data.points.forEach((point) => {
      const key = point.scenario?.scenario_id
      if (key) groups.set(key, [...(groups.get(key) ?? []), point])
    })
    const linePositions: number[] = []
    groups.forEach((points) => points.slice(1).forEach((point) => {
      const anchor = points[0]
      linePositions.push(anchor.x, anchor.y, anchor.z, point.x, point.y, point.z)
    }))
    const lineGeometry = new THREE.BufferGeometry()
    lineGeometry.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3))
    const lineMaterial = new THREE.LineBasicMaterial({ color: 0xcbd0c5, transparent: true, opacity: 0.28 })
    scene.add(new THREE.LineSegments(lineGeometry, lineMaterial))
    scene.add(new THREE.GridHelper(22, 22, 0xb8bcb3, 0xe1e3dd))

    const raycaster = new THREE.Raycaster()
    raycaster.params.Points.threshold = 0.28
    const pointer = new THREE.Vector2()
    const selectPoint = (event: PointerEvent) => {
      const rect = renderer.domElement.getBoundingClientRect()
      pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1
      pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1
      raycaster.setFromCamera(pointer, camera)
      const hit = raycaster.intersectObject(cloud)[0]
      renderer.domElement.style.cursor = hit ? 'pointer' : 'grab'
      if (event.type === 'click' && hit?.index !== undefined) setSelected(data.points[hit.index])
    }
    renderer.domElement.addEventListener('pointermove', selectPoint)
    renderer.domElement.addEventListener('click', selectPoint)

    const resize = () => {
      const { clientWidth, clientHeight } = mount
      renderer.setSize(clientWidth, clientHeight, false)
      camera.aspect = clientWidth / Math.max(clientHeight, 1)
      camera.updateProjectionMatrix()
    }
    const observer = new ResizeObserver(resize)
    observer.observe(mount)
    resize()
    let frame = 0
    const animate = () => { controls.update(); renderer.render(scene, camera); frame = requestAnimationFrame(animate) }
    animate()

    return () => {
      cancelAnimationFrame(frame)
      observer.disconnect()
      renderer.domElement.removeEventListener('pointermove', selectPoint)
      renderer.domElement.removeEventListener('click', selectPoint)
      controls.dispose(); geometry.dispose(); material.dispose(); lineGeometry.dispose(); lineMaterial.dispose(); renderer.dispose()
      renderer.domElement.remove()
    }
  }, [open, data])

  if (!open) return null
  return (
    <div className="embedding-overlay" role="dialog" aria-modal="true" aria-labelledby="embedding-title">
      <header className="embedding-header">
        <div><span className="embedding-kicker"><Box size={14} /> Evidence space / 3D projection</span><h2 id="embedding-title">How the evidence library is organised.</h2></div>
        <button type="button" onClick={onClose} aria-label="Close embedding map"><X size={22} /></button>
      </header>
      <div className="embedding-stage">
        <div className="embedding-canvas" ref={mountRef}>
          {!data && !error && <div className="embedding-loading"><Rotate3D size={24} /> Projecting approved evidence…</div>}
          {error && <div className="embedding-loading error">{error}</div>}
        </div>
        <aside className="embedding-inspector">
          <p className="mono-label">MAP READING</p>
          <p>Nearby points have similar semantic meaning. Lines connect evidence from the same transition scenario.</p>
          <div className="embedding-legend"><span><i className="learner" /> Learner evidence</span><span><i className="requirement" /> Requirements</span><span><i className="context" /> Transition context</span><span><i className="other" /> Other evidence</span></div>
          <dl><div><dt>Approved points</dt><dd>{data?.count ?? '—'}</dd></div><div><dt>Original dimensions</dt><dd>{data?.source_dimensions ?? '—'}</dd></div><div><dt>Projection</dt><dd>PCA / SVD → 3D</dd></div></dl>
          <div className="point-card">
            <p className="mono-label">{selected ? 'SELECTED POINT' : 'EXPLORE'}</p>
            {selected ? <><h3>{selected.scenario?.title ?? 'General evidence'}</h3><p>{selected.section || 'Evidence'} · {selected.scenario?.rarity ?? 'standard'}</p><small>{selected.chunk_id} · {selected.review_status}</small></> : <p>Drag to rotate, scroll to zoom, and select a point to inspect its scenario.</p>}
          </div>
          <small className="projection-note">Positions are similarity coordinates, not grades, eligibility scores, or confidence. Raw vectors remain on the server.</small>
        </aside>
      </div>
    </div>
  )
}