import React from 'react';
import { Bot, Cpu, Database, Zap, Activity, CheckCircle2 } from 'lucide-react';

export default function DashboardPanel() {
  const stats = [
    { title: 'Total Agents', value: '12 Active', icon: Bot, change: '+2 initialized' },
    { title: 'Cluster CPU Usage', value: '28.4%', icon: Cpu, change: 'Nominal' },
    { title: 'Shared Memory Nodes', value: '1,024 MB', icon: Database, change: 'Synced' },
    { title: 'Task Throughput', value: '142 / min', icon: Zap, change: '+12% vs last hour' },
  ];

  const recentAgents = [
    { name: 'Alpha-Ops', role: 'Orchestrator', status: 'Active', tasks: 4 },
    { name: 'Beta-Analyst', role: 'Data Insights', status: 'Idle', tasks: 0 },
    { name: 'Gamma-Sentry', role: 'Security Monitor', status: 'Active', tasks: 2 },
  ];

  return (
    <div className="p-6 space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-100">Central Command Hub Overview</h2>
        <p className="text-slate-400 text-sm mt-1">
          Real-time status and control panel for multi-agent digital conglomerate orchestration.
        </p>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.title} className="bg-slate-900 border border-slate-800 rounded-xl p-5">
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-slate-400">{stat.title}</span>
                <div className="p-2 bg-slate-800 rounded-lg text-indigo-400">
                  <Icon className="h-5 w-5" />
                </div>
              </div>
              <div className="mt-3 text-2xl font-semibold text-slate-100">{stat.value}</div>
              <div className="mt-1 text-xs text-emerald-400 flex items-center gap-1">
                <CheckCircle2 className="h-3 w-3" />
                {stat.change}
              </div>
            </div>
          );
        })}
      </div>

      {/* Main dashboard grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Agent status panel */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-slate-200">Active Agents</h3>
            <span className="text-xs bg-indigo-950 text-indigo-300 border border-indigo-800 px-2.5 py-1 rounded-full">
              Live Feed
            </span>
          </div>
          <div className="divide-y divide-slate-800">
            {recentAgents.map((agent) => (
              <div key={agent.name} className="py-3 flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-slate-800 rounded-lg text-slate-300">
                    <Bot className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="text-sm font-medium text-slate-200">{agent.name}</div>
                    <div className="text-xs text-slate-500">{agent.role}</div>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="text-xs text-slate-400">{agent.tasks} tasks</div>
                  <span
                    className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                      agent.status === 'Active'
                        ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                        : 'bg-slate-800 text-slate-400'
                    }`}
                  >
                    {agent.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Activity Feed panel */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-slate-200">System Logs</h3>
            <Activity className="h-4 w-4 text-slate-400" />
          </div>
          <div className="space-y-3">
            <div className="p-3 bg-slate-950 rounded-lg border border-slate-800/80 text-xs text-slate-300 space-y-1">
              <div className="flex justify-between text-slate-500">
                <span>Alpha-Ops</span>
                <span>12:00:00</span>
              </div>
              <p>Communication loop initialized successfully.</p>
            </div>
            <div className="p-3 bg-slate-950 rounded-lg border border-slate-800/80 text-xs text-slate-300 space-y-1">
              <div className="flex justify-between text-slate-500">
                <span>Gamma-Sentry</span>
                <span>12:05:00</span>
              </div>
              <p>Perimeter scan completed. No security anomalies detected.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
