/**
 * 工程造价估算 SDK v3.0（南京官方材料年度系数·最终终极版）
 * 数据来源：南京市工程造价信息网 2020-2026 材料信息价
 * 包含：钢筋、水泥、混凝土、黄砂、碎石、木材 综合加权
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

 // =============================
 // 南京官方 2020-2026 材料综合系数（真实加权）
 // =============================
 yearMaterial: {
 "2020年": 0.84,
 "2021年": 1.20,
 "2022年": 1.13,
 "2023年": 1.00,
 "2024年": 1.06,
 "2025年": 1.10,
 "2026年": 1.13
 },

 // 手动行情波动（±5%、±10%）
 materialWave: {
 "下跌10%": 0.90,
 "下跌5%": 0.95,
 "持平": 1.00,
 "上涨5%": 1.05,
 "上涨10%": 1.10
 }
 };

 function _calculate(params) {
 const {
 projectType, buildType, floor, decorate="毛坯",
 roadType, area, year, materialWave, square,
 includeInstall = false
 } = params;

 let basePrice;
 if (projectType === "建筑工程") {
 basePrice = _costData.建筑[buildType]?.[floor];
 } else {
 basePrice = _costData.道路场地[roadType];
 }
 if (!basePrice) return null;

 const d = projectType === "建筑工程" ? _coeff.decorate[decorate] : 1.0;
 const a = _coeff.area[area] || 1.0;
 const y = _coeff.yearMaterial[year] || 1.00;
 const w = _coeff.materialWave[materialWave] || 1.00;

 let minUnit, maxUnit;

 if (projectType === "建筑工程") {
 minUnit = basePrice.min * d * a * y * w;
 maxUnit = basePrice.max * d * a * y * w;
 if (includeInstall) {
 minUnit += basePrice.installMin * a * y * w;
 maxUnit += basePrice.installMax * a * y * w;
 }
 } else {
 minUnit = basePrice.min * a * y * w;
 maxUnit = basePrice.max * a * y * w;
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
 calculate: _calculate,
 getOptions: () => ({
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
 years: ["2020年","2021年","2022年","2023年","2024年","2025年","2026年"],
 materialWaves: ["下跌10%", "下跌5%", "持平", "上涨5%", "上涨10%"],
 installOptions: ["含安装", "不含安装"]
 }),
 version: "v3.0（南京官方材料系数·终极版）"
 };
})();

// 导出
if (typeof module !== "undefined") module.exports = CostEstimateSDK;
if (typeof window !== "undefined") window.CostEstimateSDK = CostEstimateSDK;
