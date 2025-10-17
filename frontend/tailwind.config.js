/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fef9ec',
          100: '#fbefc9',
          200: '#f7dd8e',
          300: '#f4c430',
          400: '#f0ad28',
          500: '#ea8e0f',
          600: '#ce6b0a',
          700: '#ab4c0c',
          800: '#8b3b10',
          900: '#723210',
        },
        secondary: {
          50: '#fff1f1',
          100: '#ffe1e1',
          200: '#ffc7c7',
          300: '#ffa0a0',
          400: '#ff6969',
          500: '#ff6f61',
          600: '#ed1c24',
          700: '#c80f1a',
          800: '#a51119',
          900: '#88131b',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Poppins', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
