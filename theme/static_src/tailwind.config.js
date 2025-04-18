/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  content: [
    /**
     * HTML. Paths to Django template files that will contain Tailwind CSS classes.
     */

    /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
    "../templates/**/*.html",

    /*
     * Main templates directory of the project (BASE_DIR/templates).
     * Adjust the following line to match your project structure.
     */
    "../../templates/**/*.html",

    /*
     * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
     * Adjust the following line to match your project structure.
     */
    "../../**/templates/**/*.html",

    /**
     * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
     * patterns match your project structure.
     */
    /* JS 1: Ignore any JavaScript in node_modules folder. */
    // '!../../**/node_modules',
    /* JS 2: Process all JavaScript files in the project. */
    // '../../**/*.js',

    /**
     * Python: If you use Tailwind CSS classes in Python, uncomment the following line
     * and make sure the pattern below matches your project structure.
     */
    // '../../**/*.py'
  ],
  theme: {
    fontFamily: {
      serif: ['"Playfair Display"', ...defaultTheme.fontFamily.serif],
      sans: ['"Junicode"', ...defaultTheme.fontFamily.sans],
    },
    extend: {
      spacing: {
        paragraph: "1.5rem",
      },
      colors: {
        "link-color": "#1a202c",
        "lasfera-red": "#B91C1C",
        "lasfera-green": "#3e5244",
        "lasfera-yellow": "#DEB841",
        "lasfera-gray": "#7C9299",
        "lasfera-darker-gray": "#63747A",
        "lasfera-black": "#191716",
        "lasfera-white": "#FFFBFE",
      },
      textDecoration: ["responsive", "hover", "focus", "active", "group-hover"],
      typography: {
        DEFAULT: {
          css: {
            fontSize: "1.2rem",
          },
        },
      },
    },
  },
  variants: {
    extend: {
      textColor: ["visited", "hover", "active"],
    },
  },
  plugins: [
    /**
     * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
     * for forms. If you don't like it or have own styling for forms,
     * comment the line below to disable '@tailwindcss/forms'.
     */
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/aspect-ratio"),
  ],
};
