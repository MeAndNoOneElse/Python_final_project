import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useStorage, useInventory } from '../hooks/useApi';
import { LoadingSpinner, ErrorMessage, Card, Button, Input, Badge } from '../components/Common';
import { apiClient } from '../utils/api';

const getProductName = (item) => item.name || item.product_name || 'Продукт';

const Storage = () => {
  const { groupId } = useParams();
  const navigate = useNavigate();
  const { storage, loading, error, setStorage } = useStorage(groupId);
  const [selectedStorage, setSelectedStorage] = useState(null);
  const [newProduct, setNewProduct] = useState({ name: '', quantity: '', unit: 'pcs' });
  const [adding, setAdding] = useState(false);

  const currentStorage = selectedStorage || (storage && storage[0]);
  const { inventory } = useInventory(currentStorage?.id);

  const handleAddProduct = async () => {
    if (!newProduct.name || !newProduct.quantity || !currentStorage?.id) return;
    try {
      setAdding(true);
      await apiClient.addInventory({
        storage_id: currentStorage.id,
        product_name: newProduct.name,
        quantity: parseFloat(newProduct.quantity),
        unit: newProduct.unit
      });
      setNewProduct({ name: '', quantity: '', unit: 'pcs' });
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

      <h1 className="text-2xl font-bold mb-4">Холодильник</h1>

      {storage && storage.length > 0 && (
        <Card className="mb-4">
          <p className="text-gray-400 text-sm">Текущий холодильник:</p>
          <p className="font-bold text-lg">{storage[0].name || 'Основной'}</p>
        </Card>
      )}

      <Card className="mb-4">
        <p className="text-gray-400 text-sm mb-2">Добавить продукт</p>
        <div className="space-y-2">
          <Input placeholder="Название" value={newProduct.name} onChange={e => setNewProduct({...newProduct, name: e.target.value})} />
          <div className="flex gap-2">
            <Input type="number" placeholder="Количество" value={newProduct.quantity} onChange={e => setNewProduct({...newProduct, quantity: e.target.value})} />
            <select value={newProduct.unit} onChange={e => setNewProduct({...newProduct, unit: e.target.value})} className="px-2 py-1 bg-gray-700 rounded text-white">
              <option value="pcs">шт</option>
              <option value="l">л</option>
              <option value="g">г</option>
            </select>
          </div>
          <Button onClick={handleAddProduct} disabled={adding} fullWidth>{adding ? 'Добавление...' : 'Добавить'}</Button>
        </div>
      </Card>

      <h2 className="text-lg font-bold mb-3">Продукты</h2>
      <div className="space-y-2">
        {inventory && inventory.length > 0 ? (
          inventory.map(item => (
            <Card key={item.id} className="hover:bg-gray-700/50 transition-colors">
              <div className="flex justify-between items-center">
                <span className="truncate">{getProductName(item)}</span>
                <Badge variant="products">{item.quantity} {item.unit}</Badge>
              </div>
            </Card>
          ))
        ) : (
          <Card className="text-center text-gray-400">Нет продуктов</Card>
        )}
      </div>
    </div>
  );
};

export default Storage;
