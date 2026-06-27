import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useShoppingList } from '../hooks/useApi';
import { LoadingSpinner, ErrorMessage, Card, Button, Input, Badge } from '../components/Common';
import { apiClient } from '../utils/api';

const getProductName = (item) => item.name || item.product_name || 'Товар';

const ShoppingList = () => {
  const { groupId } = useParams();
  const navigate = useNavigate();
  const { items, loading, error, setItems } = useShoppingList(groupId);
  const [newItem, setNewItem] = useState('');
  const [adding, setAdding] = useState(false);

  const handleAddItem = async () => {
    if (!newItem.trim()) return;
    try {
      setAdding(true);
      await apiClient.request(`/api/shopping-list`, {
        method: 'POST',
        body: JSON.stringify({ group_id: Number(groupId), product_name: newItem.trim(), quantity: 1, unit: 'pcs' })
      });
      setNewItem('');
      window.location.reload();
    } catch (err) {
      alert('Ошибка: ' + err.message);
    } finally {
      setAdding(false);
    }
  };

  const handleBack = () => {
    navigate(`/group/${groupId}/dashboard`);
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="max-w-md mx-auto p-4">
      <Button variant="ghost" onClick={handleBack} className="mb-4">
        ← Назад
      </Button>

      <h1 className="text-2xl font-bold mb-4">Список покупок</h1>

      <Card className="mb-4">
        <div className="flex gap-2">
          <Input
            placeholder="Добавить товар..."
            value={newItem}
            onChange={e => setNewItem(e.target.value)}
          />
          <Button onClick={handleAddItem} disabled={adding}>
            {adding ? '...' : '+'}
          </Button>
        </div>
      </Card>

      <div className="space-y-2">
        {items && items.length > 0 ? (
          items.map(item => (
            <Card key={item.id} className="hover:bg-gray-700/50 transition-colors">
              <div className="flex justify-between items-center">
                <div className="flex-1 min-w-0">
                  <p className="font-semibold truncate">{getProductName(item)}</p>
                  <Badge variant="products" className="mt-1">Купить: {item.quantity} {item.unit}</Badge>
                </div>
              </div>
            </Card>
          ))
        ) : (
          <Card className="text-center text-gray-400">
            <p>Список пуст</p>
          </Card>
        )}
      </div>
    </div>
  );
};

export default ShoppingList;
