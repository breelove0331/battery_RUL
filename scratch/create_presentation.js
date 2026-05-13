const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// Colors (No '#' as per guidelines)
const COLORS = {
    BG: "03050D",       // Deep space black
    CYAN: "00C8FF",     // Cyan
    NEON_CYAN: "00FFC8",// Neon Cyan
    TEXT_PRIMARY: "FFFFFF",
    TEXT_DIM: "00C8FF", // Cyan for subtext
    GRID: "00C8FF",     // Grid color
    ACCENT_RED: "FF4500" // For warning/problem
};

const FONT_TITLES = "Arial Black"; // HUD bold feel
const FONT_BODY = "Consolas";      // Monospace for technical feel

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';

// Define Master Slide
pres.defineSlideMaster({
    title: 'HUD_MASTER',
    background: { color: COLORS.BG },
    objects: [
        // Grid background (simulated with lines)
        { line: { x: 0, y: 0, w: 10, h: 0, line: { color: COLORS.GRID, width: 0.5, transparency: 85 } } },
        { line: { x: 0, y: 1.4, w: 10, h: 0, line: { color: COLORS.GRID, width: 0.5, transparency: 85 } } },
        { line: { x: 0, y: 2.8, w: 10, h: 0, line: { color: COLORS.GRID, width: 0.5, transparency: 85 } } },
        { line: { x: 0, y: 4.2, w: 10, h: 0, line: { color: COLORS.GRID, width: 0.5, transparency: 85 } } },
        { line: { x: 0, y: 5.6, w: 10, h: 0, line: { color: COLORS.GRID, width: 0.5, transparency: 85 } } },
        
        { line: { x: 2, y: 0, w: 0, h: 5.6, line: { color: COLORS.GRID, width: 0.5, transparency: 85 } } },
        { line: { x: 4, y: 0, w: 0, h: 5.6, line: { color: COLORS.GRID, width: 0.5, transparency: 85 } } },
        { line: { x: 6, y: 0, w: 0, h: 5.6, line: { color: COLORS.GRID, width: 0.5, transparency: 85 } } },
        { line: { x: 8, y: 0, w: 0, h: 5.6, line: { color: COLORS.GRID, width: 0.5, transparency: 85 } } },

        // Corner brackets
        { shape: pres.shapes.LINE, options: { x: 0.2, y: 0.2, w: 0.3, h: 0, line: { color: COLORS.NEON_CYAN, width: 2 } } },
        { shape: pres.shapes.LINE, options: { x: 0.2, y: 0.2, w: 0, h: 0.3, line: { color: COLORS.NEON_CYAN, width: 2 } } },
        
        { shape: pres.shapes.LINE, options: { x: 9.5, y: 0.2, w: 0.3, h: 0, line: { color: COLORS.NEON_CYAN, width: 2 } } },
        { shape: pres.shapes.LINE, options: { x: 9.8, y: 0.2, w: 0, h: 0.3, line: { color: COLORS.NEON_CYAN, width: 2 } } },
        
        { shape: pres.shapes.LINE, options: { x: 0.2, y: 5.4, w: 0.3, h: 0, line: { color: COLORS.NEON_CYAN, width: 2 } } },
        { shape: pres.shapes.LINE, options: { x: 0.2, y: 5.1, w: 0, h: 0.3, line: { color: COLORS.NEON_CYAN, width: 2 } } },
        
        { shape: pres.shapes.LINE, options: { x: 9.5, y: 5.4, w: 0.3, h: 0, line: { color: COLORS.NEON_CYAN, width: 2 } } },
        { shape: pres.shapes.LINE, options: { x: 9.8, y: 5.1, w: 0, h: 0.3, line: { color: COLORS.NEON_CYAN, width: 2 } } },

        // Footer info
        { text: "XAI ENGINE: ACTIVE // BATTERY DIAGNOSTIC UNIT", options: { x: 0.5, y: 5.3, w: 4, h: 0.3, fontSize: 8, fontFace: FONT_BODY, color: COLORS.TEXT_DIM } },
        { text: "CONFIDENTIAL / SYSTEM MONITORING", options: { x: 7.5, y: 5.3, w: 2, h: 0.3, fontSize: 8, fontFace: FONT_BODY, color: COLORS.TEXT_DIM, align: 'right' } }
    ]
});

// Helper to add Title
function addTitle(slide, title) {
    slide.addText(title.toUpperCase(), { 
        x: 0.5, y: 0.4, w: 9, h: 0.8, 
        fontSize: 32, fontFace: FONT_TITLES, color: COLORS.NEON_CYAN, 
        charSpacing: 2, bold: true 
    });
    // underline HUD style
    slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.1, w: 4, h: 0.05, fill: { color: COLORS.NEON_CYAN } });
    slide.addShape(pres.shapes.RECTANGLE, { x: 4.6, y: 1.1, w: 0.2, h: 0.05, fill: { color: COLORS.NEON_CYAN } });
}

// 1. Title Slide
let s1 = pres.addSlide({ masterName: "HUD_MASTER" });
s1.addText("EXPLAINABLE", { x: 1, y: 1.5, w: 8, h: 1, fontSize: 60, fontFace: FONT_TITLES, color: COLORS.TEXT_PRIMARY, align: 'center', bold: true, charSpacing: 4 });
s1.addText("BATTERY ENGINEERING AI", { x: 1, y: 2.3, w: 8, h: 1, fontSize: 40, fontFace: FONT_TITLES, color: COLORS.NEON_CYAN, align: 'center', bold: true });
s1.addText("Advanced Diagnostic & RUL Prediction Dashboard", { x: 1, y: 3.5, w: 8, h: 0.5, fontSize: 18, fontFace: FONT_BODY, color: COLORS.TEXT_DIM, align: 'center' });
// Circular HUD element in center background
s1.addShape(pres.shapes.OVAL, { x: 3.5, y: 1, w: 3, h: 3, line: { color: COLORS.CYAN, width: 1, transparency: 50 } });
s1.addShape(pres.shapes.OVAL, { x: 3.2, y: 0.7, w: 3.6, h: 3.6, line: { color: COLORS.CYAN, width: 2, transparency: 70, dashType: 'dash' } });

// 2. Problem Definition
let s2 = pres.addSlide({ masterName: "HUD_MASTER" });
addTitle(s2, "01. Problem Definition");
s2.addText([
    { text: "Battery Degradation Complexity", options: { bullet: true, breakLine: true, fontSize: 24, bold: true, color: COLORS.TEXT_PRIMARY } },
    { text: "  Non-linear electrochemical aging mechanisms", options: { breakLine: true, fontSize: 16, color: COLORS.TEXT_DIM } },
    { text: "Predictive Maintenance Criticality", options: { bullet: true, breakLine: true, fontSize: 24, bold: true, color: COLORS.TEXT_PRIMARY } },
    { text: "  Preventing sudden system failures in EV/ESS", options: { breakLine: true, fontSize: 16, color: COLORS.TEXT_DIM } },
    { text: "Black-box Model Limitation", options: { bullet: true, breakLine: true, fontSize: 24, bold: true, color: COLORS.TEXT_PRIMARY } },
    { text: "  Standard DL models lack 'Reasoning' for engineers", options: { fontSize: 16, color: COLORS.TEXT_DIM } }
], { x: 0.5, y: 1.5, w: 5, h: 3.5, fontFace: FONT_BODY });
// Add an icon or abstract graph
s2.addShape(pres.shapes.RECTANGLE, { x: 6, y: 1.5, w: 3.5, h: 3, fill: { color: "1A1A2E" }, line: { color: COLORS.ACCENT_RED, width: 2 } });
s2.addText("RELIABILITY GAP", { x: 6, y: 2.5, w: 3.5, h: 0.5, align: 'center', color: COLORS.ACCENT_RED, fontSize: 20, bold: true });

// 3. Project Goal
let s3 = pres.addSlide({ masterName: "HUD_MASTER" });
addTitle(s3, "02. Project Goal");
s3.addText("Explainable Monitoring & Diagnostic System", { x: 0.5, y: 1.5, w: 9, h: 0.5, fontSize: 24, fontFace: FONT_TITLES, color: COLORS.TEXT_PRIMARY });
const goalItems = [
    { title: "RUL PREDICTION", desc: "Accurate remaining life estimation using XGBoost" },
    { title: "XAI INTERPRETATION", desc: "Feature-level attribution via SHAP values" },
    { title: "ENGINEERING UI", desc: "Actionable dashboard for maintenance decisions" }
];
goalItems.forEach((item, idx) => {
    let y = 2.2 + (idx * 1.0);
    s3.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: y, w: 0.1, h: 0.8, fill: { color: COLORS.NEON_CYAN } });
    s3.addText(item.title, { x: 0.7, y: y, w: 3, h: 0.3, fontSize: 18, bold: true, color: COLORS.NEON_CYAN });
    s3.addText(item.desc, { x: 0.7, y: y + 0.3, w: 8, h: 0.3, fontSize: 14, color: COLORS.TEXT_PRIMARY });
});

// 4. Dataset
let s4 = pres.addSlide({ masterName: "HUD_MASTER" });
addTitle(s4, "03. NASA Battery Dataset");
s4.addText([
    { text: "Target Unit:", options: { bold: true, color: COLORS.NEON_CYAN, breakLine: true } },
    { text: "Li-ion 18650 cells (NASA Prognostics Center)", options: { breakLine: true } },
    { text: "Temperature Conditions:", options: { bold: true, color: COLORS.NEON_CYAN, breakLine: true } },
    { text: "4°C, 24°C, 43°C (Varying degradation rates)", options: { breakLine: true } },
    { text: "Cycle Data:", options: { bold: true, color: COLORS.NEON_CYAN, breakLine: true } },
    { text: "Charging/Discharging cycles until EOL (70% capacity)" }
], { x: 0.5, y: 1.5, w: 5, h: 3.5, fontFace: FONT_BODY, color: COLORS.TEXT_PRIMARY, fontSize: 16 });

s4.addTable([
    ["ID", "Temp", "Cycles"],
    ["B0005", "24°C", "168"],
    ["B0006", "24°C", "168"],
    ["B0029", "44°C", "40"],
    ["B0032", "44°C", "10"]
], { x: 6, y: 1.5, w: 3.5, color: COLORS.TEXT_PRIMARY, fontSize: 14, fontFace: FONT_BODY, border: { color: COLORS.CYAN, width: 1 } });

// 5. Pipeline
let s5 = pres.addSlide({ masterName: "HUD_MASTER" });
addTitle(s5, "04. System Pipeline");
const steps = ["RAW DATA", "FEATURE ENG", "XGBOOST", "SHAP XAI", "DASHBOARD"];
steps.forEach((step, idx) => {
    let x = 0.5 + (idx * 1.9);
    s5.addShape(pres.shapes.RECTANGLE, { x: x, y: 2.5, w: 1.6, h: 1, fill: { color: "1A1A2E" }, line: { color: COLORS.NEON_CYAN, width: 1 } });
    s5.addText(step, { x: x, y: 2.5, w: 1.6, h: 1, align: 'center', valign: 'middle', fontSize: 12, bold: true, color: COLORS.NEON_CYAN });
    if (idx < steps.length - 1) {
        s5.addShape(pres.shapes.LINE, { x: x + 1.6, y: 3, w: 0.3, h: 0, line: { color: COLORS.NEON_CYAN, width: 1 } });
    }
});

// 6. Feature Engineering
let s6 = pres.addSlide({ masterName: "HUD_MASTER" });
addTitle(s6, "05. Engineering Signals");
s6.addText("Extracting Key Electrochemical Indicators", { x: 0.5, y: 1.3, w: 9, h: 0.4, fontSize: 16, color: COLORS.TEXT_DIM });
const features = [
    { name: "VOLTAGE PLATEAU", desc: "Time interval in specific voltage range (3.8V-3.5V)" },
    { name: "INTERNAL IMPEDANCE", desc: "Derived from delta V/I during pulse load" },
    { name: "CHARGE AREA", desc: "Integration of voltage curve during CC phase" },
    { name: "PEAK TEMP", desc: "Thermal stability during discharge cycle" }
];
features.forEach((f, idx) => {
    let y = 1.8 + (idx * 0.9);
    s6.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: y, w: 9, h: 0.7, fill: { color: "112233", transparency: 50 }, line: { color: COLORS.CYAN, width: 0.5 } });
    s6.addText(f.name, { x: 0.7, y: y + 0.1, w: 3, h: 0.3, fontSize: 16, bold: true, color: COLORS.NEON_CYAN });
    s6.addText(f.desc, { x: 0.7, y: y + 0.35, w: 8, h: 0.2, fontSize: 12, color: COLORS.TEXT_PRIMARY });
});

// 7. Model Result
let s7 = pres.addSlide({ masterName: "HUD_MASTER" });
addTitle(s7, "06. XGBoost Prediction Results");
s7.addText("High Precision RUL Estimation", { x: 0.5, y: 1.3, w: 9, h: 0.4, fontSize: 16, color: COLORS.TEXT_DIM });

s7.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 2, w: 4, h: 3, fill: { color: "0A1A2E" }, line: { color: COLORS.NEON_CYAN, width: 1 } });
s7.addText("MODEL METRICS", { x: 0.5, y: 2.2, w: 4, h: 0.4, align: 'center', fontSize: 18, bold: true, color: COLORS.NEON_CYAN });
s7.addText([
    { text: "R² Score: 0.942", options: { breakLine: true, fontSize: 24, bold: true, color: COLORS.TEXT_PRIMARY } },
    { text: "MAE: 5.64%", options: { breakLine: true, fontSize: 24, bold: true, color: COLORS.TEXT_PRIMARY } },
    { text: "Stability: HIGH", options: { fontSize: 18, color: COLORS.NEON_CYAN } }
], { x: 1, y: 2.8, w: 3, h: 1.5, align: 'center' });

s7.addText("Target: Cycle-by-cycle Relative RUL (100% → 0%)", { x: 5, y: 2, w: 4.5, h: 3, fontSize: 14, color: COLORS.TEXT_PRIMARY, fontFace: FONT_BODY });
s7.addShape(pres.shapes.LINE, { x: 5, y: 4, w: 4.5, h: -1, line: { color: COLORS.ACCENT_RED, width: 2, dashType: 'dash' } });
s7.addText("Degradation Trajectory", { x: 5, y: 4.2, w: 4.5, h: 0.3, fontSize: 10, color: COLORS.TEXT_DIM });

// 8. SHAP Explainability
let s8 = pres.addSlide({ masterName: "HUD_MASTER" });
addTitle(s8, "07. SHAP Explainability");
s8.addImage({ path: "C:\\Users\\View\\.gemini\\antigravity\\brain\\0e2452db-d670-4ed4-955f-48ba27616724\\shap_ai_interpretation_view_1778476739297.png", x: 0.5, y: 1.5, w: 4.5, h: 3.5 });
s8.addText([
    { text: "Key Insights:", options: { bold: true, color: COLORS.NEON_CYAN, breakLine: true } },
    { text: "interval_38_35 is the most critical signal for RUL prediction.", options: { bullet: true, breakLine: true } },
    { text: "Voltage Plateau collapse directly correlates with capacity loss.", options: { bullet: true, breakLine: true } },
    { text: "Local fluctuations (Impedance) reflect early-stage SEI growth.", options: { bullet: true } }
], { x: 5.2, y: 1.5, w: 4.3, h: 3.5, fontSize: 16, color: COLORS.TEXT_PRIMARY, fontFace: FONT_BODY });

// 9. Dashboard Demo
let s9 = pres.addSlide({ masterName: "HUD_MASTER" });
addTitle(s9, "08. Interactive Dashboard");
s9.addImage({ path: "C:\\Users\\View\\.gemini\\antigravity\\brain\\0e2452db-d670-4ed4-955f-48ba27616724\\dashboard_full_view_1778476697132.png", x: 0.5, y: 1.5, w: 6.5, h: 3.8 });
s9.addText([
    { text: "MAIN FEATURES:", options: { bold: true, color: COLORS.NEON_CYAN, breakLine: true } },
    { text: "1. Cycle Slider: Time-based tracking", options: { breakLine: true } },
    { text: "2. Impedance Sync: Logical consistency", options: { breakLine: true } },
    { text: "3. Actionable AI: Replacement alerts", options: { breakLine: true } }
], { x: 7.2, y: 1.5, w: 2.5, h: 3.5, fontSize: 12, color: COLORS.TEXT_PRIMARY, fontFace: FONT_BODY });

// 10. Conclusion
let s10 = pres.addSlide({ masterName: "HUD_MASTER" });
addTitle(s10, "09. Conclusion & Industry Impact");
const impactItems = [
    { t: "EV ECOSYSTEM", d: "Precise RUL for battery second-life assessment" },
    { t: "SMART FACTORY", d: "Predictive maintenance for AGV/Robotics" },
    { t: "ENERGY STORAGE", d: "Safety monitoring and fire prevention" }
];
impactItems.forEach((item, idx) => {
    let y = 1.8 + (idx * 1.1);
    s10.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: y, w: 9, h: 0.9, fill: { color: COLORS.CYAN, transparency: 90 }, line: { color: COLORS.NEON_CYAN, width: 1 } });
    s10.addText(item.t, { x: 0.7, y: y + 0.1, w: 3, h: 0.3, fontSize: 20, bold: true, color: COLORS.NEON_CYAN });
    s10.addText(item.d, { x: 0.7, y: y + 0.45, w: 8, h: 0.3, fontSize: 14, color: COLORS.TEXT_PRIMARY });
});

// Final Slide
let s11 = pres.addSlide({ masterName: "HUD_MASTER" });
s11.addText("THANK YOU", { x: 1, y: 2, w: 8, h: 1, fontSize: 60, fontFace: FONT_TITLES, color: COLORS.NEON_CYAN, align: 'center', bold: true, charSpacing: 10 });
s11.addText("Q & A // Explainable Battery AI System", { x: 1, y: 3, w: 8, h: 0.5, fontSize: 18, fontFace: FONT_BODY, color: COLORS.TEXT_DIM, align: 'center' });

pres.writeFile({ fileName: "Battery_Engineering_AI_Presentation.pptx" }).then(fileName => {
    console.log(`Created file: ${fileName}`);
});
