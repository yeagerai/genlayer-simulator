import StringField from '@/components/global/fields/StringField.vue';
import IntegerField from '@/components/global/fields/IntegerField.vue';
import FloatField from '@/components/global/fields/FloatField.vue';
import BooleanField from '@/components/global/fields/BooleanField.vue';

const InputTypesMap: { [k: string]: any } = {
  str: StringField,
  int: IntegerField,
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
