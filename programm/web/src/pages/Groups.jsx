import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGroups, useCurrentGroup } from '../hooks/useApi';
import { LoadingSpinner, ErrorMessage, BalanceDisplay, Button, Card, Modal, Input, Select } from '../components/Common';
import { apiClient } from '../utils/api';

const EmptyGroupsGuide = () => (
  <Card className="py-6 text-center">
    <h2 className="text-lg font-bold text-white mb-3">Как добавить первую группу</h2>
    <ol className="list-decimal list-inside space-y-2 text-gray-300 text-sm text-left">
      <li>Найдите бота в Telegram по username и отправьте ему <span className="font-mono bg-gray-700 px-1 rounded">/start</span>.</li>
      <li>Добавьте бота в группу через «Добавить участников».</li>
      <li>Скопируйте ID чата и создайте группу ниже.</li>
    </ol>
    <Button className="mt-4" onClick={() => setShowCreateModal(true)}>Создать первую группу</Button>
  </Card>
);

const Groups = () => {
  const navigate = useNavigate();
  const { currentGroup, setCurrentGroup } = useCurrentGroup();
  const { groups, loading, error } = useGroups();
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newGroupData, setNewGroupData] = useState({
    name: '',
    chatId: '',
    mode: 'family',
  });
  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState(null);

  const handleSelectGroup = (group) => {
    setCurrentGroup(group);
    navigate(`/group/${group.id}/dashboard`);
  };

  const handleCreateGroup = async () => {
    if (!newGroupData.name.trim()) {
      setCreateError('Введите название группы');
      return;
    }
    if (!newGroupData.chatId) {
      setCreateError('Введите ID чата');
      return;
    }

    try {
      setCreating(true);
      setCreateError(null);
      await apiClient.createGroup(newGroupData);
      setShowCreateModal(false);
      setNewGroupData({ name: '', chatId: '', mode: 'family' });
      window.location.reload();
    } catch (err) {
      setCreateError(`Ошибка: ${err.message}`);
    } finally {
      setCreating(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="max-w-mobile mx-auto p-4">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white mb-1">Ваши группы</h1>
        <p className="text-gray-400 text-sm">Управление расходами</p>
      </div>

      {error && <ErrorMessage message={error} />}

      {groups.length === 0 ? (
        <div className="space-y-4">
          <Card className="text-center py-6">
            <p className="text-gray-300 mb-3">Пока нет групп.</p>
            <Button onClick={() => setShowCreateModal(true)} fullWidth>
              Создать первую группу
            </Button>
          </Card>
          <EmptyGroupsGuide />
        </div>
      ) : (
        <div className="space-y-3">
          {groups.map(group => (
            <Card
              key={group.id}
              className="cursor-pointer active:bg-gray-700/50"
              onClick={() => handleSelectGroup(group)}
            >
              <div className="flex justify-between items-center">
                <div className="flex-1 min-w-0">
                  <h2 className="font-bold text-white truncate">{group.name}</h2>
                  <p className="text-gray-400 text-xs">
                    {group.members} участников • {group.mode === 'family' ? 'Семья' : 'Друзья'}
                  </p>
                </div>
                <div className="text-right">
                  <BalanceDisplay balance={group.balance} size="sm" />
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      <Button className="mt-4" onClick={() => setShowCreateModal(true)} fullWidth>
        + Новая группа
      </Button>

      <Modal
        isOpen={showCreateModal}
        title="Новая группа"
        onClose={() => setShowCreateModal(false)}
        actions={[
          { label: 'Отмена', variant: 'secondary', onClick: () => setShowCreateModal(false) },
          { label: creating ? 'Создание...' : 'Создать', variant: 'primary', onClick: handleCreateGroup, disabled: creating }
        ]}
      >
        {createError && <ErrorMessage message={createError} />}
        <div className="space-y-4">
          <div>
            <label className="block text-sm mb-1">Название</label>
            <Input
              placeholder="Например: Семья"
              value={newGroupData.name}
              onChange={e => setNewGroupData({...newGroupData, name: e.target.value})}
              disabled={creating}
            />
          </div>
          <div>
            <label className="block text-sm mb-1">ID чата</label>
            <Input
              type="number"
              placeholder="ID Telegram чата"
              value={newGroupData.chatId}
              onChange={e => setNewGroupData({...newGroupData, chatId: e.target.value})}
              disabled={creating}
            />
          </div>
          <div>
            <label className="block text-sm mb-1">Режим</label>
            <Select
              options={[
                { value: 'family', label: 'Семья (без долгов)' },
                { value: 'friends', label: 'Друзья (с долгами)' }
              ]}
              value={newGroupData.mode}
              onChange={e => setNewGroupData({...newGroupData, mode: e.target.value})}
              disabled={creating}
            />
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Groups;
