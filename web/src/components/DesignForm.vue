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
    <label class="full">
      Name
      <input v-model="form.name" type="text" maxlength="100" />
    </label>
    <label>
      Cells X
      <input v-model.number="form.nx" type="number" min="1" max="20" />
    </label>
    <label>
      Cells Y
      <input v-model.number="form.ny" type="number" min="1" max="20" />
    </label>
    <label>
      Cells Z
      <input v-model.number="form.nz" type="number" min="1" max="20" />
    </label>
    <label>
      Cell size (mm)
      <input v-model.number="form.cell_size" type="number" step="any" />
    </label>
    <label class="full">
      Strut diameter (mm)
      <input v-model.number="form.strut_diameter" type="number" step="any" />
    </label>

    <p class="preview">
      <span>{{ nodeCount.toLocaleString() }} nodes</span>
      <span>{{ strutCount.toLocaleString() }} struts</span>
    </p>
    <ul v-if="errors.length" class="errors">
      <li v-for="message in errors" :key="message">{{ message }}</li>
    </ul>

    <button class="primary full" type="submit" :disabled="loading || errors.length > 0">
      Generate and save
    </button>
  </form>
</template>

<style scoped>
.design-form {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.full,
.preview,
.errors {
  grid-column: 1 / -1;
}

label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 12px;
  color: var(--muted);
}

input {
  width: 100%;
  padding: 9px 10px;
  font: inherit;
  font-size: 14px;
  color: var(--text);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border);
  border-radius: 10px;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}

input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.18);
}

.preview {
  display: flex;
  gap: 8px;
  margin: 0;
}

.preview span {
  padding: 3px 10px;
  font-size: 12px;
  color: var(--accent);
  background: rgba(34, 211, 238, 0.08);
  border: 1px solid rgba(34, 211, 238, 0.25);
  border-radius: 999px;
}

.errors {
  margin: 0;
  padding-left: 18px;
  font-size: 13px;
  color: var(--danger);
}
</style>