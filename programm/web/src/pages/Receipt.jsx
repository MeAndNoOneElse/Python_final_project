import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useMembers, useStorage } from '../hooks/useApi';
import { LoadingSpinner, ErrorMessage, Card, Button, Input, Badge, Modal } from '../components/Common';
import { apiClient } from '../utils/api';

const Receipt = () => {
  const { groupId } = useParams();
  const { members, loading: membersLoading } = useMembers(groupId);
  const { storage } = useStorage(groupId);
  const [receiptItems, setReceiptItems] = useState([]);
  const [scanMode, setScanMode] = useState('manual');
  const [qrCode, setQrCode] = useState('');
  const [showScanner, setShowScanner] = useState(false);
  const [showDistribution, setShowDistribution] = useState(false);
  const [distribution, setDistribution] = useState({});
  const [storageId, setStorageId] = useState(storage?.[0]?.id || null);
  const [isGrocery, setIsGrocery] = useState(true);

  const handleQRScan = async () => {
    if (!qrCode) return;
    try {
      const items = await apiClient.scanQRCode({ qr_code: qrCode });
      setReceiptItems(items);
      setScanMode('manual');
      setQrCode('');
      setShowScanner(false);
      initDistribution(items);
    } catch (err) {
      console.error('Ошибка сканирования QR:', err);
      alert('Не удалось распознать чек');
    }
  };

  const initDistribution = (items) => {
    const dist = {};
    items.forEach(item => {
      dist[item.id] = null; // null = общее
    });
    setDistribution(dist);
  };

  const handleAddManualItem = () => {
    const name = prompt('Название товара:');
    const amount = prompt('Сумма (₽):');
    if (name && amount) {
      const newItem = {
        id: Date.now(),
        name,
        amount: parseFloat(amount),
      };
      const newItems = [...receiptItems, newItem];
      setReceiptItems(newItems);
      initDistribution(newItems);
    }
  };

  const handleDistribute = async () => {
    try {
      if (receiptItems.length === 0) return;

      const createdExpense = await apiClient.createManualExpense({
        group_id: Number(groupId),
        title: `Чек ${new Date().toLocaleDateString('ru-RU')}`,
        total_amount: totalAmount,
        category: isGrocery ? 'продукты' : 'другое',
        purchase_date: new Date().toISOString().slice(0, 10),
        is_grocery: isGrocery,
        storage_location_id: isGrocery ? storageId : null,
        items: receiptItems.map((item) => ({
          name: item.name,
          price: Number(item.amount || 0),
          quantity: 1,
          unit: 'pcs',
        })),
      });

      if (createdExpense?.id) {
        const assignments = {};
        for (const item of receiptItems) {
          assignments[item.id] = distribution[item.id] ?? null;
        }
        await apiClient.distributeExpense(createdExpense.id, { assignments });
      }

      alert('Распределение сохранено!');
      setReceiptItems([]);
      setDistribution({});
      setShowDistribution(false);
    } catch (err) {
      console.error('Ошибка при распределении:', err);
    }
  };

  const handleRemoveItem = (itemId) => {
    const newItems = receiptItems.filter(i => i.id !== itemId);
    setReceiptItems(newItems);
    const newDist = { ...distribution };
    delete newDist[itemId];
    setDistribution(newDist);
  };

  const totalAmount = receiptItems.reduce((sum, item) => sum + (item.amount || 0), 0);

  if (membersLoading) return <LoadingSpinner />;

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Добавить расход</h1>

      {receiptItems.length === 0 ? (
        // Экран выбора способа добавления
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <Card
            className="text-center p-8 hover:bg-gray-700 cursor-pointer transition-colors"
            onClick={() => setShowScanner(true)}
          >
            <p className="text-4xl mb-2">📱</p>
            <h3 className="font-bold mb-2">Сканировать QR</h3>
            <p className="text-sm text-gray-400">QR-код со скрытого чека</p>
          </Card>

          <Card
            className="text-center p-8 hover:bg-gray-700 cursor-pointer transition-colors"
            onClick={() => handleAddManualItem()}
          >
            <p className="text-4xl mb-2">✍️</p>
            <h3 className="font-bold mb-2">Вручную</h3>
            <p className="text-sm text-gray-400">Добавить товар вручную</p>
          </Card>

          <Card
            className="text-center p-8 hover:bg-gray-700 cursor-pointer transition-colors"
            onClick={() => {
              const photo = prompt('Загрузить фото чека (URL):');
              if (photo) {
                // TODO: Implement photo upload
              }
            }}
          >
            <p className="text-4xl mb-2">📸</p>
            <h3 className="font-bold mb-2">Фото чека</h3>
            <p className="text-sm text-gray-400">Фотография чека (OCR)</p>
          </Card>
        </div>
      ) : (
        // Экран распределения
        <>
          <div className="flex justify-between items-center mb-6">
            <div>
              <h2 className="text-2xl font-bold mb-2">Распределение расходов</h2>
              <p className="text-gray-400">Всего: {totalAmount.toFixed(2)} ₽</p>
            </div>
            <div className="flex gap-2">
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={isGrocery}
                  onChange={e => setIsGrocery(e.target.checked)}
                  className="w-4 h-4"
                />
                <span className="text-sm">Это товары (пополнят склад)</span>
              </label>
            </div>
          </div>

          {isGrocery && (
            <Card className="mb-6">
              <label className="block text-sm font-medium mb-2">Целевой холодильник</label>
              <select
                value={storageId || ''}
                onChange={e => setStorageId(parseInt(e.target.value))}
                className="w-full px-3 py-2 bg-gray-700 text-white rounded-lg border border-gray-600 focus:outline-none focus:border-blue-500"
              >
                {storage?.map(s => (
                  <option key={s.id} value={s.id}>
                    {s.name}
                  </option>
                ))}
              </select>
            </Card>
          )}

          {/* Товары для распределения */}
          <div className="space-y-3 mb-8">
            {receiptItems.map(item => (
              <Card key={item.id} className="p-4">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <p className="font-semibold text-white">{item.name}</p>
                    <p className="text-sm text-gray-400">{item.amount?.toFixed(2)} ₽</p>
                  </div>
                  <Button
                    variant="danger"
                    onClick={() => handleRemoveItem(item.id)}
                  >
                    Удалить
                  </Button>
                </div>

                <div className="space-y-2">
                  <p className="text-sm text-gray-400 mb-2">Назначить:</p>
                  <div className="flex flex-wrap gap-2">
                    <button
                      onClick={() =>
                        setDistribution({
                          ...distribution,
                          [item.id]: null,
                        })
                      }
                      className={`px-3 py-2 rounded text-sm font-semibold transition-colors ${
                        distribution[item.id] === null
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                      }`}
                    >
                      Общее
                    </button>
                    {members?.map(member => (
                      <button
                        key={member.id}
                        onClick={() =>
                          setDistribution({
                            ...distribution,
                            [item.id]: member.id,
                          })
                        }
                        className={`px-3 py-2 rounded text-sm font-semibold transition-colors ${
                          distribution[item.id] === member.id
                            ? 'bg-green-600 text-white'
                            : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                        }`}
                      >
                        {member.name}
                      </button>
                    ))}
                  </div>
                </div>
              </Card>
            ))}
          </div>

          {/* Сводка */}
          <Card className="mb-8 p-6">
            <h3 className="font-bold mb-4">Сводка по участникам:</h3>
            <div className="space-y-2 text-sm">
              {Object.entries(
                receiptItems.reduce((acc, item) => {
                  const memberId = distribution[item.id];
                  const memberName = memberId
                    ? members?.find(m => m.id === memberId)?.name
                    : 'Общее';
                  if (!acc[memberName]) acc[memberName] = 0;
                  acc[memberName] += item.amount || 0;
                  return acc;
                }, {})
              ).map(([name, amount]) => (
                <p key={name} className="text-gray-300">
                  {name}: <span className="font-semibold">{amount.toFixed(2)} ₽</span>
                </p>
              ))}
            </div>
          </Card>

          {/* Кнопки действия */}
          <div className="flex gap-4">
            <Button
              variant="secondary"
              onClick={() => {
                setReceiptItems([]);
                setDistribution({});
              }}
            >
              Отмена
            </Button>
            <Button onClick={handleDistribute}>
              Сохранить распределение
            </Button>
          </div>
        </>
      )}

      {/* Модальное окно для сканирования */}
      <Modal
        isOpen={showScanner}
        title="Сканировать QR-код"
        onClose={() => {
          setShowScanner(false);
          setQrCode('');
        }}
        actions={[
          { label: 'Отмена', variant: 'secondary', onClick: () => setShowScanner(false) },
          { label: 'Сканировать', variant: 'primary', onClick: handleQRScan },
        ]}
      >
        <div className="space-y-4">
          <p className="text-gray-300 text-sm">
            В боевом режиме здесь была бы интеграция с камерой.
          </p>
          <Input
            placeholder="Или вставьте текст QR-кода вручную"
            value={qrCode}
            onChange={e => setQrCode(e.target.value)}
          />
        </div>
      </Modal>
    </div>
  );
};

export default Receipt;
