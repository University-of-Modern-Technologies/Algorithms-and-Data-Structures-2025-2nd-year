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

class TreeVisualizer {
  constructor() {
    this.svg = document.getElementById('treeSvg')
    this.currentNodeDisplay = document.getElementById('currentNode')
    this.orderDisplay = document.getElementById('orderDisplay')
    this.stackDisplay = document.getElementById('stackDisplay')
    this.algorithmDescription = document.getElementById('algorithmDescription')
    this.speedSlider = document.getElementById('speedSlider')
    this.speedValue = document.getElementById('speedValue')

    this.root = null
    this.animationSpeed = 800
    this.isAnimating = false
    this.isPaused = false
    this.traversalSteps = []
    this.currentStep = 0
    this.currentTraversal = null

    this.algorithms = {
      preorder: {
        name: 'Preorder (Прямий)',
        description:
          'Відвідуємо корінь, потім ліве піддерево, потім праве піддерево. Порядок: Корінь → Ліво → Право',
        func: this.preorderSteps.bind(this),
      },
      inorder: {
        name: 'Inorder (Симетричний)',
        description:
          'Відвідуємо ліве піддерево, потім корінь, потім праве піддерево. Порядок: Ліво → Корінь → Право',
        func: this.inorderSteps.bind(this),
      },
      postorder: {
        name: 'Postorder (Зворотний)',
        description:
          'Відвідуємо ліве піддерево, потім праве піддерево, потім корінь. Порядок: Ліво → Право → Корінь',
        func: this.postorderSteps.bind(this),
      },
    }

    this.initializeTree()
    this.setupEventListeners()
    this.drawTree()
  }

  initializeTree() {
    // Створюємо дерево як у Python коді
    this.root = new Node(1)
    this.root.left = new Node(2)
    this.root.right = new Node(3)
    this.root.left.left = new Node(4)
    this.root.left.right = new Node(5)
    this.root.right.left = new Node(13)
    this.root.right.right = new Node(15)

    this.calculateNodePositions(this.root, 400, 50, 200)
  }

  calculateNodePositions(node, x, y, spacing) {
    if (!node) return

    node.x = x
    node.y = y

    if (node.left) {
      this.calculateNodePositions(node.left, x - spacing, y + 80, spacing / 2)
    }

    if (node.right) {
      this.calculateNodePositions(node.right, x + spacing, y + 80, spacing / 2)
    }
  }

  setupEventListeners() {
    document.getElementById('preorderBtn').addEventListener('click', () => {
      this.startTraversal('preorder')
    })

    document.getElementById('inorderBtn').addEventListener('click', () => {
      this.startTraversal('inorder')
    })

    document.getElementById('postorderBtn').addEventListener('click', () => {
      this.startTraversal('postorder')
    })

    document.getElementById('pauseBtn').addEventListener('click', () => {
      this.togglePause()
    })

    document.getElementById('resetBtn').addEventListener('click', () => {
      this.reset()
    })

    document.getElementById('stepBtn').addEventListener('click', () => {
      this.stepForward()
    })

    this.speedSlider.addEventListener('input', (e) => {
      this.animationSpeed = parseInt(e.target.value)
      this.speedValue.textContent = `${this.animationSpeed}ms`
    })
  }

  drawTree() {
    this.svg.innerHTML = ''

    // Група для ребер
    const edgeGroup = document.createElementNS(
      'http://www.w3.org/2000/svg',
      'g',
    )
    edgeGroup.setAttribute('id', 'edges')

    // Група для вузлів
    const nodeGroup = document.createElementNS(
      'http://www.w3.org/2000/svg',
      'g',
    )
    nodeGroup.setAttribute('id', 'nodes')

    // Малюємо ребра
    this.drawEdges(this.root, edgeGroup)

    // Малюємо вузли
    this.drawNodes(this.root, nodeGroup)

    this.svg.appendChild(edgeGroup)
    this.svg.appendChild(nodeGroup)
  }

  drawEdges(node, group) {
    if (!node) return

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
    if (!node) return

    // Створюємо групу для вузла
    const nodeGroup = document.createElementNS(
      'http://www.w3.org/2000/svg',
      'g',
    )
    nodeGroup.setAttribute('class', 'node')
    nodeGroup.setAttribute('id', `node-${node.value}`)
    nodeGroup.setAttribute('transform', `translate(${node.x}, ${node.y})`)

    // Створюємо коло
    const circle = document.createElementNS(
      'http://www.w3.org/2000/svg',
      'circle',
    )
    circle.setAttribute('r', '25')

    // Створюємо текст
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text')
    text.textContent = node.value

    nodeGroup.appendChild(circle)
    nodeGroup.appendChild(text)
    group.appendChild(nodeGroup)

    // Зберігаємо посилання на елемент
    node.element = nodeGroup

    // Рекурсивно малюємо дочірні вузли
    this.drawNodes(node.left, group)
    this.drawNodes(node.right, group)
  }

  preorderSteps(node, steps = [], stack = []) {
    if (!node) return steps

    steps.push({
      type: 'push',
      node: node,
      stack: [...stack, node.value],
    })

    steps.push({
      type: 'visit',
      node: node,
      stack: [...stack, node.value],
    })

    this.preorderSteps(node.left, steps, [...stack, node.value])
    this.preorderSteps(node.right, steps, [...stack, node.value])

    steps.push({
      type: 'pop',
      node: node,
      stack: stack.slice(0, -1),
    })

    return steps
  }

  inorderSteps(node, steps = [], stack = []) {
    if (!node) return steps

    steps.push({
      type: 'push',
      node: node,
      stack: [...stack, node.value],
    })

    this.inorderSteps(node.left, steps, [...stack, node.value])

    steps.push({
      type: 'visit',
      node: node,
      stack: stack,
    })

    this.inorderSteps(node.right, steps, stack)

    steps.push({
      type: 'pop',
      node: node,
      stack: stack.slice(0, -1),
    })

    return steps
  }

  postorderSteps(node, steps = [], stack = []) {
    if (!node) return steps

    steps.push({
      type: 'push',
      node: node,
      stack: [...stack, node.value],
    })

    this.postorderSteps(node.left, steps, [...stack, node.value])
    this.postorderSteps(node.right, steps, [...stack, node.value])

    steps.push({
      type: 'visit',
      node: node,
      stack: stack,
    })

    steps.push({
      type: 'pop',
      node: node,
      stack: stack.slice(0, -1),
    })

    return steps
  }

  async startTraversal(type) {
    if (this.isAnimating) return

    this.reset()
    this.isAnimating = true
    this.currentTraversal = type
    this.traversalSteps = this.algorithms[type].func(this.root)

    // Оновлюємо опис алгоритму
    this.algorithmDescription.textContent = this.algorithms[type].description

    // Блокуємо кнопки обходу
    this.toggleTraversalButtons(false)

    // Розблоковуємо кнопку паузи
    document.getElementById('pauseBtn').disabled = false

    await this.animateSteps()
  }

  async animateSteps() {
    for (let i = 0; i < this.traversalSteps.length; i++) {
      if (!this.isAnimating) break

      while (this.isPaused) {
        await this.sleep(100)
      }

      this.currentStep = i
      await this.executeStep(this.traversalSteps[i])
      await this.sleep(this.animationSpeed)
    }

    this.isAnimating = false
    this.toggleTraversalButtons(true)
    document.getElementById('pauseBtn').disabled = true
  }

  async executeStep(step) {
    const { type, node, stack } = step

    // Оновлюємо стек
    this.updateStack(stack)

    if (type === 'push') {
      this.highlightEdge(node, true)
    } else if (type === 'visit') {
      this.highlightNode(node, 'visiting')
      this.currentNodeDisplay.textContent = node.value

      // Додаємо до порядку обходу
      const orderItem = document.createElement('div')
      orderItem.className = 'order-item'
      orderItem.textContent = node.value
      this.orderDisplay.appendChild(orderItem)

      await this.sleep(this.animationSpeed / 2)
      this.highlightNode(node, 'visited')
    } else if (type === 'pop') {
      this.highlightEdge(node, false)
    }
  }

  highlightNode(node, className) {
    // Скидаємо попередні підсвічування
    if (className === 'visiting') {
      document.querySelectorAll('.node').forEach((n) => {
        n.classList.remove('visiting')
      })
    }

    if (node.element) {
      node.element.classList.remove('visiting', 'visited')
      if (className) {
        node.element.classList.add(className)
      }
    }
  }

  highlightEdge(node, active) {
    if (node.left) {
      const edge = document.getElementById(
        `edge-${node.value}-${node.left.value}`,
      )
      if (edge) {
        if (active) {
          edge.classList.add('active')
        } else {
          edge.classList.remove('active')
        }
      }
    }

    if (node.right) {
      const edge = document.getElementById(
        `edge-${node.value}-${node.right.value}`,
      )
      if (edge) {
        if (active) {
          edge.classList.add('active')
        } else {
          edge.classList.remove('active')
        }
      }
    }
  }

  updateStack(stack) {
    this.stackDisplay.innerHTML = ''

    if (stack.length === 0) {
      this.stackDisplay.innerHTML =
        '<div class="stack-item">Стек порожній</div>'
      return
    }

    stack.reverse().forEach((item) => {
      const stackItem = document.createElement('div')
      stackItem.className = 'stack-item'
      stackItem.textContent = `Node(${item})`
      this.stackDisplay.appendChild(stackItem)
    })
  }

  togglePause() {
    this.isPaused = !this.isPaused
    const pauseBtn = document.getElementById('pauseBtn')
    pauseBtn.textContent = this.isPaused ? 'Продовжити' : 'Пауза'
  }

  async stepForward() {
    if (this.currentStep >= this.traversalSteps.length - 1) return

    this.currentStep++
    await this.executeStep(this.traversalSteps[this.currentStep])
  }

  reset() {
    this.isAnimating = false
    this.isPaused = false
    this.currentStep = 0
    this.traversalSteps = []
    this.currentTraversal = null

    // Скидаємо візуальні елементи
    document.querySelectorAll('.node').forEach((node) => {
      node.classList.remove('visiting', 'visited')
    })

    document.querySelectorAll('.edge').forEach((edge) => {
      edge.classList.remove('active')
    })

    this.currentNodeDisplay.textContent = '-'
    this.orderDisplay.innerHTML = ''
    this.stackDisplay.innerHTML = '<div class="stack-item">Стек порожній</div>'
    this.algorithmDescription.textContent = ''

    // Скидаємо кнопки
    this.toggleTraversalButtons(true)
    document.getElementById('pauseBtn').disabled = true
    document.getElementById('pauseBtn').textContent = 'Пауза'
  }

  toggleTraversalButtons(enabled) {
    document.getElementById('preorderBtn').disabled = !enabled
    document.getElementById('inorderBtn').disabled = !enabled
    document.getElementById('postorderBtn').disabled = !enabled
  }

  sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms))
  }
}

// Ініціалізуємо візуалізатор при завантаженні сторінки
document.addEventListener('DOMContentLoaded', () => {
  new TreeVisualizer()
})
