import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Globe, Search, Layers, GitCompare, Eye, CheckSquare, Clock, Info } from 'lucide-react';

export const Header: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { label: 'Search', path: '/search', icon: Search },
    { label: 'Find Similar', path: '/similar', icon: Layers },
    { label: 'Compare', path: '/compare', icon: GitCompare },
    { label: 'Change Analysis', path: '/change', icon: Eye },
    { label: 'Review Queue', path: '/review', icon: CheckSquare },
    { label: 'About & Truth-in-AI', path: '/about', icon: Info },
  ];

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14">
          <div className="flex items-center gap-3">
            <Link to="/" className="flex items-center gap-2">
              <div className="w-8 h-8 rounded bg-blue-700 flex items-center justify-center text-white shadow-sm">
                <Globe className="w-5 h-5" />
              </div>
              <div>
                <span className="text-lg font-bold tracking-tight text-slate-900">TerraSeek</span>
                <span className="hidden sm:inline-block ml-2 text-xs text-slate-700 font-medium px-1.5 py-0.5 bg-slate-100 rounded border border-slate-200">
                  Demo Mode
                </span>
              </div>
            </Link>
          </div>

          <nav className="flex items-center gap-1 sm:gap-2">
            {navItems.map((item) => {
              const active = location.pathname === item.path;
              const Icon = item.icon;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-medium rounded-md transition-colors ${
                    active
                      ? 'bg-blue-50 text-blue-700 border border-blue-200'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span className="hidden md:inline">{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
};
