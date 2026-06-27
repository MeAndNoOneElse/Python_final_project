import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useExpenses, useMembers } from '../hooks/useApi';
import { LoadingSpinner, ErrorMessage, Card, Button, Modal, Badge, Input } from '../components/Common';
import { apiClient } from '../utils/api';

const getExpenseName = (expense) => expense.name || expense.title || expense.expense_name || 'Расход';
const getExpenseAmount = (expense) => expense.amount || expense.total_amount || 0;
const getMemberName = (member) => member.name || member.username || `Пользователь ${member.id}`;

const Distribute = () => {
  const { groupId } = useParams();
  const navigate = useNavigate();
  const { expenses, loading: expensesLoading, setExpenses } = useExpenses(groupId);
  const { members, loading: membersLoading } = useMembers(groupId);
  const [selectedExpense, setSelectedExpense] = useState(null);
  const [selectedMembers, setSelectedMembers] = useState({});
  const [distributing, setDistributing] = useState(false);

  const handleBack = () => navigate(`/group/${groupId}/dashboard`);

  const toggleMember = (memberId) => {
    setSelectedMembers(prev => ({
      ...prev,
      [memberId]: !prev[memberId]
    }));
  };

  const handleAmountChange = (memberId, amount) => {
    setSelectedMembers(prev => ({
      ...prev,
      [memberId]: { ...prev[memberId], amount }
    }));
  };

  const handleDistribute = async () => {
    if (!selectedExpense || Object.keys(selectedMembers).filter(k => selectedMembers[k]).length === 0) return;

    // Формируем assignments: {member_id: сумма или null}
    const assignments = {};
    Object.keys(selectedMembers).filter(k => selectedMembers[k]).forEach(memberId => {
      const memberData = selectedMembers[memberId];
      const amount = typeof memberData === 'object' ? memberData.amount : null;
      assignments[Number(memberId)] = amount ? Number(amount) : null;
    });

    try {
      setDistributing(true);
      await apiClient.distributeExpense(selectedExpense.id, assignments);
      alert('Распределено!');
      setSelectedExpense(null);
      setSelectedMembers({});
      // Обновляем страницу для отображения новых долгов
      window.location.reload();
    } catch (err) {
      alert('Ошибка: ' + err.message);
    } finally {
      setDistributing(false);
    }
  };

  if (expensesLoading || membersLoading) return <LoadingSpinner />;

  return (
    <div className="max-w-md mx-auto p-4">
      <Button variant="ghost" onClick={handleBack} className="mb-4">← Назад</Button>
      <h1 className="text-2xl font-bold mb-4">Распределить расходы</h1>

      {!selectedExpense ? (
        <div className="space-y-3">
          {expenses && expenses.length > 0 ? (
            expenses.map(expense => (
              <Card
                key={expense.id}
                className="cursor-pointer hover:bg-gray-700/50 transition-colors"
                onClick={() => setSelectedExpense(expense)}
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1 min-w-0">
                    <p className="font-semibold truncate">{getExpenseName(expense)}</p>
                    <Badge className="mt-1">{expense.category || 'другое'}</Badge>
                  </div>
                  <span className="font-semibold text-blue-400 text-sm">
                    {getExpenseAmount(expense).toFixed(2)} ₽
                  </span>
                </div>
              </Card>
            ))
          ) : (
            <Card className="text-center text-gray-400">Нет расходов для распределения</Card>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          <Card>
            <p className="text-gray-400 text-sm mb-1">Расход</p>
            <p className="font-bold text-lg">{getExpenseName(selectedExpense)}</p>
            <p className="text-blue-400 font-semibold">{getExpenseAmount(selectedExpense).toFixed(2)} ₽</p>
          </Card>

          <div>
            <p className="text-gray-400 text-sm mb-2">Выберите участников и их доли:</p>
            <div className="space-y-2 max-h-60 overflow-y-auto">
              {members && members.length > 0 ? (
                members.map(member => {
                  const isSelected = selectedMembers[member.id];
                  const memberData = isSelected ? selectedMembers[member.id] : null;
                  return (
                    <Card
                      key={member.id}
                      className={`transition-colors ${
                        isSelected ? 'bg-blue-500/20 border border-blue-500' : 'hover:bg-gray-700/50'
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        <input
                          type="checkbox"
                          checked={!!isSelected}
                          onChange={() => toggleMember(member.id)}
                          className="w-4 h-4 accent-blue-500"
                        />
                        <span className="flex-1 truncate">{getMemberName(member)}</span>
                        {isSelected && (
                          <Input
                            type="number"
                            placeholder="сумма"
                            value={typeof memberData === 'object' ? (memberData.amount || '') : ''}
                            onChange={(e) => handleAmountChange(member.id, e.target.value)}
                            className="w-20 text-right"
                            min="0"
                            step="0.01"
                          />
                        )}
                      </div>
                    </Card>
                  );
                })
              ) : (
                <Card className="text-center text-gray-400">Нет участников</Card>
              )}
            </div>
            <p className="text-xs text-gray-400 mt-2">Оставьте поле пустым для равномерного распределения</p>
            <Card className="mt-2 bg-yellow-500/20 border border-yellow-500">
              <p className="text-yellow-300 text-xs">
                ⚠️ Долги после распределения обновляются при следующем открытии группы
              </p>
            </Card>
          </div>

          <div className="flex gap-2">
            <Button variant="secondary" onClick={() => setSelectedExpense(null)} fullWidth>
              Отмена
            </Button>
            <Button
              variant="primary"
              onClick={handleDistribute}
              disabled={distributing || Object.keys(selectedMembers).filter(k => selectedMembers[k]).length === 0}
              fullWidth
            >
              {distributing ? 'Распределение...' : 'Распределить'}
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Distribute;