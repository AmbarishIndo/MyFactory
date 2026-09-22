import React from 'react';
import { Layout, Bot, Database, Activity, ShieldCheck, Terminal, Layers } from 'lucide-react';

export default function Sidebar() {
  const navItems = [
    { name: 'Overview', icon: Layout, active: true },
    { name: 'Quant Engine (Omega)', icon: Bot, active: false },
    { name: 'Media Studio (Sigma)', icon: Activity, active: false },
    { name: 'Asset Foundry', icon: ShieldCheck, active: false },
    { name: 'RAG Memory Logs (Theta)', icon: Database, active: false },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col min-h-screen">
      <div className="p-6 border-b border-slate-800 flex items-center space-x-3">
        <div className="bg-indigo-600 p-2 rounded-lg text-white">
          <Layers className="h-6 w-6" />
        </div>
        <div>
          <h1 className="font-bold text-slate-100 text-lg leading-tight">Command Hub</h1>
          <p className="text-xs text-slate-400">Multi-Agent Conglomerate</p>
        </div>
      </div>
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <a
              key={item.name}
              href="#"
              className={`flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                item.active
                  ? 'bg-indigo-600 text-white'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
              }`}
            >
              <Icon className="h-5 w-5" />
              <span>{item.name}</span>
            </a>
          );
        })}
      </nav>
      <div className="p-4 border-t border-slate-800">
        <div className="flex items-center space-x-2 text-xs text-slate-400">
          <Terminal className="h-4 w-4 text-emerald-400" />
          <span>Cluster: Operational (v0.1)</span>
        </div>
      </div>
    </aside>
  );
}
