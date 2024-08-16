import StringField from '@/components/global/fields/StringField.vue';
import IntegerField from '@/components/global/fields/IntegerField.vue';
import FloatField from '@/components/global/fields/FloatField.vue';
import BooleanField from '@/components/global/fields/BooleanField.vue';

export const InputTypesMap: { [k: string]: any } = {
  str: StringField, // For backwards compatibility with constructors; should be removed when constructors are refactored
  int: IntegerField, // For backwards compatibility with constructors; should be removed when constructors are refactored
  string: StringField,
  uint256: IntegerField,
  float: FloatField,
  bool: BooleanField,
};
