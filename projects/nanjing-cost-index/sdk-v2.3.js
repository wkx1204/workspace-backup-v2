/**
 * 工程造价快速估算 SDK v2.3
 * 按南京官方造价指数校准
 * 建筑类型：普通住宅 / 办公楼 / 钢结构厂房(单层)
 * 新增：是否含安装 选项
 * 材料：下跌10%、5% → 持平 → 上涨5%、10%
 */
const CostEstimateSDK = (function() {

 const _costData = {
 建筑: {
 普通住宅: {
 '1-6层': { min: 1500, max: 1800, installMin: 200, installMax: 260 },
 '7-11层': { min: 1800, max: 2100, installMin: 220, installMax: 280 },
 '12-18层': { min: 2100, max: 2400, installMin: 240, installMax: 300 },
 '19-33层': { min: 2300, max: 2600, installMin: 260, installMax: 320 }
 },
 办公楼: {
 '1-6层': { min: 2100, max: 2400, installMin: 280, installMax: 360 },
 '7-11层': { min: 2300, max: 2600, installMin: 300, installMax: 380 },
 '12-18层': { min: 2500, max: 2800, installMin: 320, installMax: 400 },
 '19-33层': { min: 2600, max: 3000, installMin: 340, installMax: 420 }
 },
 钢结构厂房: {
 '单层': { min: 900, max: 1200, installMin: 120, installMax: 180 }
 }
 },

 道路场地: {
 "素混凝土场地10cm": { min: 100, max: 130 },
 "素混凝土场地15cm": { min: 130, max: 160 },
 "钢筋混凝土场地15cm": { min: 160, max: 200 },
 "混凝土道路15cm": { min: 220, max: 260 },
 "混凝土道路20cm": { min: 260, max: 320 },
 "混凝土道路25cm": { min: 300, max: 380 },
 "沥青路面4cm": { min: 220, max: 280 },
 "沥青路面6cm": { min: 280, max: 340 },
 "沥青路面双层8cm": { min: 340, max: 420 }
 }
 };

 const _coeff = {
 decorate: { 毛坯:1.0, 简装:1.2, 中档:1.4, 精装:1.8 },
 area: { 县城:0.9, 地级市:1.0, 二线:1.1, 一线:1.2 },
 year: { "2021年":0.88, "2022年":0.94, "2023年":1.00,
 "2024年":1.05, "2025年":1.10, "2026年":1.15 },
 material: { 
 "下跌10%": 0.90,
 "下跌5%": 0.95,
 "持平": 1.00,
 "上涨5%": 1.05,
 "上涨10%": 1.10
 }
 };

 function _calculate(params) {
 if (!params || !params.projectType || params.square <= 0) return null;

 const {
 projectType, buildType, floor, decorate="毛坯",
 roadType, area, year, material, square,
 includeInstall = false // 新增：是否含安装
 } = params;

 let basePrice;
 if (projectType === "建筑工程") {
 basePrice = _costData.建筑[buildType]?.[floor];
 } else if (projectType === "道路场地工程") {
 basePrice = _costData.道路场地[roadType];
 }
 if (!basePrice) return null;

 const d = projectType === "建筑工程" ? _coeff.decorate[decorate] : 1.0;
 const a = _coeff.area[area] || 1.0;
 const y = _coeff.year[year] || 1.0;
 const m = _coeff.material[material] || 1.0;

 let minUnit, maxUnit;

 if (projectType === "建筑工程") {
 minUnit = basePrice.min * d * a * y * m;
 maxUnit = basePrice.max * d * a * y * m;

 // 含安装则叠加安装费
 if (includeInstall) {
 minUnit += basePrice.installMin * a * y * m;
 maxUnit += basePrice.installMax * a * y * m;
 }
 } else {
 minUnit = basePrice.min * a * y * m;
 maxUnit = basePrice.max * a * y * m;
 }

 minUnit = Math.round(minUnit);
 maxUnit = Math.round(maxUnit);

 const minTotal = Number((minUnit * square / 10000).toFixed(2));
 const maxTotal = Number((maxUnit * square / 10000).toFixed(2));

 return {
 unitPrice: `${minUnit} ~ ${maxUnit} 元/㎡`,
 totalPrice: `${minTotal} ~ ${maxTotal} 万元`
 };
 }

 return {
 calculate: (params) => _calculate(params),

 getOptions: function() {
 return {
 projectTypes: ["建筑工程", "道路场地工程"],
 buildTypes: ["普通住宅", "办公楼", "钢结构厂房"],
 floors: {
 普通住宅: ["1-6层", "7-11层", "12-18层", "19-33层"],
 办公楼: ["1-6层", "7-11层", "12-18层", "19-33层"],
 钢结构厂房: ["单层"]
 },
 decorates: ["毛坯", "简装", "中档", "精装"],
 roadTypes: Object.keys(_costData.道路场地),
 areas: ["县城", "地级市", "二线", "一线"],
 years: ["2021年","2022年","2023年","2024年","2025年","2026年"],
 materials: ["下跌10%", "下跌5%", "持平", "上涨5%", "上涨10%"],
 includeInstallOptions: [true, false] // 安装选项
 };
 },

 version: "v2.3（含安装选项·最终版）"
 };

})();

if (typeof module !== "undefined") module.exports = CostEstimateSDK;
if (typeof window !== "undefined") window.CostEstimateSDK = CostEstimateSDK;
