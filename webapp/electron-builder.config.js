if (process.env.VITE_APP_VERSION === undefined) {
  const now = new Date();
  process.env.VITE_APP_VERSION = `${now.getUTCFullYear() - 2000}.${
    now.getUTCMonth() + 1
  }.${now.getUTCDate()}-${now.getUTCHours() * 60 + now.getUTCMinutes()}`;
}

/**
 * @type {import('electron-builder').Configuration}
 * @see https://www.electron.build/configuration/configuration
 */
const config = {
  appId: 'com.starrailcopilot.app',
  productName: 'StarRailCopilot',
  
  directories: {
    output: 'dist',
    buildResources: 'buildResources',
  },
  
  files: [
    'packages/**/dist/**',  // Vite构建输出
    // 排除不必要的文件
    '!**/node_modules/**', 
    '!**/tests/**',
    '!**/*.test.js',
    '!**/*.spec.js',
    '!**/coverage/**',
    '!**/.nyc_output/**',
    '!**/dist/**',  // 排除构建输出自身
    // 确保包含关键目录
    '../config/**',     // 如果存在的话
    '../deploy/**',     // 如果存在的话
    '../scripts/**'     // 脚本文件
  ],
  
  extraMetadata: {
    version: process.env.VITE_APP_VERSION,
  },
  
  // 目标平台配置
  targets: {
    // 生成可移植的可执行文件
    dir: {},
  },
  
  // 不同平台的目标格式
  win: {
    target: [
      {
        target: 'dir',
        arch: ['x64']
      }
    ],
    icon: 'buildResources/icon.ico'
  },
  
  mac: {
    target: [
      {
        target: 'dmg',
        arch: ['x64', 'arm64']
      },
      {
        target: 'zip',
        arch: ['x64', 'arm64']
      }
    ],
    icon: 'buildResources/icon.icns'
  },
  
  linux: {
    target: [
      {
        target: 'AppImage',
        arch: ['x64']
      },
      {
        target: 'deb',
        arch: ['x64']
      },
      {
        target: 'rpm',
        arch: ['x64']
      }
    ],
    icon: 'buildResources/icon.png',
    category: 'Utility'
  },
  
  // 打包选项
  compression: 'maximum',
  
  // NSIS 安装程序配置
  nsis: {
    oneClick: false,
    allowToChangeInstallationDirectory: true,
    createDesktopShortcut: true,
    createStartMenuShortcut: true
  },
  
  // dmg 配置 (macOS)
  dmg: {
    contents: [
      {
        x: 130,
        y: 220,
        type: 'file'
      },
      {
        x: 410,
        y: 220,
        type: 'link',
        path: '/Applications'
      }
    ]
  },
  
  // AppImage 配置 (Linux)
  appImage: {
    category: 'Utility'
  },
  
  // 文件关联
  fileAssociations: [
    {
      ext: 'src',
      name: 'StarRailCopilot Config',
      description: 'StarRailCopilot Configuration File',
      role: 'Editor'
    }
  ]
};

module.exports = config;
