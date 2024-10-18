import StringField from '@/components/global/fields/StringField.vue';
import IntegerField from '@/components/global/fields/IntegerField.vue';
import BooleanField from '@/components/global/fields/BooleanField.vue';

export const InputTypesMap: { [k: string]: any } = {
  string: StringField,
  int: IntegerField,
  bool: BooleanField,
};

export const useInputMap = () => {
  const getComponent = (type: string) => {
    const component = InputTypesMap[type];

    if (!component) {
      console.warn(
        `Component not found for input type: ${type}, defaulting to string`,
      );
      return StringField;
    }

    return component;
  };

  return { getComponent };
};
