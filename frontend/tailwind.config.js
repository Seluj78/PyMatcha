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
        'purple-matcha-menu-current': '#efedfd',
        'purple-matcha-menu-hover': '#e0dafb',
        'white-matcha' : '#FFFFFE',
        'gray-matcha' : '#001858',
      },
      borderRadius: {
        'xl' : '2rem',
      },
      fontSize: {
        '7xl': '5rem',
        '8xl': '6rem',
      },
      maxWidth: {
        'xss': '15rem',
      },
    },
  },
  variants: {
    backgroundColor: ['responsive', 'hover', 'focus', 'active'],
    borderRadius: ['responsive', 'hover', 'focus', 'active'],
  },
  plugins: [],
}
