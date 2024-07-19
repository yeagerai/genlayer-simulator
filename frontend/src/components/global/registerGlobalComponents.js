export default function registerGlobalComponents(app) {
  const components = import.meta.glob('@/components/global/*.vue')

  for (const path in components) {
    components[path]().then((module) => {
      const componentName = path
        .split('/')
        .pop()
        .replace(/\.\w+$/, '')
      app.component(componentName, module.default)
    })
  }
}
