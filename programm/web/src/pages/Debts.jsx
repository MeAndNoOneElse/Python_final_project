import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useDebts, useBalance } from '../hooks/useApi';
import { LoadingSpinner, ErrorMessage, Card, Button, Modal, BalanceDisplay } from '../components/Common';
import { apiClient } from '../utils/api';

const getDebtorName = (debt) => debt.debtor_name || debt.debtor?.name || `Пользователь ${debt.debtor_id}`;
const getCreditorName = (debt) => debt.creditor_name || debt.creditor?.name || `Пользователь ${debt.creditor_id}`;

const Debts = () => {
  const { groupId } = useParams();
  const { debts, loading: debtsLoading, setDebts } = useDebts(groupId);
  const { balance, loading: balanceLoading } = useBalance(groupId);
  const [showSettleModal, setShowSettleModal] = useState(false);
  const [selectedDebt, setSelectedDebt] = useState(null);

  const handleSettleDebt = async () => {
    try {
      await apiClient.settleDebt(selectedDebt.id, {
        settled_date: new Date().toISOString(),
      });
      setDebts(debts.filter(d => d.id !== selectedDebt.id));
      setShowSettleModal(false);
      setSelectedDebt(null);
    } catch (err) {
      console.error('Ошибка погашения долга:', err);
    }
  };

  if (debtsLoading || balanceLoading) return <LoadingSpinner />;

  const activeDebts = debts?.filter(d => !d.settled) || [];
  const myDebts = activeDebts.filter(d => d.debtor_id === balance?.current_user_id);
  const debtsToMe = activeDebts.filter(d => d.creditor_id === balance?.current_user_id);

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Долги</h1>

      {/* Сводка по балансу */}
      {balance && (
        <Card className="mb-8 p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <p className="text-gray-400 text-sm mb-2">Общий баланс</p>
              <div className="text-2xl">
                <BalanceDisplay balance={balance.total_balance} />
              </div>
            </div>
            <div>
              <p className="text-gray-400 text-sm mb-2">Вы должны</p>
              <p className="text-2xl text-red-500 font-semibold">{balance.should_pay.toFixed(2)} ₽</p>
            </div>
            <div>
              <p className="text-gray-400 text-sm mb-2">Должны вам</p>
              <p className="text-2xl text-green-500 font-semibold">{balance.should_get.toFixed(2)} ₽</p>
            </div>
          </div>
        </Card>
      )}

      {/* Долги других мне */}
      {debtsToMe.length > 0 && (
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4 text-green-500">Должны вам ↓</h2>
          <div className="space-y-3">
            {debtsToMe.map(debt => (
              <Card key={debt.id} className="hover:bg-gray-700 transition-colors">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-white font-semibold">{getDebtorName(debt)} должен вам</p>
                    <p className="text-sm text-gray-400">{debt.reason}</p>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(debt.created_date).toLocaleDateString('ru-RU')}
                    </p>
                  </div>
                  <span className="font-bold text-green-400">{debt.amount.toFixed(2)} ₽</span>
                </div>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Мои долги */}
      {myDebts.length > 0 && (
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4 text-red-500">Вы должны ↑</h2>
          <div className="space-y-3">
            {myDebts.map(debt => (
              <Card key={debt.id} className="hover:bg-gray-700 transition-colors border-l-4 border-red-500">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-white font-semibold">Вы должны {getCreditorName(debt)}</p>
                    <p className="text-sm text-gray-400">{debt.reason}</p>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(debt.created_date).toLocaleDateString('ru-RU')}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-red-400 mb-3">{debt.amount.toFixed(2)} ₽</p>
                    <Button
                      variant="success"
                      onClick={() => {
                        setSelectedDebt(debt);
                        setShowSettleModal(true);
                      }}
                    >
                      Я заплатил
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      )}

      {activeDebts.length === 0 && (
        <Card className="text-center py-12 text-gray-400">
          <p className="text-xl">Долгов нет 🎉</p>
          <p className="text-sm mt-2">Все расчеты сбалансированы</p>
        </Card>
      )}

      {/* Модальное окно погашения долга */}
      <Modal
        isOpen={showSettleModal}
        title="Подтвердить платёж"
        onClose={() => {
          setShowSettleModal(false);
          setSelectedDebt(null);
        }}
        actions={[
          {
            label: 'Отмена',
            variant: 'secondary',
            onClick: () => {
              setShowSettleModal(false);
              setSelectedDebt(null);
            },
          },
          {
            label: 'Я заплатил',
            variant: 'success',
            onClick: handleSettleDebt,
          },
        ]}
      >
        {selectedDebt && (
          <div className="space-y-4">
            <p className="text-white">
              Вы платите <span className="font-bold">{getCreditorName(selectedDebt)}</span>
            </p>
            <p className="text-2xl font-bold text-red-500">
              {selectedDebt.amount.toFixed(2)} ₽
            </p>
            <p className="text-gray-400 text-sm">
              За: {selectedDebt.reason}
            </p>
            <p className="text-gray-400 text-sm">
              После подтверждения кредитору придёт запрос на подтверждение получения денег.
            </p>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Debts;
