/**
 * 工程造价速算工具 - 完整版 v2
 * 来源：豆包Chat（https://www.doubao.com/chat/38421127038926338）
 * 功能：建筑工程 + 道路场地工程 估算
 * 版本：v2.1 (2026-04-11) — 办公楼按层数分级，厂房一层/二层/三层
 */

// ============================================================
// 1. 基础造价库（2023年基准）
// ============================================================

const costData = {
  // ---------- 建筑工程 ----------
  建筑: {
    普通住宅: {
      '1-6层':   { min: 1100, max: 1500 },
      '7-11层':  { min: 1400, max: 1800 },
      '12-18层': { min: 1800, max: 2300 },
      '19-33层': { min: 2300, max: 3000 },
    },
    办公楼: {
      '1-6层':   { min: 1600, max: 2000 },
      '7-11层':  { min: 2000, max: 2500 },
      '12-18层': { min: 2500, max: 3100 },
      '19-33层': { min: 3100, max: 3900 },
    },
    厂房: {
      '一层': { min: 1000, max: 1400 },
      '二层': { min: 1200, max: 1600 },
      '三层': { min: 1300, max: 1800 },
    },
    仓库: {
      '单层': { min: 650, max: 950 },
    },
  },

  // ---------- 道路 & 场地 ----------
  道路场地: {
    '素混凝土场地10cm':   { min: 65,  max: 85  },
    '素混凝土场地15cm':   { min: 85,  max: 110 },
    '钢筋混凝土场地15cm':{ min: 110, max: 140 },
    '混凝土道路15cm':    { min: 90,  max: 120 },
    '混凝土道路20cm':    { min: 120, max: 150 },
    '混凝土道路25cm':    { min: 150, max: 180 },
    '沥青路面4cm':       { min: 75,  max: 95  },
    '沥青路面6cm':       { min: 95,  max: 120 },
    '沥青路面双层8cm':   { min: 130, max: 160 },
  },
};

// ============================================================
// 2. 系数配置
// ============================================================

const decorateCoeff  = { '毛坯': 1.0, '简装': 1.2, '中档': 1.4, '精装': 1.8 };
const areaCoeff     = { '县城': 0.9, '地级市': 1.0, '二线': 1.1, '一线': 1.2 };
const yearCoeff     = { '2021年': 0.88, '2022年': 0.94, '2023年': 1.00, '2024年': 1.05, '2025年': 1.10, '2026年': 1.15 };
const materialCoeff  = { '下跌10%': 0.90, '下跌5%': 0.95, '持平': 1.00, '上涨5%': 1.05, '上涨10%': 1.10 };

// ============================================================
// 3. 核心计算函数
// ============================================================

/**
 * 工程造价估算
 * @param {Object} params
 * @param {string} params.cate      - 类别：'建筑' 或 '道路场地'
 * @param {string} params.type      - 具体类型
 * @param {string} params.floor     - 层数/规格
 * @param {number} params.square    - 面积 m²
 * @param {string} params.decorate   - 装修标准（仅建筑用）
 * @param {string} params.areaLevel - 地区
 * @param {string} params.year      - 年份
 * @param {string} params.material  - 材料行情
 * @returns {Object|null}
 */
function calcCost({
  cate,
  type,
  floor     = '',
  square,
  decorate  = '毛坯',
  areaLevel = '地级市',
  year      = '2026年',
  material  = '平稳',
}) {
  let base;
  if (cate === '建筑') {
    base = costData.建筑[type]?.[floor];
  } else if (cate === '道路场地') {
    base = costData.道路场地[type];
  }
  if (!base) return null;

  const d = (cate === '道路场地') ? 1.0 : (decorateCoeff[decorate] ?? 1.0);
  const a = areaCoeff[areaLevel] ?? 1.0;
  const y = yearCoeff[year]       ?? 1.0;
  const m = materialCoeff[material] ?? 1.0;

  const minUnit = Math.round(base.min * d * a * y * m);
  const maxUnit = Math.round(base.max * d * a * y * m);
  const minTotal = minUnit * square;
  const maxTotal = maxUnit * square;

  return {
    unitCost: `${minUnit.toLocaleString()} ~ ${maxUnit.toLocaleString()} 元/㎡`,
    totalCost: `${(minTotal / 10000).toFixed(2)} ~ ${(maxTotal / 10000).toFixed(2)} 万元`,
    _minUnit: minUnit, _maxUnit: maxUnit,
    _minTotal: minTotal, _maxTotal: maxTotal,
  };
}

// ============================================================
// 4. 测试用例
// ============================================================

console.log('========== 建筑工程 ==========');
console.log('普通住宅 7-11层 1200㎡ 毛坯 地级市 2026 平稳:');
console.log(calcCost({ cate: '建筑', type: '普通住宅', floor: '7-11层', square: 1200, decorate: '毛坯', areaLevel: '地级市', year: '2026年', material: '平稳' }));

console.log('\n办公楼 12-18层 3000㎡ 精装 一线城市 2025 上涨:');
console.log(calcCost({ cate: '建筑', type: '办公楼', floor: '12-18层', square: 3000, decorate: '精装', areaLevel: '一线', year: '2025年', material: '上涨5%' }));

console.log('\n厂房 二层 2000㎡ 简装 二线城市 2026 上涨:');
console.log(calcCost({ cate: '建筑', type: '厂房', floor: '二层', square: 2000, decorate: '简装', areaLevel: '二线城市', year: '2026年', material: '上涨5%' }));

console.log('\n========== 道路场地 ==========');
console.log('沥青路面双层8cm 2000㎡ 县城 2026 上涨:');
console.log(calcCost({ cate: '道路场地', type: '沥青路面双层8cm', square: 2000, areaLevel: '县城', year: '2026年', material: '上涨5%' }));

console.log('\n钢筋混凝土场地15cm 500㎡ 地级市 2024 平稳:');
console.log(calcCost({ cate: '道路场地', type: '钢筋混凝土场地15cm', square: 500, areaLevel: '地级市', year: '2024年', material: '平稳' }));

module.exports = { calcCost, costData, decorateCoeff, areaCoeff, yearCoeff, materialCoeff };
