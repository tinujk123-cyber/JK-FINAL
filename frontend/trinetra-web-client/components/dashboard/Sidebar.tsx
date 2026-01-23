import { Settings, SlidersHorizontal, Search, RefreshCw, Radar, TrendingUp, TrendingDown, ArrowUpDown } from "lucide-react"

export function Sidebar() {
  return (
    <aside className="w-72 bg-white dark:bg-slate-800 border-r border-slate-200 dark:border-slate-700 flex flex-col shadow-xl z-20 shrink-0">
      {/* Logo Section */}
      <div className="p-6 border-b border-slate-100 dark:border-slate-700/50">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded bg-indigo-600 flex items-center justify-center text-white font-bold text-lg shadow-lg shadow-indigo-600/30">
            T
          </div>
          <h1 className="text-xl font-bold tracking-tight text-slate-900 dark:text-white">
            JK TRINETRA
          </h1>
        </div>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 font-medium tracking-wide">
          PRO TRADING TERMINAL
        </p>
      </div>

      {/* Controls Section */}
      <div className="p-5 flex-1 overflow-y-auto space-y-8">
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
            <SlidersHorizontal className="h-4 w-4" />
            Controls
          </div>

          {/* Select List */}
          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-600 dark:text-slate-300 ml-1">
              Select List
            </label>
            <div className="relative">
              <select
                aria-label="Select trading list"
                className="w-full bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-600 rounded-lg py-2.5 px-3 text-sm focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600 dark:text-slate-200 shadow-sm appearance-none"
              >
                <option>NIFTY 50</option>
                <option>BANK NIFTY</option>
                <option>FINNIFTY</option>
              </select>
              <svg
                className="absolute right-3 top-3 h-4 w-4 text-slate-400 pointer-events-none"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </div>
          </div>

          {/* Symbol Search */}
          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-600 dark:text-slate-300 ml-1">
              Symbol Search
            </label>
            <div className="relative">
              <input
                type="text"
                placeholder="Ex: TRENT"
                className="w-full bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-600 rounded-lg py-2.5 pl-3 pr-10 text-sm focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600 dark:text-slate-200 shadow-sm placeholder-slate-400"
              />
              <Search className="absolute right-3 top-2.5 h-4 w-4 text-slate-400" />
            </div>
          </div>

          {/* Refresh Button */}
          <button className="w-full flex items-center justify-center gap-2 bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 font-semibold py-2.5 rounded-lg transition-all text-sm border border-slate-200 dark:border-slate-600">
            <RefreshCw className="h-4 w-4" />
            Refresh Data
          </button>
        </div>

        {/* Manual Scanner Section */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
            <Radar className="h-4 w-4" />
            Manual Scanner
          </div>

          <div className="grid grid-cols-2 gap-3">
            <button className="flex flex-col items-center justify-center gap-1 bg-emerald-50 dark:bg-emerald-900/20 hover:bg-emerald-100 dark:hover:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400 font-medium py-3 rounded-lg border border-emerald-200 dark:border-emerald-800/50 transition-all text-xs">
              <TrendingUp className="h-5 w-5" />
              BUY SCAN
            </button>
            <button className="flex flex-col items-center justify-center gap-1 bg-rose-50 dark:bg-rose-900/20 hover:bg-rose-100 dark:hover:bg-rose-900/30 text-rose-700 dark:text-rose-400 font-medium py-3 rounded-lg border border-rose-200 dark:border-rose-800/50 transition-all text-xs">
              <TrendingDown className="h-5 w-5" />
              SELL SCAN
            </button>
          </div>

          <button className="w-full flex items-center justify-center gap-2 bg-amber-50 dark:bg-amber-900/20 hover:bg-amber-100 dark:hover:bg-amber-900/30 text-amber-700 dark:text-amber-400 font-medium py-2.5 rounded-lg border border-amber-200 dark:border-amber-800/50 transition-all text-xs">
            <ArrowUpDown className="h-4 w-4" />
            REVERSAL SCAN
          </button>
        </div>
      </div>

      {/* User Profile Section */}
      <div className="p-4 border-t border-slate-100 dark:border-slate-700/50 bg-slate-50 dark:bg-slate-800/50">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-linear-to-tr from-indigo-600 to-purple-500 flex items-center justify-center text-white text-xs font-bold">
            JK
          </div>
          <div className="flex-1">
            <p className="text-sm font-semibold text-slate-900 dark:text-white">
              User Account
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Pro Plan Active
            </p>
          </div>
          <button
            aria-label="User settings"
            className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
          >
            <Settings className="h-5 w-5" />
          </button>
        </div>
      </div>
    </aside>
  )
}
