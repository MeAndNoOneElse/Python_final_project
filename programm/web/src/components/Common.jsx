import React from 'react';

export const Card = ({ className = '', children, onClick }) => (
  <div
    className={`bg-gray-800/50 rounded-xl p-4 backdrop-blur-sm ${className}`}
    onClick={onClick}
  >
    {children}
  </div>
);

export const Button = ({ 
  children, 
  variant = 'primary', 
  onClick, 
  disabled = false,
  fullWidth = false,
  className = ''
}) => {
  const baseClasses = 'font-semibold rounded-lg transition-all duration-200 touch-target';
  const variants = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    secondary: 'bg-gray-700 hover:bg-gray-600 text-white',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
    ghost: 'bg-transparent hover:bg-gray-700 text-gray-300'
  };
  
  const widthClass = fullWidth ? 'w-full' : '';
  return (
    <button
      className={`${baseClasses} ${variants[variant]} ${widthClass} ${className} ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export const Input = ({ 
  placeholder, 
  value, 
  onChange, 
  type = 'text',
  disabled = false,
  error
}) => (
  <div>
    <input
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      disabled={disabled}
      className={`w-full px-3 py-2 bg-gray-700/50 border rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 ${error ? 'border-red-500' : 'border-gray-600'}`}
    />
    {error && <p className="text-red-400 text-xs mt-1">{error}</p>}
  </div>
);

export const Select = ({ options, value, onChange, disabled }) => (
  <select
    value={value}
    onChange={onChange}
    disabled={disabled}
    className="w-full px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
  >
    {options.map(opt => (
      <option key={opt.value} value={opt.value}>
        {opt.label}
      </option>
    ))}
  </select>
);

export const Modal = ({ isOpen, title, onClose, children, actions }) => {
  if (!isOpen) return null;
  
  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center bg-black/50 p-4">
      <div className="bg-gray-900 rounded-t-2xl max-h-[80vh] w-full max-w-md p-6 overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold">{title}</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-white text-2xl">×</button>
        </div>
        {children}
        {actions && (
          <div className="flex gap-2 mt-6 pt-4 border-t border-gray-700">
            {actions.map((action, i) => (
              <Button
                key={i}
                variant={action.variant}
                onClick={action.onClick}
                disabled={action.disabled}
                fullWidth={action.label.includes('Отмена') ? false : true}
              >
                {action.label}
              </Button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export const LoadingSpinner = () => (
  <div className="flex items-center justify-center p-8">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
  </div>
);

export const ErrorMessage = ({ message }) => (
  <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-3 text-red-300 text-sm">
    {message}
  </div>
);

export const BalanceDisplay = ({ balance, size = 'md' }) => {
  const colors = balance >= 0 ? 'text-green-400' : 'text-red-400';
  const sizeClass = size === 'lg' ? 'text-2xl' : 'text-xl';
  
  return (
    <span className={`font-bold ${colors} ${sizeClass}`}>
      {balance >= 0 ? '+' : ''}{balance.toFixed(0)}₽
    </span>
  );
};

export const Badge = ({ children, variant = 'default' }) => {
  const variants = {
    default: 'bg-gray-700 text-gray-300',
    success: 'bg-green-500/20 text-green-400',
    warning: 'bg-yellow-500/20 text-yellow-400',
    danger: 'bg-red-500/20 text-red-400',
    products: 'bg-blue-500/20 text-blue-400',
    entertainment: 'bg-purple-500/20 text-purple-400',
    transport: 'bg-indigo-500/20 text-indigo-400',
    utilities: 'bg-cyan-500/20 text-cyan-400',
    other: 'bg-gray-500/20 text-gray-300'
  };

  const getCategoryVariant = (category) => {
    const cat = (category || '').toLowerCase();
    if (cat.includes('продукт') || cat.includes('продукты') || cat.includes('еда')) return 'products';
    if (cat.includes('развл') || cat.includes('отдых') || cat.includes('развлечения')) return 'entertainment';
    if (cat.includes('транспорт') || cat.includes('проезд')) return 'transport';
    if (cat.includes('коммунал') || cat.includes('коммунальные') || cat.includes('связь')) return 'utilities';
    if (cat === 'другое' || cat === 'other') return 'other';
    return 'default';
  };

  const variantKey = variant === 'default' && typeof children === 'string' ? getCategoryVariant(children) : variant;

  return (
    <span className={`text-xs px-2 py-1 rounded-full ${variants[variantKey]}`}>
      {children}
    </span>
  );
};
