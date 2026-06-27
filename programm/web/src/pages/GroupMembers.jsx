import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useMembers } from '../hooks/useApi';
import { LoadingSpinner, ErrorMessage, Card, Button, Input, Modal, Badge } from '../components/Common';
import { apiClient } from '../utils/api';

const getMemberName = (member) => member.name || member.username || `Пользователь ${member.id}`;

const GroupMembers = () => {
  const { groupId } = useParams();
  const navigate = useNavigate();
  const { members, loading, error, setMembers } = useMembers(groupId);
  const [newMemberId, setNewMemberId] = useState('');
  const [adding, setAdding] = useState(false);
  const [removingId, setRemovingId] = useState(null);
  const [showRoleModal, setShowRoleModal] = useState(false);
  const [selectedMember, setSelectedMember] = useState(null);

  const handleAddMember = async () => {
    if (!newMemberId.trim()) return;
    try {
      setAdding(true);
      await apiClient.addMember(Number(groupId), Number(newMemberId.trim()));
      setNewMemberId('');
      const updated = await apiClient.getMembers(groupId);
      setMembers(updated);
    } catch (err) {
      alert('Ошибка: ' + err.message);
    } finally {
      setAdding(false);
    }
  };

  const handleRemoveMember = async (memberId) => {
    if (!window.confirm('Удалить участника из группы?')) return;
    try {
      setRemovingId(memberId);
      await apiClient.removeMember(groupId, memberId);
      const updated = await apiClient.getMembers(groupId);
      setMembers(updated);
    } catch (err) {
      alert('Ошибка: ' + err.message);
    } finally {
      setRemovingId(null);
    }
  };

  const handleRoleChange = async (memberId, newRole) => {
    try {
      await apiClient.updateMemberRole(groupId, memberId, newRole);
      const updated = await apiClient.getMembers(groupId);
      setMembers(updated);
      setShowRoleModal(false);
      setSelectedMember(null);
    } catch (err) {
      alert('Ошибка: ' + err.message);
    }
  };

  const handleBack = () => navigate(`/group/${groupId}/dashboard`);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="max-w-md mx-auto p-4">
      <Button variant="ghost" onClick={handleBack} className="mb-4">← Назад</Button>
      <h1 className="text-2xl font-bold mb-4">Участники</h1>

      <Card className="mb-4">
        <p className="text-gray-400 text-sm mb-2">Добавить участника</p>
        <div className="flex gap-2">
          <Input
            placeholder="Telegram ID"
            value={newMemberId}
            onChange={e => setNewMemberId(e.target.value)}
            disabled={adding}
          />
          <Button onClick={handleAddMember} disabled={adding}>
            {adding ? '...' : 'Добавить'}
          </Button>
        </div>
      </Card>

      <div className="space-y-2">
        {members && members.length > 0 ? (
          members.map(member => (
            <Card key={member.id} className="hover:bg-gray-700/50 transition-colors">
              <div className="flex justify-between items-center">
                <div className="flex-1 min-w-0">
                  <p className="font-semibold truncate">{getMemberName(member)}</p>
                  <div className="flex gap-2 mt-1">
                    <Badge variant={member.role === 'admin' ? 'danger' : member.role === 'moderator' ? 'warning' : 'default'}>
                      {member.role === 'admin' ? 'Админ' : member.role === 'moderator' ? 'Модератор' : 'Участник'}
                    </Badge>
                    <Badge>{member.telegram_id || member.user_id}</Badge>
                  </div>
                </div>
                <div className="flex gap-1">
                  <Button
                    variant="ghost"
                    onClick={() => {
                      setSelectedMember(member);
                      setShowRoleModal(true);
                    }}
                  >
                    ⚙️
                  </Button>
                  <Button
                    variant="danger"
                    onClick={() => handleRemoveMember(member.id)}
                    disabled={removingId === member.id}
                  >
                    {removingId === member.id ? '...' : '✕'}
                  </Button>
                </div>
              </div>
            </Card>
          ))
        ) : (
          <Card className="text-center text-gray-400">Нет участников</Card>
        )}
      </div>

      {/* Модальное окно изменения роли */}
      <Modal
        isOpen={showRoleModal}
        title="Изменить роль"
        onClose={() => {
          setShowRoleModal(false);
          setSelectedMember(null);
        }}
        actions={[
          { label: 'Отмена', variant: 'secondary', onClick: () => setShowRoleModal(false) }
        ]}
      >
        {selectedMember && (
          <div className="space-y-3">
            <p className="text-white font-semibold">{getMemberName(selectedMember)}</p>
            <div className="space-y-2">
              {['member', 'moderator', 'admin'].map(role => (
                <Button
                  key={role}
                  variant={selectedMember.role === role ? 'primary' : 'secondary'}
                  onClick={() => handleRoleChange(selectedMember.id, role)}
                  fullWidth
                >
                  {role === 'admin' ? 'Администратор' : role === 'moderator' ? 'Модератор' : 'Участник'}
                </Button>
              ))}
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default GroupMembers;