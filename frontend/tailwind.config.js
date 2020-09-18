module.exports = {
  future: {
    // removeDeprecatedGapUtilities: true,
    // purgeLayersByDefault: true,
  },
  purge: [],
  theme: {
    extend: {
      colors: {
        'purple-matcha' : '#6246EA',
        'white-matcha' : '#FFFFFE',
        'gray-matcha' : '#001858',
      },
      borderRadius: {
        'xl' : '2rem',
      },
    },
  },
  variants: {
    backgroundColor: ['responsive', 'hover', 'focus', 'active'],
    borderRadius: ['responsive', 'hover', 'focus', 'active'],
  },
  plugins: [],
}
