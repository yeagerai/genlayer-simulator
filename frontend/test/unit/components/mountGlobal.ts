import { mount } from '@vue/test-utils';
import { globalComponents } from '@/../../frontend/src/components/global/registerGlobalComponents';

export default function mountGlobal(component: any, options?: any) {
  let wrapper = mount(component, {
    global: {
      components: globalComponents,
    },
    ...options,
  });
  return wrapper;
}
