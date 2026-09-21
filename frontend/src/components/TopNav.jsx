import React from 'react';
import { Bell, Search, Cpu, RefreshCw } from 'lucide-react';

export default function TopNav() {
  return (
    <header className="h-16 bg-slate-900/80 backdrop-blur-md border-b border-slate-800 px-6 flex items-center justify-between sticky top-0 z-10">
      <div className="flex items-center space-x-4 w-1/3">
        <div className="relative w-full">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
          <input
            type="text"
            placeholder="Search agents, memory logs, tasks..."
            className="w-full bg-slate-800 border border-slate-700 rounded-lg pl-9 pr-4 py-1.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      <div className="flex items-center space-x-4">
        <button
          className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors"
          title="Refresh Data"
        >
          <RefreshCw className="h-5 w-5" />
        </button>
        <button className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors relative">
          <Bell className="h-5 w-5" />
          <span className="absolute top-1.5 right-1.5 h-2 w-2 bg-indigo-500 rounded-full"></span>
        </button>
        <div className="h-6 w-px bg-slate-800"></div>
        <div className="flex items-center space-x-3">
          <div className="bg-indigo-950 border border-indigo-700/50 p-2 rounded-lg">
            <Cpu className="h-5 w-5 text-indigo-400" />
          </div>
          <div>
            <div className="text-sm font-medium text-slate-200">Central Node</div>
            <div className="text-xs text-emerald-400 flex items-center gap-1">
              <span className="inline-block h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
              Online
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
