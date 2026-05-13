# Explainable Battery Engineering AI System (XAI-Battery)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/Model-XGBoost-orange.svg)](https://xgboost.readthedocs.io/)
[![SHAP](https://img.shields.io/badge/XAI-SHAP-red.svg)](https://shap.readthedocs.io/)
[![React](https://img.shields.io/badge/Dashboard-React-61DAFB.svg)](https://reactjs.org/)

## 🔋 프로젝트 개요
본 프로젝트는 NASA Randomized Battery Dataset을 활용하여 리튬 이온 배터리의 잔여 수명(RUL, Remaining Useful Life)을 예측하고, SHAP(Shapley Additive Explanations)을 통해 예측 결과에 대한 공학적 해석을 제공하는 **설명 가능한 배터리 진단 AI 시스템**입니다.

단순한 수명 예측을 넘어, 어떤 물리적 인자(전압 안정성, 온도 상승, 내부 저항 등)가 배터리 열화에 결정적인 영향을 미치는지 분석함으로써 배터리 관리 시스템(BMS)의 신뢰성을 높이는 것을 목표로 합니다.

## 📊 Dataset: NASA PCoE Battery Dataset
- **Data Source**: NASA Ames Prognostics Data Repository
- **Type**: Randomized Discharge Cycles (B0005, B0006, B0007, B0018 등)
- **Features**: 전압(Voltage), 전류(Current), 온도(Temperature), 임피던스(Impedance) 등
- **RUL 정의**: 초기 용량 대비 80% 수준을 수명 종료(EOL)로 정의하고, 현재 시점부터 EOL까지의 상대적 비율(Relative RUL %)을 예측 타겟으로 설정

## 🤖 핵심 기술 스택
### 1. XGBoost Regressor
- 대규모 정형 데이터 처리에 최적화된 Gradient Boosting 모델 사용
- **LOBO (Leave-One-Battery-Out)** 교차 검증을 통해 학습에 사용되지 않은 미지의 배터리에 대한 범용 성능 확보
- 고차원 물리 특성(Voltage Area, Interval Duration 등)을 효과적으로 학습

### 2. SHAP (Explainable AI)
- 예측 결과에 대한 기여도를 정량적으로 분석
- **Global Importance**: 전체 배터리군에서 공통적으로 중요한 열화 지표 식별
- **Local Explanation**: 특정 사이클에서 왜 수명이 급격히 감소했는지에 대한 개별 원인 분석

### 3. Interactive Dashboard
- React & Vite 기반의 실시간 모니터링 인터페이스
- 배터리별 열화 궤적 시각화 및 AI 진단 Insight 제공
- 환경별(상온, 고온, 동적 부하) 배터리 상태 비교 분석

## 📂 프로젝트 구조
```text
data_analysis/
├── data/
│   ├── raw/           # 원본 NASA 데이터셋 (metadata.csv 등)
│   └── processed/     # 전처리된 Feature Dataset 및 결과 CSV
├── src/
│   ├── preprocessing/ # 데이터 로딩 및 특성 추출 (01~04)
│   ├── modeling/      # XGBoost 모델 학습 및 예측 (05)
│   ├── explainability/# SHAP 및 상관관계 분석 (06~07)
│   └── utils/         # 공통 유틸리티 함수
├── results/
│   ├── figures/       # 분석 결과 그래프 (PNG)
│   ├── metrics/       # 모델 성능 지표
│   └── shap/          # SHAP 분석 상세 리포트
├── dashboard/         # React 기반 인터페이스 소스
├── ppt/               # 발표 자료 및 보고서 (pptx)
└── main_model/        # [Legacy] 원본 스크립트 백업
```

## 🚀 실행 방법
### 1. 환경 설정
```bash
# 가상환경 생성 및 라이브러리 설치
uv venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 모델 학습 및 분석
```bash
# 데이터 전처리 및 특성 추출
python src/preprocessing/04_build_dataset.py

# 모델 학습 및 결과 생성
python src/modeling/05_train_xgboost.py

# 설명 가능성(XAI) 분석
python src/explainability/07_shap_analysis.py
```

### 3. 대시보드 실행
```bash
cd dashboard
npm install
npm run dev
```

## 📈 주요 분석 결과
- **예측 성능**: R² Score 0.94 이상 달성 (LOBO 검증 기준)
- **핵심 인사이트**: 전압 Plateau Stability(3.8V-3.5V 구간)의 변화가 배터리 수명 종료를 예측하는 가장 강력한 지표임을 SHAP 분석을 통해 증명

---
© 2026 Battery AI Project Team. All Rights Reserved.
