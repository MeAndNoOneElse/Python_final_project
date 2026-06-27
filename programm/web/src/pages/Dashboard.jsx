import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useBalance, useExpenses, useDebts, useShoppingList, useMembers } from '../hooks/useApi';
import { LoadingSpinner, ErrorMessage, Card, Button, BalanceDisplay, Badge } from '../components/Common';

const getExpenseName = (expense) => expense.name || expense.title || expense.expense_name || 'Расход';
const getExpenseAmount = (expense) => expense.amount || expense.total_amount || 0;

const Dashboard = () => {
  const { groupId } = useParams();
  const navigate = useNavigate();
  const { balance, loading: balanceLoading, error: balanceError } = useBalance(groupId);
  const { expenses, loading: expensesLoading } = useExpenses(groupId);
  const { debts, loading: debtsLoading } = useDebts(groupId);
  const { members } = useMembers(groupId);

  if (balanceLoading || expensesLoading || debtsLoading) return <LoadingSpinner />;
  if (balanceError) return <ErrorMessage message={balanceError} />;

  const recentExpenses = expenses?.slice(0, 5) || [];
  const pendingDebts = debts?.filter(d => !d.settled) || [];

  const handleQuickAction = (action) => {
    switch(action) {
      case 'expense':
        navigate(`/group/${groupId}/expenses`);
        break;
      case 'storage':
        navigate(`/group/${groupId}/storage`);
        break;
      case 'shopping':
        navigate(`/group/${groupId}/shopping-list`);
        break;
      case 'distribute':
        navigate(`/group/${groupId}/distribute`);
        break;
      default:
        break;
    }
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Дашборд</h1>

      {/* Баланс */}
      <Card className="mb-4 text-center">
        <p className="text-gray-400 text-sm mb-1">Ваш баланс</p>
        <BalanceDisplay balance={balance?.total_balance || 0} size="lg" />
        <div className="mt-2 text-xs text-gray-400 space-y-1">
          <p>Должны вам: {(balance?.should_get || 0).toFixed(2)} ₽</p>
          <p>Вы должны: {(balance?.should_pay || 0).toFixed(2)} ₽</p>
        </div>
      </Card>

      {/* Быстрые действия */}
      <div className="mb-4">
        <h2 className="text-lg font-bold mb-3">Быстрые действия</h2>
        <div className="grid grid-cols-2 gap-2">
          <Button onClick={() => handleQuickAction('expense')}>💰 Расход</Button>
          <Button variant="secondary" onClick={() => handleQuickAction('storage')}>🛒 Товар</Button>
          <Button variant="secondary" onClick={() => handleQuickAction('shopping')}>📝 Список</Button>
          <Button variant="secondary" onClick={() => handleQuickAction('distribute')}>📊 Распределить</Button>
        </div>
      </div>

      {/* Последние расходы */}
      <div className="mb-4">
        <h2 className="text-lg font-bold mb-3">Последние расходы</h2>
        {recentExpenses.length === 0 ? (
          <Card className="text-center py-4 text-gray-400 text-sm"><p>Расходов ещё нет</p></Card>
        ) : (
          <div className="space-y-2">
            {recentExpenses.map(expense => (
              <Card key={expense.id} className="hover:bg-gray-700/50 transition-colors">
                <div className="flex justify-between items-start">
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-white text-sm truncate">{getExpenseName(expense)}</h3>
                    <Badge className="mt-1">{expense.category || 'другое'}</Badge>
                  </div>
                  <span className="font-semibold text-blue-400 text-sm">
                    {getExpenseAmount(expense).toFixed(2)} ₽
                  </span>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Активные долги */}
      <div>
        <h2 className="text-lg font-bold mb-3">Активные долги</h2>
        {pendingDebts.length === 0 ? (
          <Card className="text-center py-4 text-gray-400 text-sm"><p>Долгов нет 🎉</p></Card>
        ) : (
          <div className="space-y-2">
            {pendingDebts.map(debt => (
              <Card key={debt.id}>
                <p className="text-white font-semibold text-sm">{debt.debtor_name} → {debt.creditor_name}</p>
                <p className="text-red-500 font-semibold text-sm">{debt.amount?.toFixed(2) || '0.00'} ₽</p>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
