<script setup lang="ts">
import { computed, onMounted } from 'vue'

import DesignForm from './components/DesignForm.vue'
import LatticeViewer from './components/LatticeViewer.vue'
import { useDesignsStore } from './stores/designs'

const store = useDesignsStore()

onMounted(store.fetchDesigns)

const cards = computed(() => {
  const s = store.stats
  if (!s) return []
  return [
    { label: 'Nodes', value: s.node_count.toLocaleString(), unit: '' },
    { label: 'Struts', value: s.strut_count.toLocaleString(), unit: '' },
    { label: 'Total length', value: (s.total_length_mm / 1000).toFixed(2), unit: 'm' },
    { label: 'Volume', value: (s.volume_mm3 / 1000).toFixed(1), unit: 'cm³' },
    { label: 'Mass', value: s.mass_g.toFixed(1), unit: 'g' },
    {
      label: 'Bounding box',
      value: s.bounding_box_mm.map((v) => v.toFixed(0)).join(' × '),
      unit: 'mm',
    },
  ]
})
</script>

<template>
  <div class="shell">
    <header class="topbar">
      <div class="brand">
        <span class="logo">◆</span>
        <strong>CADMIN</strong>
        <span class="tag">Lattice Design Suite</span>
      </div>
      <span v-if="store.loading" class="pill">Working…</span>
    </header>

    <main class="layout">
      <aside class="sidebar">
        <section class="card">
          <h2>New design</h2>
          <DesignForm :loading="store.loading" @submit="store.createDesign" />
        </section>

        <section class="card">
          <h2>Saved designs</h2>
          <p v-if="store.designs.length === 0" class="muted">No design yet.</p>
          <ul class="design-list">
            <li v-for="design in store.designs" :key="design.id">
              <button
                class="design-item"
                :class="{ active: store.current?.id === design.id }"
                @click="store.selectDesign(design.id)"
              >
                <span class="design-name">{{ design.name }}</span>
                <span class="design-dims">{{ design.nx }}×{{ design.ny }}×{{ design.nz }}</span>
              </button>
            </li>
          </ul>
        </section>
      </aside>

      <section class="main">
        <p v-if="store.error" class="alert">Error: {{ store.error }}</p>

        <template v-if="store.current">
          <div class="title-row">
            <h1>{{ store.current.name }}</h1>
            <span class="muted">
              #{{ store.current.id }} · {{ store.current.nx }}×{{ store.current.ny }}×{{
                store.current.nz
              }}
              cells · cell {{ store.current.cell_size }} mm
            </span>
          </div>

          <div class="stats">
            <div v-for="card in cards" :key="card.label" class="stat">
              <span class="stat-label">{{ card.label }}</span>
              <span class="stat-value">
                {{ card.value }}<small v-if="card.unit"> {{ card.unit }}</small>
              </span>
            </div>
          </div>

          <LatticeViewer :nodes="store.current.nodes" :struts="store.current.struts" />
        </template>

        <div v-else class="empty">
          <span class="empty-icon">◆</span>
          <h2>No lattice selected</h2>
          <p class="muted">Generate a new design or pick one from the list.</p>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.shell {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px 24px 40px;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
}

.logo {
  font-size: 20px;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.tag {
  padding: 3px 10px;
  font-size: 12px;
  color: var(--muted);
  border: 1px solid var(--border);
  border-radius: 999px;
}

.pill {
  padding: 4px 12px;
  font-size: 13px;
  color: var(--accent);
  border: 1px solid rgba(34, 211, 238, 0.35);
  border-radius: 999px;
  animation: pulse 1.2s ease-in-out infinite;
}

@keyframes pulse {
  50% {
    opacity: 0.45;
  }
}

.layout {
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: 20px;
  align-items: start;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card {
  padding: 18px;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  backdrop-filter: blur(10px);
}

.card h2 {
  margin-bottom: 14px;
  font-size: 15px;
}

.muted {
  color: var(--muted);
  font-size: 14px;
}

.design-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: 320px;
  overflow-y: auto;
}

.design-item {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: space-between;
  text-align: left;
}

.design-item.active {
  border-color: rgba(34, 211, 238, 0.6);
  background: rgba(34, 211, 238, 0.1);
}

.design-dims {
  font-size: 12px;
  color: var(--muted);
}

.main {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
}

.title-row {
  display: flex;
  align-items: baseline;
  gap: 14px;
  flex-wrap: wrap;
}

.title-row h1 {
  font-size: 26px;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 14px 16px;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.stat-label {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
}

.stat-value {
  font-size: 20px;
  font-weight: 650;
}

.stat-value small {
  font-size: 13px;
  font-weight: 400;
  color: var(--muted);
}

.alert {
  margin: 0;
  padding: 10px 14px;
  color: var(--danger);
  background: rgba(248, 113, 113, 0.1);
  border: 1px solid rgba(248, 113, 113, 0.35);
  border-radius: 10px;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 90px 20px;
  text-align: center;
  background: var(--panel);
  border: 1px dashed var(--border);
  border-radius: var(--radius);
}

.empty-icon {
  font-size: 40px;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

@media (max-width: 900px) {
  .layout {
    grid-template-columns: 1fr;
  }
}
</style>