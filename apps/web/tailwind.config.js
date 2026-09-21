/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#0a0f1d',
          900: '#0f172a',
          800: '#1e293b',
          700: '#334155',
        },
        brand: {
          blue: '#1d4ed8',
          hover: '#1e40af',
          light: '#eff6ff',
          border: '#dbeafe',
        },
        status: {
          supported: '#15803d',
          supportedBg: '#f0fdf4',
          supportedBorder: '#bbf7d0',
          review: '#b45309',
          reviewBg: '#fffbeb',
          reviewBorder: '#fde68a',
          insufficient: '#475569',
          insufficientBg: '#f8fafc',
          insufficientBorder: '#cbd5e1',
          nomatch: '#b91c1c',
          nomatchBg: '#fef2f2',
          nomatchBorder: '#fecaca',
        }
      }
    },
  },
  plugins: [],
}
