/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{html,js,ts,tsx,vue}"],
  darkMode: ['selector', '[data-mode="dark"]'],
  theme: {
    extend: {
      colors: {
        'primary': '#1a3851',
        transparent: 'transparent'
      },
    },
  },
  plugins: [],
}

