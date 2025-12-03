// BST Node class
class Node {
  constructor(value) {
    this.value = value
    this.left = null
    this.right = null
    this.x = 0
    this.y = 0
    this.element = null
  }
}

// Binary Search Tree class
class BinarySearchTree {
  constructor() {
    this.root = null
  }

  insert(value) {
    const newNode = new Node(value)
    if (this.root === null) {
      this.root = newNode
      return newNode
    } else {
      return this.insertNode(this.root, newNode)
    }
  }

  insertNode(node, newNode) {
    if (newNode.value < node.value) {
      if (node.left === null) {
        node.left = newNode
        return newNode
      } else {
        return this.insertNode(node.left, newNode)
      }
    } else {
      if (node.right === null) {
        node.right = newNode
        return newNode
      } else {
        return this.insertNode(node.right, newNode)
      }
    }
  }

  search(value, node = this.root) {
    if (node === null) {
      return null
    }

    if (value < node.value) {
      return this.search(value, node.left)
    } else if (value > node.value) {
      return this.search(value, node.right)
    } else {
      return node
    }
  }

  delete(value) {
    this.root = this.deleteNode(this.root, value)
  }

  deleteNode(node, value) {
    if (node === null) {
      return null
    }

    if (value < node.value) {
      node.left = this.deleteNode(node.left, value)
      return node
    } else if (value > node.value) {
      node.right = this.deleteNode(node.right, value)
      return node
    } else {
      // Node to be deleted found
      if (node.left === null && node.right === null) {
        return null
      }

      if (node.left === null) {
        return node.right
      }

      if (node.right === null) {
        return node.left
      }

      // Node has two children
      const minRight = this.findMinNode(node.right)
      node.value = minRight.value
      node.right = this.deleteNode(node.right, minRight.value)
      return node
    }
  }

  findMinNode(node) {
    while (node.left !== null) {
      node = node.left
    }
    return node
  }

  getHeight(node = this.root) {
    if (node === null) {
      return 0
    }
    return 1 + Math.max(this.getHeight(node.left), this.getHeight(node.right))
  }

  getNodeCount(node = this.root) {
    if (node === null) {
      return 0
    }
    return 1 + this.getNodeCount(node.left) + this.getNodeCount(node.right)
  }

  getMinValue(node = this.root) {
    if (node === null) {
      return null
    }
    while (node.left !== null) {
      node = node.left
    }
    return node.value
  }

  getMaxValue(node = this.root) {
    if (node === null) {
      return null
    }
    while (node.right !== null) {
      node = node.right
    }
    return node.value
  }

  inorderTraversal(node = this.root, result = []) {
    if (node !== null) {
      this.inorderTraversal(node.left, result)
      result.push(node.value)
      this.inorderTraversal(node.right, result)
    }
    return result
  }

  preorderTraversal(node = this.root, result = []) {
    if (node !== null) {
      result.push(node.value)
      this.preorderTraversal(node.left, result)
      this.preorderTraversal(node.right, result)
    }
    return result
  }

  postorderTraversal(node = this.root, result = []) {
    if (node !== null) {
      this.postorderTraversal(node.left, result)
      this.postorderTraversal(node.right, result)
      result.push(node.value)
    }
    return result
  }

  clear() {
    this.root = null
  }
}

// Tree Visualizer class
class TreeVisualizer {
  constructor() {
    this.bst = new BinarySearchTree()
    this.svg = document.getElementById('treeSvg')
    this.animationSpeed = 800
    this.animationsEnabled = true
    this.showValues = true
    this.highlightedNodes = []
    this.searchPath = []

    this.initializeElements()
    this.setupEventListeners()
    this.updateStatistics()
    this.drawTree()
  }

  initializeElements() {
    // Input elements
    this.nodeInput = document.getElementById('nodeInput')
    this.searchInput = document.getElementById('searchInput')

    // Buttons
    this.addBtn = document.getElementById('addBtn')
    this.randomBtn = document.getElementById('randomBtn')
    this.searchBtn = document.getElementById('searchBtn')
    this.deleteBtn = document.getElementById('deleteBtn')
    this.clearBtn = document.getElementById('clearBtn')
    this.balanceBtn = document.getElementById('balanceBtn')
    this.exportBtn = document.getElementById('exportBtn')

    // Traversal buttons
    this.inorderBtn = document.getElementById('inorderBtn')
    this.preorderBtn = document.getElementById('preorderBtn')
    this.postorderBtn = document.getElementById('postorderBtn')

    // Settings
    this.animationToggle = document.getElementById('animationToggle')
    this.showValuesToggle = document.getElementById('showValuesToggle')
    this.speedSlider = document.getElementById('speedSlider')
    this.speedValue = document.getElementById('speedValue')

    // Display elements
    this.nodeCount = document.getElementById('nodeCount')
    this.treeHeight = document.getElementById('treeHeight')
    this.minValue = document.getElementById('minValue')
    this.maxValue = document.getElementById('maxValue')
    this.traversalResult = document.getElementById('traversalResult')
    this.history = document.getElementById('history')

    // Modal
    this.modal = document.getElementById('nodeModal')
    this.closeModal = document.querySelector('.close')
    this.nodeDetails = document.getElementById('nodeDetails')
  }

  setupEventListeners() {
    // Add node
    this.addBtn.addEventListener('click', () => this.addNode())
    this.nodeInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.addNode()
    })

    // Random node
    this.randomBtn.addEventListener('click', () => this.addRandomNode())

    // Search
    this.searchBtn.addEventListener('click', () => this.searchNode())
    this.searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.searchNode()
    })

    // Delete
    this.deleteBtn.addEventListener('click', () => this.deleteNode())

    // Tree operations
    this.clearBtn.addEventListener('click', () => this.clearTree())
    this.balanceBtn.addEventListener('click', () => this.balanceTree())
    this.exportBtn.addEventListener('click', () => this.exportTree())

    // Traversals
    this.inorderBtn.addEventListener('click', () =>
      this.performTraversal('inorder'),
    )
    this.preorderBtn.addEventListener('click', () =>
      this.performTraversal('preorder'),
    )
    this.postorderBtn.addEventListener('click', () =>
      this.performTraversal('postorder'),
    )

    // Settings
    this.animationToggle.addEventListener('change', (e) => {
      this.animationsEnabled = e.target.checked
    })

    this.showValuesToggle.addEventListener('change', (e) => {
      this.showValues = e.target.checked
      this.drawTree()
    })

    this.speedSlider.addEventListener('input', (e) => {
      this.animationSpeed = parseInt(e.target.value)
      this.speedValue.textContent = `${this.animationSpeed}ms`
    })

    // Modal
    this.closeModal.addEventListener('click', () => this.closeModalWindow())

    window.addEventListener('click', (e) => {
      if (e.target === this.modal) {
        this.closeModalWindow()
      }
    })
  }

  addNode() {
    const value = parseInt(this.nodeInput.value)
    if (isNaN(value)) {
      this.showMessage('Будь ласка, введіть число', 'warning')
      return
    }

    const existingNode = this.bst.search(value)
    if (existingNode) {
      this.showMessage(`Вузол зі значенням ${value} вже існує`, 'warning')
      return
    }

    const newNode = this.bst.insert(value)
    this.addToHistory(`Додано вузол: ${value}`, 'add')

    if (this.animationsEnabled) {
      this.animateInsertion(newNode).then(() => {
        this.updateStatistics()
        this.drawTree()
      })
    } else {
      this.updateStatistics()
      this.drawTree()
    }

    this.nodeInput.value = ''
    this.nodeInput.focus()
  }

  addRandomNode() {
    const value = Math.floor(Math.random() * 200) - 100 // Random between -100 and 100
    this.nodeInput.value = value
    this.addNode()
  }

  async searchNode() {
    const value = parseInt(this.searchInput.value)
    if (isNaN(value)) {
      this.showMessage('Будь ласка, введіть число для пошуку', 'warning')
      return
    }

    this.clearHighlights()
    const foundNode = this.bst.search(value)

    if (foundNode) {
      this.addToHistory(`Знайдено вузол: ${value}`, 'search')
      if (this.animationsEnabled) {
        await this.animateSearch(value)
      } else {
        this.highlightNode(foundNode, 'found')
      }
      this.showMessage(`Вузол ${value} знайдено!`, 'success')
    } else {
      this.addToHistory(`Не знайдено вузол: ${value}`, 'search')
      this.showMessage(`Вузол ${value} не знайдено`, 'error')
    }

    this.searchInput.value = ''
  }

  deleteNode() {
    const value = parseInt(this.searchInput.value)
    if (isNaN(value)) {
      this.showMessage('Будь ласка, введіть число для видалення', 'warning')
      return
    }

    const existingNode = this.bst.search(value)
    if (!existingNode) {
      this.showMessage(`Вузол ${value} не знайдено`, 'error')
      return
    }

    if (this.animationsEnabled) {
      this.animateDeletion(existingNode).then(() => {
        this.bst.delete(value)
        this.addToHistory(`Видалено вузол: ${value}`, 'delete')
        this.updateStatistics()
        this.drawTree()
      })
    } else {
      this.bst.delete(value)
      this.addToHistory(`Видалено вузол: ${value}`, 'delete')
      this.updateStatistics()
      this.drawTree()
    }

    this.searchInput.value = ''
  }

  clearTree() {
    if (this.bst.getNodeCount() === 0) {
      this.showMessage('Дерево вже порожнє', 'info')
      return
    }

    this.bst.clear()
    this.clearHighlights()
    this.addToHistory('Дерево очищено', 'delete')
    this.updateStatistics()
    this.drawTree()
    this.showMessage('Дерево очищено', 'success')
  }

  balanceTree() {
    // Simple balancing by rebuilding from sorted array
    const values = this.bst.inorderTraversal()
    if (values.length === 0) {
      this.showMessage('Дерево порожнє', 'info')
      return
    }

    this.bst.clear()
    this.buildBalancedTree(values, 0, values.length - 1)
    this.addToHistory('Дерево збалансовано', 'add')
    this.updateStatistics()
    this.drawTree()
    this.showMessage('Дерево збалансовано', 'success')
  }

  buildBalancedTree(values, start, end) {
    if (start > end) return

    const mid = Math.floor((start + end) / 2)
    this.bst.insert(values[mid])
    this.buildBalancedTree(values, start, mid - 1)
    this.buildBalancedTree(values, mid + 1, end)
  }

  exportTree() {
    const svgData = new XMLSerializer().serializeToString(this.svg)
    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')
    const img = new Image()

    canvas.width = 800
    canvas.height = 600

    img.onload = function () {
      ctx.fillStyle = 'white'
      ctx.fillRect(0, 0, canvas.width, canvas.height)
      ctx.drawImage(img, 0, 0)

      const link = document.createElement('a')
      link.download = 'bst-tree.png'
      link.href = canvas.toDataURL()
      link.click()
    }

    img.src = 'data:image/svg+xml;base64,' + btoa(svgData)
    this.showMessage('Дерево експортовано', 'success')
  }

  performTraversal(type) {
    let result = []
    switch (type) {
      case 'inorder':
        result = this.bst.inorderTraversal()
        break
      case 'preorder':
        result = this.bst.preorderTraversal()
        break
      case 'postorder':
        result = this.bst.postorderTraversal()
        break
    }

    this.traversalResult.textContent = result.join(' → ')
    this.addToHistory(`Обхід ${type}: [${result.join(', ')}]`, 'search')

    if (this.animationsEnabled) {
      this.animateTraversal(result)
    }
  }

  drawTree() {
    this.svg.innerHTML = ''

    if (this.bst.root === null) {
      const text = document.createElementNS(
        'http://www.w3.org/2000/svg',
        'text',
      )
      text.setAttribute('x', '400')
      text.setAttribute('y', '250')
      text.setAttribute('text-anchor', 'middle')
      text.setAttribute('font-size', '18')
      text.setAttribute('fill', '#999')
      text.textContent = 'Дерево порожнє. Додайте вузли для початку.'
      this.svg.appendChild(text)
      return
    }

    // Calculate positions
    const svgWidth = 800
    const svgHeight = 500
    this.calculateNodePositions(this.bst.root, svgWidth / 2, 50, svgWidth / 4)

    // Create groups
    const edgeGroup = document.createElementNS(
      'http://www.w3.org/2000/svg',
      'g',
    )
    edgeGroup.setAttribute('id', 'edges')

    const nodeGroup = document.createElementNS(
      'http://www.w3.org/2000/svg',
      'g',
    )
    nodeGroup.setAttribute('id', 'nodes')

    // Draw edges
    this.drawEdges(this.bst.root, edgeGroup)

    // Draw nodes
    this.drawNodes(this.bst.root, nodeGroup)

    this.svg.appendChild(edgeGroup)
    this.svg.appendChild(nodeGroup)
  }

  calculateNodePositions(node, x, y, spacing) {
    if (node === null) return

    node.x = x
    node.y = y

    if (node.left) {
      this.calculateNodePositions(node.left, x - spacing, y + 80, spacing / 2)
    }

    if (node.right) {
      this.calculateNodePositions(node.right, x + spacing, y + 80, spacing / 2)
    }
  }

  drawEdges(node, group) {
    if (node === null) return

    if (node.left) {
      const edge = document.createElementNS(
        'http://www.w3.org/2000/svg',
        'line',
      )
      edge.setAttribute('x1', node.x)
      edge.setAttribute('y1', node.y)
      edge.setAttribute('x2', node.left.x)
      edge.setAttribute('y2', node.left.y)
      edge.setAttribute('class', 'edge')
      edge.setAttribute('id', `edge-${node.value}-${node.left.value}`)
      group.appendChild(edge)

      this.drawEdges(node.left, group)
    }

    if (node.right) {
      const edge = document.createElementNS(
        'http://www.w3.org/2000/svg',
        'line',
      )
      edge.setAttribute('x1', node.x)
      edge.setAttribute('y1', node.y)
      edge.setAttribute('x2', node.right.x)
      edge.setAttribute('y2', node.right.y)
      edge.setAttribute('class', 'edge')
      edge.setAttribute('id', `edge-${node.value}-${node.right.value}`)
      group.appendChild(edge)

      this.drawEdges(node.right, group)
    }
  }

  drawNodes(node, group) {
    if (node === null) return

    // Create node group
    const nodeGroup = document.createElementNS(
      'http://www.w3.org/2000/svg',
      'g',
    )
    nodeGroup.setAttribute('class', 'node')
    nodeGroup.setAttribute('id', `node-${node.value}`)
    nodeGroup.setAttribute('transform', `translate(${node.x}, ${node.y})`)

    // Add click event
    nodeGroup.addEventListener('click', () => this.showNodeDetails(node))

    // Create circle
    const circle = document.createElementNS(
      'http://www.w3.org/2000/svg',
      'circle',
    )
    circle.setAttribute('r', '25')

    // Add circle first so text appears on top
    nodeGroup.appendChild(circle)

    // Create text
    if (this.showValues) {
      const text = document.createElementNS(
        'http://www.w3.org/2000/svg',
        'text',
      )
      text.textContent = node.value
      nodeGroup.appendChild(text)
    }

    group.appendChild(nodeGroup)

    // Store reference
    node.element = nodeGroup

    // Draw children
    this.drawNodes(node.left, group)
    this.drawNodes(node.right, group)
  }

  async animateInsertion(newNode) {
    this.drawTree()
    if (newNode && newNode.element) {
      newNode.element.classList.add('new-node')
      await this.sleep(600)
    }
  }

  async animateSearch(value) {
    const path = []
    let current = this.bst.root

    while (current !== null) {
      path.push(current)
      if (value < current.value) {
        current = current.left
      } else if (value > current.value) {
        current = current.right
      } else {
        break
      }
    }

    for (const node of path) {
      this.highlightNode(node, 'highlighted')
      await this.sleep(this.animationSpeed)

      if (node.value === value) {
        this.highlightNode(node, 'found')
        break
      } else {
        this.highlightNode(node, '')
      }
    }
  }

  async animateDeletion(node) {
    if (node && node.element) {
      node.element.style.opacity = '0.5'
      node.element.style.transform = 'scale(0.8)'
      await this.sleep(300)
    }
  }

  async animateTraversal(values) {
    for (const value of values) {
      const node = this.bst.search(value)
      if (node) {
        this.highlightNode(node, 'highlighted')
        await this.sleep(200)
        this.highlightNode(node, '')
      }
    }
  }

  highlightNode(node, className) {
    if (node && node.element) {
      node.element.classList.remove('highlighted', 'found')
      if (className) {
        node.element.classList.add(className)
      }
    }
  }

  clearHighlights() {
    document.querySelectorAll('.node').forEach((node) => {
      node.classList.remove('highlighted', 'found', 'new-node')
    })
    document.querySelectorAll('.edge').forEach((edge) => {
      edge.classList.remove('highlighted')
    })
  }

  showNodeDetails(node) {
    const leftValue = node.left ? node.left.value : 'null'
    const rightValue = node.right ? node.right.value : 'null'
    const height = this.bst.getHeight(node)

    this.nodeDetails.innerHTML = `
      <p><strong>Значення:</strong> ${node.value}</p>
      <p><strong>Лівий дочірній вузол:</strong> ${leftValue}</p>
      <p><strong>Правий дочірній вузол:</strong> ${rightValue}</p>
      <p><strong>Висота піддерева:</strong> ${height}</p>
      <p><strong>Кількість вузлів у піддереві:</strong> ${this.bst.getNodeCount(
        node,
      )}</p>
    `

    this.modal.style.display = 'block'
  }

  closeModalWindow() {
    this.modal.style.display = 'none'
  }

  updateStatistics() {
    this.nodeCount.textContent = this.bst.getNodeCount()
    this.treeHeight.textContent = this.bst.getHeight()

    const minVal = this.bst.getMinValue()
    const maxVal = this.bst.getMaxValue()

    this.minValue.textContent = minVal !== null ? minVal : '-'
    this.maxValue.textContent = maxVal !== null ? maxVal : '-'
  }

  addToHistory(message, type = '') {
    const historyItem = document.createElement('div')
    historyItem.className = `history-item ${type}`
    historyItem.textContent = `${new Date().toLocaleTimeString()}: ${message}`

    this.history.insertBefore(historyItem, this.history.firstChild)

    // Keep only last 20 items
    while (this.history.children.length > 20) {
      this.history.removeChild(this.history.lastChild)
    }
  }

  showMessage(message, type = 'info') {
    // Create toast notification
    const toast = document.createElement('div')
    toast.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 15px 20px;
      border-radius: 8px;
      color: white;
      font-weight: 500;
      z-index: 10000;
      animation: slideInRight 0.3s ease;
    `

    const colors = {
      success: '#48bb78',
      error: '#fc8181',
      warning: '#f6ad55',
      info: '#4299e1',
    }

    toast.style.backgroundColor = colors[type] || colors.info
    toast.textContent = message
    document.body.appendChild(toast)

    setTimeout(() => {
      toast.style.animation = 'fadeOut 0.3s ease'
      setTimeout(() => {
        document.body.removeChild(toast)
      }, 300)
    }, 3000)
  }

  sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms))
  }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
  new TreeVisualizer()
})
