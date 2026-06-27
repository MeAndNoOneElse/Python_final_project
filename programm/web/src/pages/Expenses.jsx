import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useExpenses, useMembers } from '../hooks/useApi';
import { LoadingSpinner, ErrorMessage, Card, Button, Input, Modal, Badge } from '../components/Common';
import { apiClient } from '../utils/api';

const getExpenseName = (expense) => expense.name || expense.title || expense.expense_name || 'Расход';
const getExpenseAmount = (expense) => expense.amount || expense.total_amount || 0;

const Expenses = () => {
  const { groupId } = useParams();
  const navigate = useNavigate();
  const { expenses, loading, error } = useExpenses(groupId);
  const { members } = useMembers(groupId);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newExpense, setNewExpense] = useState({ name: '', amount: '', category: 'другое', date: new Date().toISOString().split('T')[0] });
  const [creating, setCreating] = useState(false);

  const handleCreateExpense = async () => {
    if (!newExpense.name || !newExpense.amount) return;
    try {
      setCreating(true);
      await apiClient.createManualExpense({
        group_id: Number(groupId),
        title: newExpense.name,
        total_amount: parseFloat(newExpense.amount),
        category: newExpense.category,
        purchase_date: newExpense.date,
        participant_ids: members?.map(m => m.id) || [],
      });
      setShowCreateModal(false);
      // Перезагружаем страницу для обновления баланса и долгов
      window.location.reload();
    } catch (err) {
      alert('Ошибка: ' + err.message);
    } finally {
      setCreating(false);
    }
  };

  const handleBack = () => navigate(`/group/${groupId}/dashboard`);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="max-w-md mx-auto p-4">
      <Button variant="ghost" onClick={handleBack} className="mb-4">← Назад</Button>
      <h1 className="text-2xl font-bold mb-4">Расходы</h1>

      <Button onClick={() => setShowCreateModal(true)} fullWidth className="mb-4">+ Новый расход</Button>

      <div className="space-y-3">
        {expenses && expenses.length > 0 ? (
          expenses.map(expense => (
            <Card key={expense.id} className="hover:bg-gray-700/50 transition-colors">
              <div className="flex justify-between items-start">
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-white text-sm truncate">{getExpenseName(expense)}</h3>
                  <div className="flex gap-2 mt-1">
                    <Badge variant="products">{(expense.amount || expense.total_amount || 0).toFixed(2)} ₽</Badge>
                    <Badge>{expense.category || 'другое'}</Badge>
                  </div>
                </div>
                <span className="font-semibold text-blue-400 text-sm">
                  {getExpenseAmount(expense).toFixed(2)} ₽
                </span>
              </div>
            </Card>
          ))
        ) : (
          <Card className="text-center text-gray-400">Расходов нет</Card>
        )}
      </div>

      <Modal
        isOpen={showCreateModal}
        title="Новый расход"
        onClose={() => setShowCreateModal(false)}
        actions={[
          { label: 'Отмена', variant: 'secondary', onClick: () => setShowCreateModal(false) },
          { label: creating ? 'Создание...' : 'Создать', variant: 'primary', onClick: handleCreateExpense, disabled: creating }
        ]}
      >
        <div className="space-y-4">
          <div>
            <label className="block text-sm mb-1">Название</label>
            <Input placeholder="Название" value={newExpense.name} onChange={e => setNewExpense({...newExpense, name: e.target.value})} />
          </div>
          <div>
            <label className="block text-sm mb-1">Сумма</label>
            <Input type="number" placeholder="100" value={newExpense.amount} onChange={e => setNewExpense({...newExpense, amount: e.target.value})} />
          </div>
          <div>
            <label className="block text-sm mb-1">Категория</label>
            <select value={newExpense.category} onChange={e => setNewExpense({...newExpense, category: e.target.value})} className="w-full px-3 py-2 bg-gray-700 rounded text-white">
              <option value="продукты">Продукты</option>
              <option value="развлечения">Развлечения</option>
              <option value="другое">Другое</option>
            </select>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Expenses;
