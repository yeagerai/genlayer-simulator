import { describe, it, expect } from 'vitest';
import { useInputMap } from '@/hooks';
import StringField from '@/components/global/fields/StringField.vue';
import IntegerField from '@/components/global/fields/IntegerField.vue';
import FloatField from '@/components/global/fields/FloatField.vue';
import BooleanField from '@/components/global/fields/BooleanField.vue';

describe('useInputMap composable', () => {
  const { getComponent } = useInputMap();

  it('should return the correct component for type "string"', () => {
    const component = getComponent('string');
    expect(component).toBe(StringField);
  });

  it('should return the correct component for type "int"', () => {
    const component = getComponent('int');
    expect(component).toBe(IntegerField);
  });

  it('should return the correct component for type "bool"', () => {
    const component = getComponent('bool');
    expect(component).toBe(BooleanField);
  });

  it('should default to string for an empty type', () => {
    const component = getComponent('');
    expect(component).toBe(StringField);
  });

  it('should default to string for an unknown type', () => {
    const component = getComponent('unknown');
    expect(component).toBe(StringField);
  });
});
