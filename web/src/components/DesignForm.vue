<script setup lang="ts">
import { computed, reactive } from 'vue'

import type { DesignCreate } from '../types'

defineProps<{ loading: boolean }>()
const emit = defineEmits<{ submit: [data: DesignCreate] }>()

const form = reactive<DesignCreate>({
  name: 'My lattice',
  nx: 3,
  ny: 3,
  nz: 3,
  cell_size: 10,
  strut_diameter: 2,
})

const errors = computed(() => {
  const list: string[] = []
  if (form.name.trim().length === 0) list.push('Name is required')
  for (const key of ['nx', 'ny', 'nz'] as const) {
    if (!Number.isInteger(form[key]) || form[key] < 1 || form[key] > 20) {
      list.push(`${key} must be a whole number between 1 and 20`)
    }
  }
  if (!(form.cell_size > 0)) list.push('Cell size must be positive')
  if (!(form.strut_diameter > 0)) list.push('Strut diameter must be positive')
  return list
})

const nodeCount = computed(() => (form.nx + 1) * (form.ny + 1) * (form.nz + 1))
const strutCount = computed(
  () =>
    form.nx * (form.ny + 1) * (form.nz + 1) +
    (form.nx + 1) * form.ny * (form.nz + 1) +
    (form.nx + 1) * (form.ny + 1) * form.nz,
)

function onSubmit() {
  if (errors.value.length === 0) emit('submit', { ...form })
}
</script>

<template>
  <form class="design-form" @submit.prevent="onSubmit">
    <label>Name <input v-model="form.name" type="text" maxlength="100" /></label>
    <label>Cells in x <input v-model.number="form.nx" type="number" min="1" max="20" /></label>
    <label>Cells in y <input v-model.number="form.ny" type="number" min="1" max="20" /></label>
    <label>Cells in z <input v-model.number="form.nz" type="number" min="1" max="20" /></label>
    <label>Cell size <input v-model.number="form.cell_size" type="number" step="any" /></label>
    <label>
      Strut diameter
      <input v-model.number="form.strut_diameter" type="number" step="any" />
    </label>

    <p class="summary">Preview: {{ nodeCount }} nodes, {{ strutCount }} struts</p>
    <ul v-if="errors.length" class="errors">
      <li v-for="message in errors" :key="message">{{ message }}</li>
    </ul>

    <button type="submit" :disabled="loading || errors.length > 0">Generate and save</button>
  </form>
</template>

<style scoped>
.design-form {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px 24px;
  padding: 16px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 14px;
}

input {
  padding: 6px 8px;
  border: 1px solid #9ca3af;
  border-radius: 6px;
}

.summary,
.errors,
button {
  grid-column: 1 / -1;
}

.summary {
  margin: 0;
  color: #4b5563;
}

.errors {
  margin: 0;
  padding-left: 18px;
  color: #b91c1c;
}
</style>