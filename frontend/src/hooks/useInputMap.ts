import StringField from '@/components/global/fields/StringField.vue';
import IntegerField from '@/components/global/fields/IntegerField.vue';
import FloatField from '@/components/global/fields/FloatField.vue';
import BooleanField from '@/components/global/fields/BooleanField.vue';

export const InputTypesMap: { [k: string]: any } = {
  string: StringField,
  uint256: IntegerField,
  float: FloatField,
  bool: BooleanField,
};

export const useInputMap = () => {
  const getComponent = (type: string) => {
    const component = InputTypesMap[type];

    if (!component) {
      throw new Error(`Component not found for input type: ${type}`);
    }

    return component;
  };

  return { getComponent };
};
