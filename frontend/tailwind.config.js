/** @type {import('tailwindcss').Config} */
import colors from 'tailwindcss/colors';

export default {
  content: ["./src/**/*.{html,js,ts,tsx,vue}"],
  darkMode: ['selector', '[data-mode="dark"]'],
  theme: {
    extend: {
      transitionDuration: {
        DEFAULT: '100ms',
      },
      colors: {
        'primary': '#1a3851',
        'accent': colors.blue[500],
        transparent: 'transparent'
      },
    },
  },
  plugins: [],
}

