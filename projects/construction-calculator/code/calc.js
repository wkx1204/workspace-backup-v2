/**
 * 工程造价速算工具 - 核心计算逻辑
 * 来源：豆包Chat + Boss校准数据
 * 版本：v1.0 (2026-04-11)
 */

// ============================================================
// 1. 基础数据配置
// ============================================================

const costData = {
  // 住宅
  house: {
    '1_6':   [1100, 1500],   // 普通住宅 1-6层
    '7_11':  [1400, 1800],   // 小高层 7-11层
    '12_18': [1600, 2100],   // 中高层 12-18层
    '19_33': [1900, 2500],   // 高层 19-33层
  },
  '安置房': {
    '多层': [900, 1400],
    '高层': [900, 1400],
  },
  '别墅': {
    '联排': [2200, 3000],
  },
  // 办公楼
  office: {
    '多层': [1500, 1900],
    '高层': [1900, 2600],
  },
  // 学校/教学楼
  school: {
    '4_6层': [1600, 2100],
  },
  // 幼儿园
  kindergarten: {
    '2_3层': [1800, 2400],
  },
  // 医院
  hospital: {
    '多层': [2500, 3500],
  },
  // 商场/商业
  mall: {
    '多层': [2200, 3000],
  },
  // 厂房
  factory: {
    '砖混单层':  [900, 1200],
    '钢结构单层': [700, 1100],
    '框架多层':   [1300, 1800],
  },
  // 仓库
  warehouse: {
    '单层': [650, 950],
  },
};

// 装修系数
const decorateCoeff = {
  '毛坯': 1.0,
  '简装': 1.2,
  '中档': 1.4,
  '精装': 1.8,
};

// 地区系数
const areaCoeff = {
  '县城':   0.9,
  '地级市': 1.0,
  '二线':   1.1,
  '一线':   1.3,
};

// ============================================================
// 2. 计算函数
// ============================================================

/**
 * 计算工程造价
 * @param {Object} params
 * @param {string} params.buildType   - 建筑类型 key
 * @param {string} params.floorType   - 层数类型 key
 * @param {number} params.area        - 建筑面积 m²
 * @param {string} params.decorate    - 装修标准
 * @param {string} params.areaLevel   - 地区级别
 * @returns {Object} { unitCost[], totalCost[], totalCostWan[] }
 */
function calcTotalCost({
  buildType,
  floorType,
  area,
  decorate = '毛坯',
  areaLevel = '地级市',
}) {
  // 取基础单方区间
  let [minUnit, maxUnit] = costData[buildType]?.[floorType] || [1000, 2000];

  // 乘装修系数
  const dCoeff = decorateCoeff[decorate] || 1.0;
  minUnit *= dCoeff;
  maxUnit *= dCoeff;

  // 乘地区系数
  const aCoeff = areaCoeff[areaLevel] || 1.0;
  minUnit *= aCoeff;
  maxUnit *= aCoeff;

  // 四舍五入
  minUnit = Math.round(minUnit);
  maxUnit = Math.round(maxUnit);

  // 总价
  const minTotal = minUnit * area;
  const maxTotal = maxUnit * area;

  return {
    unitCost: [minUnit, maxUnit],                          // 单方造价
    totalCost: [minTotal, maxTotal],                        // 总造价(元)
    totalCostWan: [
      (minTotal / 10000).toFixed(2),
      (maxTotal / 10000).toFixed(2),
    ],                                                      // 总造价(万元)
  };
}

// ============================================================
// 3. 使用示例
// ============================================================

// 示例：计算无锡7-11层住宅，1000m²，毛坯，地级市
const result = calcTotalCost({
  buildType: 'house',
  floorType: '7_11',
  area: 1000,
  decorate: '毛坯',
  areaLevel: '地级市',
});

console.log('单方造价:', result.unitCost[0], '-', result.unitCost[1], '元/m²');
console.log('总造价:', result.totalCostWan[0], '-', result.totalCostWan[1], '万元');

module.exports = { calcTotalCost, costData, decorateCoeff, areaCoeff };
