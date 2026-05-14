import React, { useState, useEffect, useMemo } from 'react'
import './index.css'
import batteryFullData from './battery_full_data.json'
import localShapImportance from './local_shap_importance.json'
import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
  ReferenceLine,
  ReferenceDot
} from 'recharts'

const ENV_MAP = {
  'Room Temperature (24°C)': ['B0005', 'B0006', 'B0007', 'B0018'],
  'Dynamic Load': ['B0025', 'B0026', 'B0027', 'B0028'],
  'High Temperature (44°C)': ['B0029', 'B0030', 'B0031', 'B0032']
}

const ENV_SPECS = {
  'Room Temperature (24°C)': {
    characteristics: 'Standard Electrochemical Reaction (표준 전기화학 반응)',
    riskFactor: 'Stable SEI Growth',
    monitoredSignals: ['Voltage Stability', 'Internal Resistance']
  },
  'Dynamic Load': {
    characteristics: 'Irregular Ion Transport (불규칙한 이온 이동)',
    riskFactor: 'Localized Overpotential',
    monitoredSignals: ['Dynamic Voltage Drop', 'Current Stress']
  },
  'High Temperature (44°C)': {
    characteristics: 'Accelerated Side Reactions (가속화된 부반응)',
    riskFactor: 'Thermal Aging & Plateau Collapse',
    monitoredSignals: ['Temperature Rise', 'Rapid Impedance Gain']
  }
}

const FEATURE_MEANINGS = {
  'interval_38_35': 'Voltage Plateau Stability Duration',
  'area_38_35': 'High Voltage Energy Capacity',
  'area_35_32': 'Low Voltage Energy Capacity',
  'max_temperature': 'Peak Thermal Stress',
  'discharge_duration': 'Active Material Sustainability',
  'dvdt_35': 'Voltage Decay Gradient',
  'Rct': 'Charge Transfer Impedance',
  'Re': 'Electrolyte Resistance',
  'mean_internal_resistance': 'Internal Impedance Rise',
  'mean_current': 'Operational Load Stress',
  'voltage_slope': 'Electrochemical Stability Decay',
  'temperature_rise': 'Exothermic Degradation Rate'
}

function App() {
  const [selectedEnv, setSelectedEnv] = useState(Object.keys(ENV_MAP)[0])
  const [selectedId, setSelectedId] = useState(ENV_MAP[Object.keys(ENV_MAP)[0]][0])
  const [currentCycle, setCurrentCycle] = useState(0)
  const [currentBattery, setCurrentBattery] = useState(null)
  const [degradationRate, setDegradationRate] = useState(0)
  const [currentTime, setCurrentTime] = useState(new Date().toLocaleTimeString())

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date().toLocaleTimeString()), 1000)
    return () => clearInterval(timer)
  }, [])

  const batteryHistory = useMemo(() => batteryFullData[selectedId] || [], [selectedId])
  const minCycle = useMemo(() => batteryHistory.length > 0 ? batteryHistory[0].cycle : 1, [batteryHistory])
  const maxCycle = useMemo(() => batteryHistory.length > 0 ? batteryHistory[batteryHistory.length - 1].cycle : 1, [batteryHistory])

  const fleetBenchmark = useMemo(() => {
    const cycleMap = {}
    Object.values(batteryFullData).forEach(list => list.forEach(d => {
      if (!cycleMap[d.cycle]) cycleMap[d.cycle] = []
      cycleMap[d.cycle].push(d.Relative_RUL)
    }))
    return Object.fromEntries(Object.entries(cycleMap).map(([c, v]) => [c, v.reduce((a, b) => a + b, 0) / v.length]))
  }, [])

  // 환경 변경 시 해당 환경의 첫 번째 배터리로 자동 전환
  useEffect(() => {
    if (ENV_MAP[selectedEnv]) {
      const validIds = ENV_MAP[selectedEnv]
      if (!validIds.includes(selectedId)) {
        setSelectedId(validIds[0])
      }
    }
  }, [selectedEnv, selectedId])

  // 배터리(ID) 변경 시 사이클을 해당 배터리의 시작 시점으로 초기화
  useEffect(() => {
    setCurrentCycle(minCycle)
  }, [selectedId, minCycle])

  useEffect(() => {
    const battery = [...batteryHistory].reverse().find(b => b.cycle <= currentCycle) || batteryHistory[0]
    if (battery) {
      setCurrentBattery(battery)
      const idx = batteryHistory.findIndex(b => b.cycle === battery.cycle)
      if (idx > 2) {
        setDegradationRate((battery.Relative_RUL - batteryHistory[idx-3].Relative_RUL) / (battery.cycle - batteryHistory[idx-3].cycle))
      } else {
        setDegradationRate(0)
      }
    }
  }, [currentCycle, batteryHistory])

  const initialImpedance = useMemo(() => batteryHistory.length > 0 ? batteryHistory[0].Rct + batteryHistory[0].Re : 0, [batteryHistory])
  const localImportanceData = useMemo(() => (localShapImportance[selectedId] || []).slice(0, 5), [selectedId])

  if (!currentBattery) return <div className="loading">Initializing Predictive Maintenance System...</div>

  const getRiskAssessment = (rul, velocity, impGrowth, benchmarkDiff, env) => {
    let rank = 0;
    let reasons = [];

    // 1. Base Risk (Strictly by Relative RUL)
    if (rul > 70) rank = 0;      // LOW
    else if (rul > 40) rank = 1; // MODERATE
    else if (rul > 20) rank = 2; // HIGH
    else rank = 3;               // CRITICAL

    // 2. Monitoring Observations (Insight only, does not affect rank)
    if (env.includes('High Temperature')) {
      reasons.push("High Temperature Operating Environment (고온 운영 환경)");
    }
    if (impGrowth > 5) {
      reasons.push("Significant Impedance Growth (>5%) (임피던스 급증)");
    }
    if (Math.abs(velocity) > 1.2) {
      reasons.push("Accelerated Degradation Velocity (열화 속도 가속)");
    }
    if (benchmarkDiff < -10) {
      reasons.push("Fleet Benchmark Variance Detected (동일 환경 대비 편차)");
    }

    const levels = [
      { level: 'LOW', color: '#10b981', priority: 'LOW', timing: 'Routine Check', label: '안정 상태' },
      { level: 'MODERATE', color: '#f59e0b', priority: 'MEDIUM', timing: 'Next 50 Cycles', label: '주의 상태' },
      { level: 'HIGH', color: '#f97316', priority: 'HIGH', timing: 'Immediate Inspection', label: '경고 상태' },
      { level: 'CRITICAL', color: '#ef4444', priority: 'CRITICAL', timing: 'ASAP Replacement', label: '위험 상태' }
    ];

    return { ...levels[rank], reasons };
  }

  const currentImp = currentBattery.Rct + currentBattery.Re
  const impGrowth = initialImpedance > 0 ? ((currentImp - initialImpedance) / initialImpedance) * 100 : 0
  const currentAvgRul = fleetBenchmark[currentCycle] || currentBattery.Relative_RUL
  const benchmarkDiff = currentBattery.Relative_RUL - currentAvgRul
  
  const risk = getRiskAssessment(currentBattery.Relative_RUL, degradationRate, impGrowth, benchmarkDiff, selectedEnv)
  
  const getPrescriptiveAdvisory = () => {
    const topFeat = localImportanceData[0]?.Feature
    const meaning = FEATURE_MEANINGS[topFeat] || topFeat
    
    if (risk.level === 'LOW') {
      return {
        action: "현 운영 파라미터 최적화 상태 유지",
        strategy: "Standard Cycle Protocol 적용 및 데이터 로깅 지속",
        priority: "정기 점검 (Level 3)"
      }
    } else if (risk.level === 'MODERATE') {
      return {
        action: `${meaning} 변동 감지. 열화 가속 주의`,
        strategy: "High C-rate 충전 빈도 20% 감소 권고",
        priority: "주의 관찰 (Level 2)"
      }
    } else {
      return {
        action: "예측 수명 급감 및 안전 임계치 도달",
        strategy: "운전 부하 0.5C 제한 및 냉각 시스템 강제 가동",
        priority: "긴급 점검 (Level 1)"
      }
    }
  }

  const advisory = getPrescriptiveAdvisory()

  return (
    <div className="app-container">
      <aside className="sidebar">
        <h2>PBM-X1 <span style={{fontSize: '0.6rem', opacity: 0.5, fontWeight: 400}}>PREDICTIVE SYSTEM</span></h2>
        <div className="selector-group">
          <div className="selector-item">
            <label>Operating Environment</label>
            <select value={selectedEnv} onChange={(e) => setSelectedEnv(e.target.value)}>
              {Object.keys(ENV_MAP).map(env => <option key={env} value={env}>{env}</option>)}
            </select>
          </div>
          <div className="selector-item">
            <label>Active Asset ID</label>
            <select value={selectedId} onChange={(e) => setSelectedId(e.target.value)}>
               {ENV_MAP[selectedEnv].map(id => <option key={id} value={id}>{id}</option>)}
            </select>
          </div>
          <div className="selector-item" style={{marginTop: '1rem'}}>
            <label>Analysis Timeline (Cycle)</label>
            <div style={{fontSize: '1.5rem', fontWeight: 900, color: 'var(--accent-color)'}}>{currentCycle}</div>
            <input type="range" min={minCycle} max={maxCycle} value={currentCycle} onChange={(e) => setCurrentCycle(parseInt(e.target.value))} className="cycle-slider" />
          </div>
        </div>
        <div style={{marginTop: 'auto', borderTop: '1px solid #1e293b', paddingTop: '1rem'}}>
          <div className="status-indicator"><div className="heartbeat"></div> SYSTEM LIVE</div>
          <div style={{fontSize: '0.65rem', color: '#64748b', marginTop: '0.5rem'}}>{currentTime} | {selectedId} CONNECTED</div>
        </div>
      </aside>

      <main className="main-content">
        <header className="header">
          <div>
            <h1>Predictive Maintenance Monitoring System</h1>
            <p>Fleet-wide Intelligent Battery Asset Management</p>
          </div>
          <div style={{textAlign: 'right'}}>
            <div style={{fontSize: '0.7rem', color: '#64748b', fontWeight: 800, marginBottom: '0.2rem'}}>SYSTEM RISK ASSESSMENT</div>
            <div style={{fontSize: '1.8rem', fontWeight: 950, color: risk.color, textShadow: `0 0 20px ${risk.color}44`}}>
              {risk.level} <span style={{fontSize: '1.2rem', fontWeight: 700, opacity: 0.8}}>({risk.label})</span>
            </div>
            <div style={{marginTop: '0.5rem', display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '0.2rem'}}>
              {risk.reasons.map((reason, idx) => (
                <div key={idx} style={{fontSize: '0.65rem', color: risk.color, opacity: 0.9, fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.4rem'}}>
                   <div style={{width: '4px', height: '4px', borderRadius: '50%', background: risk.color}}></div>
                   {reason}
                </div>
              ))}
              {risk.reasons.length === 0 && <div style={{fontSize: '0.65rem', color: '#64748b'}}>No critical penalty detected</div>}
            </div>
          </div>
        </header>

        <section className="summary-grid">
          <div className="card">
            <div className="card-title">REMAINING USEFUL LIFE (RUL)</div>
            <div className="card-value" style={{color: risk.color}}>{currentBattery.Relative_RUL.toFixed(1)}%</div>
            <div style={{fontSize: '0.7rem', color: '#64748b', fontWeight: 600}}>현재 용량 기준 남은 사용 가능 수명</div>
          </div>
          <div className="card">
            <div className="card-title">Impedance Growth <span className="priority-tag priority-medium">ΔZ</span></div>
            <div className="card-value">{impGrowth >= 0 ? '+' : ''}{impGrowth.toFixed(1)}%</div>
            <div style={{fontSize: '0.7rem', color: '#64748b', fontWeight: 600}}>{currentImp.toFixed(4)} Ω (Initial 대비 증가율)</div>
          </div>
          <div className="card">
            <div className="card-title">Degradation Velocity <span className="priority-tag priority-high">Rate</span></div>
            <div className="card-value" style={{color: Math.abs(degradationRate) > 1.0 ? '#ef4444' : '#fff'}}>
              {Math.abs(degradationRate).toFixed(3)}
            </div>
            <div style={{fontSize: '0.7rem', color: '#64748b', fontWeight: 600}}>% RUL Loss Per Cycle</div>
          </div>
          <div className="card">
            <div className="card-title">Fleet Benchmark <span className="priority-tag priority-low">Global</span></div>
            <div className="card-value" style={{color: benchmarkDiff < -1 ? '#ef4444' : '#10b981'}}>
              {benchmarkDiff > 0 ? '+' : ''}{benchmarkDiff.toFixed(1)}%
            </div>
            <div style={{fontSize: '0.7rem', color: '#64748b', fontWeight: 600}}>동일 환경 평균 대비 수명 격차</div>
          </div>
        </section>

        <div className="control-panel">
          <section className="prescriptive-card">
            <div className="action-item">
              <div className="action-label">Recommended Action (권고 조치)</div>
              <div className="action-content" style={{color: 'var(--accent-color)', fontSize: '1.4rem'}}>{advisory.action}</div>
            </div>
            <div className="action-item">
              <div className="action-label">Operation Strategy (운용 전략)</div>
              <div className="action-content">{advisory.strategy}</div>
            </div>
            <div style={{display: 'flex', gap: '3rem'}}>
              <div>
                <div className="action-label">Inspection Priority</div>
                <div style={{fontSize: '1.2rem', fontWeight: 900, color: risk.color}}>{advisory.priority}</div>
              </div>
              <div>
                <div className="action-label">Maintenance Timing</div>
                <div style={{fontSize: '1.2rem', fontWeight: 900}}>{risk.timing}</div>
              </div>
            </div>
          </section>

          <section className="card" style={{justifyContent: 'center', background: 'rgba(15, 23, 42, 0.3)'}}>
            <div className="card-title">Environment Insights</div>
            <div style={{marginBottom: '1.5rem'}}>
              <div style={{fontSize: '1rem', fontWeight: 800, color: 'var(--accent-color)'}}>{ENV_SPECS[selectedEnv].characteristics}</div>
              <div style={{fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.4rem'}}>열화 주관 인자: {ENV_SPECS[selectedEnv].riskFactor}</div>
            </div>
            <div style={{display: 'flex', flexWrap: 'wrap', gap: '0.75rem'}}>
              {ENV_SPECS[selectedEnv].monitoredSignals.map(s => (
                <div key={s} style={{padding: '0.4rem 0.8rem', border: '1px solid #1e293b', borderRadius: '6px', fontSize: '0.65rem', fontWeight: 900, color: 'var(--accent-color)'}}>
                  {s.toUpperCase()} MONITORING
                </div>
              ))}
            </div>
          </section>
        </div>

        <section className="chart-container">
          <div className="chart-header">
            <h3>Predictive Lifetime Trajectory (Relative RUL)</h3>
            <div style={{fontSize: '0.7rem', color: '#64748b', fontWeight: 700}}>* 95% Confidence Shading Applied</div>
          </div>
          <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
              <AreaChart data={batteryHistory}>
                <defs>
                  <linearGradient id="colorRul" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#22d3ee" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} opacity={0.3} />
                <XAxis dataKey="cycle" stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} tick={{fontWeight: 600}}/>
                <YAxis stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} domain={[0, 100]} tick={{fontWeight: 600}}/>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', boxShadow: '0 10px 30px rgba(0,0,0,0.5)' }}
                  itemStyle={{ color: '#22d3ee', fontWeight: 800 }}
                />
                <Area type="monotone" dataKey={(d) => [Math.max(0, d.Relative_RUL - 5), d.Relative_RUL + 5]} stroke="none" fill="#22d3ee" fillOpacity={0.05} />
                <Area type="monotone" dataKey="Relative_RUL" stroke="#22d3ee" strokeWidth={4} fill="url(#colorRul)" isAnimationActive={false} />
                <ReferenceLine x={currentCycle} stroke="#ef4444" strokeWidth={2} strokeDasharray="5 5" />
                <ReferenceDot x={currentCycle} y={currentBattery.Relative_RUL} r={7} fill="#ef4444" stroke="#fff" strokeWidth={3} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="card">
          <div className="card-title">Explainable AI: Degradation Fingerprint (SHAP)</div>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Priority</th>
                  <th>Feature Signal</th>
                  <th>Maintenance Impact</th>
                  <th>Engineering Interpretation (현상 분석)</th>
                </tr>
              </thead>
              <tbody>
                {localImportanceData.map((f, i) => (
                  <tr key={i}>
                    <td><div className={`priority-tag ${i < 2 ? 'priority-high' : 'priority-medium'}`}>{i < 2 ? 'CRITICAL' : 'OBSERVE'}</div></td>
                    <td style={{fontWeight: 800, fontSize: '0.95rem'}}>{f.Feature}</td>
                    <td style={{width: '250px'}}>
                      <div className="importance-bar-bg">
                        <div className="importance-bar-fill" style={{width: `${(f.Mean_SHAP_Importance / localImportanceData[0].Mean_SHAP_Importance) * 100}%`}}></div>
                      </div>
                    </td>
                    <td style={{fontSize: '0.8rem', color: 'var(--accent-color)', fontWeight: 700}}>
                      {FEATURE_MEANINGS[f.Feature] || 'Complex System Interaction'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
