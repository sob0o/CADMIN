<script setup lang="ts">
import { onMounted } from 'vue'


import DesignForm from './components/DesignForm.vue'
import { useDesignsStore } from './stores/designs'
import LatticeViewer from './components/LatticeViewer.vue'

const store = useDesignsStore()

onMounted(store.fetchDesigns)
</script>

<template>
  <h1>CADMIN - Lattice Design Suite</h1>

  <DesignForm :loading="store.loading" @submit="store.createDesign" />
  <p v-if="store.loading">Loading...</p>
  <p v-if="store.error" style="color: #b91c1c">Error: {{ store.error }}</p>

  <h2>Saved designs</h2>
  <p v-if="store.designs.length === 0">No design yet.</p>
  <ul>
    <li v-for="design in store.designs" :key="design.id">
      <button @click="store.selectDesign(design.id)">
        #{{ design.id }} {{ design.name }} ({{ design.nx }}x{{ design.ny }}x{{ design.nz }})
      </button>
    </li>
  </ul>

  <section v-if="store.current">
    <h2>{{ store.current.name }}</h2>
    <p>{{ store.current.nodes.length }} nodes, {{ store.current.struts.length }} struts</p>
    <LatticeViewer :nodes="store.current.nodes" :struts="store.current.struts" />
  </section>
</template>