"use client"

import {
  Sidebar,
  DashboardHeader,
  AlertBanner,
  MetricCard,
  SmartMoneyValue,
  TrendValue,
  PriceRangeGrid,
  PivotLevels,
  MovingAverages,
  StrategyCard,
  ADXIndicator,
  RSIIndicator,
  ThemeToggle,
} from "@/components/dashboard"

export default function DashboardPage() {
  // Data for the dashboard
  const priceRanges = [
    { label: "Today High", value: "25585.0" },
    { label: "Today Low", value: "25171.35" },
    { label: "Prev High", value: "25653.3" },
    { label: "Prev Low", value: "25494.35" },
  ]

  const pivotLevels = [
    { label: "S2", value: "25418.77" },
    { label: "S1", value: "25502.13" },
    { label: "Pivot", value: "25577.72", isPivot: true },
    { label: "R1", value: "25661.08" },
    { label: "R2", value: "25736.67" },
  ]

  const movingAverages = [
    { period: "10 SMA", value: "25758.01", isPositive: false },
    { period: "20 SMA", value: "25942.5", isPositive: false },
    { period: "50 SMA", value: "25957.89", isPositive: false },
    { period: "100 SMA", value: "25580.12", isPositive: false },
    { period: "200 SMA", value: "25114.03", isPositive: true },
  ]

  const buyTargets = [
    { label: "T1", value: "25643.31" },
    { label: "T2", value: "25683.36" },
    { label: "T3", value: "25723.44" },
    { label: "T4", value: "25763.55" },
    { label: "TARGET 5", value: "25803.7" },
  ]

  const sellTargets = [
    { label: "T1", value: "25512.19" },
    { label: "T2", value: "25472.28" },
    { label: "T3", value: "25432.39" },
    { label: "T4", value: "25392.54" },
    { label: "TARGET 5", value: "25352.72" },
  ]

  return (
    <div className="bg-slate-100 dark:bg-slate-900 text-slate-800 dark:text-slate-100 font-sans transition-colors duration-200 antialiased h-screen flex overflow-hidden">
      <Sidebar />

      <main className="flex-1 flex flex-col h-full overflow-hidden relative">
        <div className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8 space-y-6">
          {/* Header */}
          <DashboardHeader
            symbol="NIFTY 50"
            price="Rs. 25232.5"
            marketStatus="open"
            lastUpdated="10:45:22 AM"
          />

          {/* Alert Banner */}
          <AlertBanner type="sell" message="SELL CONFIRMED" />

          {/* Main Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard label="LTP" value="Rs. 25232.5" />
            <MetricCard
              label="Smart Money"
              value={<SmartMoneyValue status="LONG UNWINDING" />}
              valueClassName=""
            />
            <MetricCard label="VWAP" value="25329.62" />
            <MetricCard
              label="Trend (50 SMA)"
              value={<TrendValue trend="DOWNTREND" description="(Below 50 SMA)" />}
              valueClassName=""
            />
          </div>

          {/* Price Ranges */}
          <PriceRangeGrid levels={priceRanges} />

          {/* Pivot Levels */}
          <PivotLevels levels={pivotLevels} />

          {/* Moving Averages */}
          <MovingAverages averages={movingAverages} />

          {/* Strategy Cards */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <StrategyCard
              type="buy"
              entry="25603.29"
              stopLoss="25577.72"
              targets={buyTargets}
            />
            <StrategyCard
              type="sell"
              entry="25552.14"
              stopLoss="25577.72"
              targets={sellTargets}
            />
          </div>

          {/* Indicators */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <ADXIndicator value={24.65} strength="WEAK" />
            <RSIIndicator value={29.9} status="OVERSOLD (Bounce Expected)" />
          </div>

          {/* Disclaimer */}
          <div className="pt-6 pb-2 text-center md:text-left">
            <p className="text-[10px] text-slate-400 dark:text-slate-500 leading-relaxed">
              IT IS NOT A BUY/SELL RECOMMENDATION. STRICTLY FOR STUDY PURPOSE.{" "}
              <br className="hidden md:inline" />
              CONSULT YOUR FINANCIAL ADVISOR BEFORE TRADING.
            </p>
          </div>
        </div>
      </main>

      <ThemeToggle />
    </div>
  )
}
