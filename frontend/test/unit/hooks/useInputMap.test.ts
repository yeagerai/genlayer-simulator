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

  it('should return the correct component for type "uint256"', () => {
    const component = getComponent('uint256');
    expect(component).toBe(IntegerField);
  });

  it('should return the correct component for type "float"', () => {
    const component = getComponent('float');
    expect(component).toBe(FloatField);
  });

  it('should return the correct component for type "bool"', () => {
    const component = getComponent('bool');
    expect(component).toBe(BooleanField);
  });

  it('should throw an error for an unknown type', () => {
    expect(() => getComponent('unknown')).toThrowError(
      'Component not found for input type: unknown',
    );
  });
});
