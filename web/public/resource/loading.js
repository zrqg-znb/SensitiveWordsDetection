/**
 * 初始化加载效果的svg格式logo
 * @param {string} id - 元素id
 */
function initSvgLogo(id) {
//     const svgStr = `<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
//   <style>
//     .tech-line {
//       stroke: #00ffff; /* 青蓝色，常见的科技感颜色 */
//       stroke-width: 4;
//       fill: none;
//       stroke-linecap: round;
//       stroke-linejoin: round;
//     }
//     .tech-circle {
//       fill: #00ffff;
//     }
//   </style>
//
//   <path class="tech-line" d="M 10 50 Q 30 20 50 50 T 90 50"/>
//   <circle class="tech-circle" cx="10" cy="50" r="5"/>
//   <circle class="tech-circle" cx="50" cy="50" r="5"/>
//   <circle class="tech-circle" cx="90" cy="50" r="5"/>
// </svg>`
    const appEl = document.querySelector(id)
    const div = document.createElement('div')
    // div.innerHTML = svgStr
    if (appEl) {
        appEl.appendChild(div)
    }
}

function addThemeColorCssVars() {
    const key = '__THEME_COLOR__'
    const defaultColor = '#2080F0FF'
    const themeColor = window.localStorage.getItem(key) || defaultColor
    const cssVars = `--primary-color: ${themeColor}`
    document.documentElement.style.cssText = cssVars
}

addThemeColorCssVars()

initSvgLogo('#loadingLogo')
