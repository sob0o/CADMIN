<script setup lang="ts">
import * as THREE from 'three'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

import type { NodeOut, StrutOut } from '../types'

const props = defineProps<{ nodes: NodeOut[]; struts: StrutOut[] }>()
const container = ref<HTMLDivElement | null>(null)
const spinning = ref(true)

const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 5000)
camera.up.set(0, 0, 1)
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
renderer.setPixelRatio(window.devicePixelRatio)
renderer.setClearColor(0x000000, 0)
const controls = new OrbitControls(camera, renderer.domElement)
controls.enableDamping = true
controls.autoRotate = true
controls.autoRotateSpeed = 1.2

const COLOR_LOW = new THREE.Color(0x22d3ee)
const COLOR_HIGH = new THREE.Color(0x8b5cf6)

let lattice: THREE.Group | null = null
let frameId = 0
let observer: ResizeObserver | null = null

function clearLattice() {
  if (!lattice) return
  scene.remove(lattice)
  lattice.traverse((obj) => {
    if (obj instanceof THREE.LineSegments || obj instanceof THREE.Points) {
      obj.geometry.dispose()
      ;(obj.material as THREE.Material).dispose()
    }
  })
  lattice = null
}

function buildLattice() {
  clearLattice()
  if (props.struts.length === 0) return

  const byId = new Map(props.nodes.map((n) => [n.id, n]))
  const zs = props.nodes.map((n) => n.z)
  const zMin = Math.min(...zs)
  const zRange = Math.max(...zs) - zMin || 1

  const positions = new Float32Array(props.struts.length * 6)
  const colors = new Float32Array(props.struts.length * 6)
  const tmp = new THREE.Color()

  props.struts.forEach((strut, i) => {
    const a = byId.get(strut.start_node_id)!
    const b = byId.get(strut.end_node_id)!
    positions.set([a.x, a.y, a.z, b.x, b.y, b.z], i * 6)
    tmp.lerpColors(COLOR_LOW, COLOR_HIGH, (a.z - zMin) / zRange)
    colors.set([tmp.r, tmp.g, tmp.b], i * 6)
    tmp.lerpColors(COLOR_LOW, COLOR_HIGH, (b.z - zMin) / zRange)
    colors.set([tmp.r, tmp.g, tmp.b], i * 6 + 3)
  })

  const lineGeometry = new THREE.BufferGeometry()
  lineGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  lineGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))
  lineGeometry.computeBoundingBox()
  const box = lineGeometry.boundingBox!
  const center = box.getCenter(new THREE.Vector3())
  const size = box.getSize(new THREE.Vector3()).length()

  const pointPositions = new Float32Array(props.nodes.length * 3)
  props.nodes.forEach((n, i) => pointPositions.set([n.x, n.y, n.z], i * 3))
  const pointGeometry = new THREE.BufferGeometry()
  pointGeometry.setAttribute('position', new THREE.BufferAttribute(pointPositions, 3))

  lattice = new THREE.Group()
  lattice.add(
    new THREE.LineSegments(
      lineGeometry,
      new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.9 }),
    ),
    new THREE.Points(
      pointGeometry,
      new THREE.PointsMaterial({
        color: 0xffffff,
        size: size * 0.012,
        transparent: true,
        opacity: 0.85,
      }),
    ),
  )
  lattice.position.sub(center)
  scene.add(lattice)

  camera.position.set(size, -size, size * 0.8)
  controls.target.set(0, 0, 0)
  controls.update()
}

function resize() {
  const el = container.value
  if (!el) return
  renderer.setSize(el.clientWidth, el.clientHeight)
  camera.aspect = el.clientWidth / el.clientHeight
  camera.updateProjectionMatrix()
}

function animate() {
  frameId = requestAnimationFrame(animate)
  controls.update()
  renderer.render(scene, camera)
}

onMounted(() => {
  container.value!.appendChild(renderer.domElement)
  observer = new ResizeObserver(resize)
  observer.observe(container.value!)
  resize()
  buildLattice()
  animate()
})

watch(() => [props.nodes, props.struts], buildLattice)
watch(spinning, (value) => {
  controls.autoRotate = value
})

onBeforeUnmount(() => {
  cancelAnimationFrame(frameId)
  observer?.disconnect()
  controls.dispose()
  clearLattice()
  renderer.dispose()
  renderer.domElement.remove()
})
</script>

<template>
  <div class="wrap">
    <div ref="container" class="viewer"></div>
    <button class="overlay" @click="spinning = !spinning">
      {{ spinning ? 'Pause rotation' : 'Auto-rotate' }}
    </button>
    <span class="hint">Drag to rotate · Scroll to zoom · Right-drag to pan</span>
  </div>
</template>

<style scoped>
.wrap {
  position: relative;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  background: radial-gradient(circle at 50% 40%, #17213d 0%, #0b0f1a 75%);
}

.viewer {
  width: 100%;
  height: 560px;
}

.overlay {
  position: absolute;
  top: 14px;
  right: 14px;
  font-size: 13px;
  backdrop-filter: blur(8px);
  background: rgba(11, 15, 26, 0.6);
}

.hint {
  position: absolute;
  left: 16px;
  bottom: 12px;
  font-size: 12px;
  color: var(--muted);
  pointer-events: none;
}
</style>