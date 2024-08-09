import StringField from '@/components/fields/StringField.vue';
import IntegerField from '@/components/fields/IntegerField.vue';
import FloatField from '@/components/fields/FloatField.vue';
import BooleanField from '@/components/fields/BooleanField.vue';

export const InputTypesMap: { [k: string]: any } = {
  str: StringField,
  int: IntegerField,
  float: FloatField,
  bool: BooleanField,
};
