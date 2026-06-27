import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { LoadingSpinner, ErrorMessage, Card, Button, Input, Modal } from '../components/Common';
import { apiClient } from '../utils/api';

const GroupSettings = () => {
  const { groupId } = useParams();
  const navigate = useNavigate();
  const [group, setGroup] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('general');
  const [editedName, setEditedName] = useState('');
  const [editedMode, setEditedMode] = useState('');
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const fetchGroup = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getGroupById(groupId);
        setGroup(data);
        setEditedName(data.name);
        setEditedMode(data.mode);
      } catch (err) {
        console.error('Ошибка загрузки группы:', err);
      } finally {
        setLoading(false);
      }
    };

    if (groupId) fetchGroup();
  }, [groupId]);

  const handleSaveGroup = async () => {
    try {
      setSaving(true);
      await apiClient.updateGroup(groupId, {
        name: editedName,
        mode: editedMode,
      });
      setGroup({ ...group, name: editedName, mode: editedMode });
      alert('Группа обновлена');
    } catch (err) {
      console.error('Ошибка сохранения:', err);
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteGroup = async () => {
    try {
      setSaving(true);
      await apiClient.deleteGroup(groupId);
      alert('Группа удалена');
      navigate('/');
    } catch (err) {
      console.error('Ошибка удаления:', err);
    } finally {
      setSaving(false);
      setShowDeleteModal(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!group) return <ErrorMessage message="Группа не найдена" />;

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Настройки группы</h1>

      {/* Вкладки */}
      <div className="flex gap-4 mb-6 border-b border-gray-700">
        {[
          { id: 'general', label: 'Общие' },
          { id: 'members', label: 'Участники' },
          { id: 'notifications', label: 'Уведомления' },
          { id: 'danger', label: 'Опасно' },
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 font-semibold border-b-2 transition-colors ${
              activeTab === tab.id
                ? 'border-blue-600 text-white'
                : 'border-transparent text-gray-400 hover:text-white'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Вкладка Общие */}
      {activeTab === 'general' && (
        <div className="space-y-6">
          <Card>
            <h2 className="text-xl font-bold mb-4">Основные сведения</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Название группы</label>
                <Input
                  value={editedName}
                  onChange={e => setEditedName(e.target.value)}
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Режим</label>
                <select
                  value={editedMode}
                  onChange={e => setEditedMode(e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 text-white rounded-lg border border-gray-600"
                >
                  <option value="family">👨‍👩‍👧 Семейный режим (без долгов)</option>
                  <option value="friends">👥 Режим друзей (с долгами)</option>
                </select>
              </div>

              <div className="pt-4 border-t border-gray-700">
                <Button onClick={handleSaveGroup} disabled={saving}>
                  {saving ? 'Сохранение...' : 'Сохранить изменения'}
                </Button>
              </div>
            </div>
          </Card>

          <Card>
            <h2 className="text-xl font-bold mb-4">Информация</h2>
            <div className="space-y-2 text-sm text-gray-400">
              <p>ID группы: <span className="font-mono text-white">{group.id}</span></p>
              <p>Создана: {new Date(group.created_at).toLocaleDateString('ru-RU')}</p>
              <p>Участников: {group.members_count || '—'}</p>
              <p>Режим: {group.mode === 'family' ? 'Семейный' : 'Друзья'}</p>
            </div>
          </Card>
        </div>
      )}

      {/* Вкладка Участники */}
      {activeTab === 'members' && (
        <Card>
          <h2 className="text-xl font-bold mb-4">Участники</h2>
          <p className="text-gray-400">
            Всего участников: {group.members_count || '—'}
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Управление членами доступно в Telegram боте
          </p>
        </Card>
      )}

      {/* Вкладка Уведомления */}
      {activeTab === 'notifications' && (
        <Card>
          <h2 className="text-xl font-bold mb-4">Уведомления</h2>
          <div className="space-y-4">
            <label className="flex items-center gap-3">
              <input type="checkbox" defaultChecked className="w-4 h-4" />
              <span>Новые расходы</span>
            </label>
            <label className="flex items-center gap-3">
              <input type="checkbox" defaultChecked className="w-4 h-4" />
              <span>Запросы на подтверждение</span>
            </label>
            <label className="flex items-center gap-3">
              <input type="checkbox" defaultChecked className="w-4 h-4" />
              <span>Нарушения порогов товаров</span>
            </label>
            <label className="flex items-center gap-3">
              <input type="checkbox" defaultChecked className="w-4 h-4" />
              <span>Сводка по долгам</span>
            </label>
          </div>
        </Card>
      )}

      {/* Вкладка Опасные операции */}
      {activeTab === 'danger' && (
        <div className="space-y-6">
          <Card className="border-l-4 border-red-600">
            <h2 className="text-xl font-bold mb-4 text-red-500">⚠️ Опасные операции</h2>
            <p className="text-gray-400 mb-6">
              Эти действия необратимы. Будьте осторожны!
            </p>

            <Button
              variant="danger"
              onClick={() => setShowDeleteModal(true)}
            >
              🗑️ Удалить группу
            </Button>

            <p className="text-xs text-gray-500 mt-4">
              При удалении всех данные группы будут окончательно стёрты из базы:
              холодильники, расходы, долги и история.
            </p>
          </Card>
        </div>
      )}

      {/* Модальное окно подтверждения удаления */}
      <Modal
        isOpen={showDeleteModal}
        title="Удалить группу?"
        onClose={() => setShowDeleteModal(false)}
        actions={[
          {
            label: 'Отмена',
            variant: 'secondary',
            onClick: () => setShowDeleteModal(false),
          },
          {
            label: 'Удалить',
            variant: 'danger',
            onClick: handleDeleteGroup,
          },
        ]}
      >
        <div className="space-y-4">
          <p className="text-white">
            Вы уверены? Эта операция <span className="font-bold">необратима</span>.
          </p>
          <div className="bg-red-900 border border-red-700 p-3 rounded text-sm text-red-200">
            <p>Будут удалены:</p>
            <ul className="list-disc list-inside mt-2 space-y-1">
              <li>Все холодильники и остатки</li>
              <li>Все расходы и чеки</li>
              <li>Все долги и история платежей</li>
              <li>Список покупок</li>
            </ul>
          </div>
          <Input
            type="text"
            placeholder={`Введите "${group.name}" для подтверждения`}
            onChange={e => {
              // Можно добавить валидацию
            }}
          />
        </div>
      </Modal>
    </div>
  );
};

export default GroupSettings;

