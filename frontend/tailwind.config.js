/** @type {import('tailwindcss').Config} */
import colors from 'tailwindcss/colors'
import forms from '@tailwindcss/forms';

export default {
  content: ['./src/**/*.{html,js,ts,tsx,vue}'],
  darkMode: ['selector', '[data-mode="dark"]'],
  theme: {
    extend: {
      transitionDuration: {
        DEFAULT: '100ms',
      },
      colors: {
        primary: '#1a3851',
        accent: colors.sky[600],
        transparent: 'transparent',
      },
    },
  },
  plugins: [forms],
}