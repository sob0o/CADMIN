export interface DesignCreate {
  name: string
  nx: number
  ny: number
  nz: number
  cell_size: number
  strut_diameter: number
}

export interface NodeOut {
  id: number
  x: number
  y: number
  z: number
}

export interface StrutOut {
  id: number
  start_node_id: number
  end_node_id: number
  diameter: number
}

export interface DesignSummary extends DesignCreate {
  id: number
  created_at: string
}

export interface DesignDetail extends DesignSummary {
  nodes: NodeOut[]
  struts: StrutOut[]
}