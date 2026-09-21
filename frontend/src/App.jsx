import React from 'react';
import Sidebar from './components/Sidebar';
import TopNav from './components/TopNav';
import DashboardPanel from './components/DashboardPanel';

export default function App() {
  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <TopNav />
        <main className="flex-1 overflow-y-auto">
          <DashboardPanel />
        </main>
      </div>
    </div>
  );
}
