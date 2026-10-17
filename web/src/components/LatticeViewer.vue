<script setup lang="ts">
import * as THREE from 'three'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

import type { NodeOut, StrutOut } from '../types'

const props = defineProps<{ nodes: NodeOut[]; struts: StrutOut[] }>()
const container = ref<HTMLDivElement | null>(null)

const scene = new THREE.Scene()
scene.background = new THREE.Color(0xffffff)
const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 5000)
camera.up.set(0, 0, 1)
const renderer = new THREE.WebGLRenderer({ antialias: true })
renderer.setPixelRatio(window.devicePixelRatio)
const controls = new OrbitControls(camera, renderer.domElement)
controls.enableDamping = true

let lattice: THREE.LineSegments | null = null
let frameId = 0
let observer: ResizeObserver | null = null

function clearLattice() {
  if (!lattice) return
  scene.remove(lattice)
  lattice.geometry.dispose()
  ;(lattice.material as THREE.Material).dispose()
  lattice = null
}

function buildLattice() {
  clearLattice()
  if (props.struts.length === 0) return

  const byId = new Map(props.nodes.map((n) => [n.id, n]))
  const positions = new Float32Array(props.struts.length * 6)
  props.struts.forEach((strut, i) => {
    const a = byId.get(strut.start_node_id)!
    const b = byId.get(strut.end_node_id)!
    positions.set([a.x, a.y, a.z, b.x, b.y, b.z], i * 6)
  })

  const geometry = new THREE.BufferGeometry()
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.computeBoundingBox()
  const box = geometry.boundingBox!
  const center = box.getCenter(new THREE.Vector3())
  const size = box.getSize(new THREE.Vector3()).length()

  lattice = new THREE.LineSegments(geometry, new THREE.LineBasicMaterial({ color: 0x2563eb }))
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
  <div ref="container" class="viewer"></div>
</template>

<style scoped>
.viewer {
  width: 100%;
  height: 480px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}
</style>