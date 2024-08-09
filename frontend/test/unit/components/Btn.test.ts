import { describe, it, expect } from 'vitest';
import Btn from '@/../../frontend/src/components/global/Btn.vue';
import mountGlobal from './mountGlobal';

describe('Btn.vue', () => {
  it('should emit a click event when clicked', async () => {
    let wrapper = mountGlobal(Btn);
    await wrapper.trigger('click');
    expect(wrapper.emitted('click')).toBeTruthy();
  });

  it('should apply testId to data-testid attribute', () => {
    const testId = 'my-button';
    let wrapper = mountGlobal(Btn, {
      props: { testId },
    });
    expect(wrapper.attributes('data-testid')).toBe(testId);
  });
});
