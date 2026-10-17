import { defineStore } from 'pinia'
import { ref } from 'vue'

import { api } from '../api'
import type { DesignCreate, DesignDetail, DesignSummary } from '../types'

export const useDesignsStore = defineStore('designs', () => {
  const designs = ref<DesignSummary[]>([])
  const current = ref<DesignDetail | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function run(action: () => Promise<void>) {
    loading.value = true
    error.value = null
    try {
      await action()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Unknown error'
    } finally {
      loading.value = false
    }
  }

  const fetchDesigns = () =>
    run(async () => {
      designs.value = await api.listDesigns()
    })

  const selectDesign = (id: number) =>
    run(async () => {
      current.value = await api.getDesign(id)
    })

  const createDesign = (data: DesignCreate) =>
    run(async () => {
      current.value = await api.createDesign(data)
      designs.value = await api.listDesigns()
    })

  return { designs, current, loading, error, fetchDesigns, selectDesign, createDesign }
})