import { useState, useEffect, useContext, createContext } from 'react';
import { apiClient } from '../utils/api';

// Контекст для хранения текущей выбранной группы
export const GroupContext = createContext(null);

export const useCurrentGroup = () => {
  const context = useContext(GroupContext);
  if (!context) {
    throw new Error('useCurrentGroup must be used within GroupProvider');
  }
  return context;
};

// Хук для загрузки групп
export const useGroups = () => {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchGroups = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getGroups();
        setGroups(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchGroups();
  }, []);

  return { groups, loading, error };
};

// Хук для загрузки холодильников группы
export const useStorage = (groupId) => {
  const [storage, setStorage] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!groupId) return;

    const fetchStorage = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getStorage(groupId);
        setStorage(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStorage();
  }, [groupId]);

  return { storage, loading, error, setStorage };
};

// Хук для загрузки инвентаря конкретного холодильника
export const useInventory = (storageId) => {
  const [inventory, setInventory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!storageId) return;

    const fetchInventory = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getInventory(storageId);
        setInventory(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchInventory();
  }, [storageId]);

  return { inventory, loading, error, setInventory };
};

// Хук для загрузки списка покупок
export const useShoppingList = (groupId) => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!groupId) return;

    const fetchShoppingList = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getShoppingList(groupId);
        setItems(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchShoppingList();
  }, [groupId]);

  return { items, loading, error, setItems };
};

// Хук для загрузки расходов
export const useExpenses = (groupId) => {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!groupId) return;

    const fetchExpenses = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getExpenses(groupId);
        setExpenses(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchExpenses();
  }, [groupId]);

  return { expenses, loading, error, setExpenses };
};

// Хук для загрузки долгов
export const useDebts = (groupId) => {
  const [debts, setDebts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!groupId) return;

    const fetchDebts = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getDebts(groupId);
        setDebts(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDebts();
  }, [groupId]);

  return { debts, loading, error, setDebts };
};

// Хок для загрузки баланса пользователя в группе
export const useBalance = (groupId) => {
  const [balance, setBalance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!groupId) return;

    const fetchBalance = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getBalance(groupId);
        setBalance(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchBalance();
  }, [groupId]);

  return { balance, loading, error };
};

// Хук для загрузки членов группы
export const useMembers = (groupId) => {
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!groupId) return;

    const fetchMembers = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getMembers(groupId);
        setMembers(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchMembers();
  }, [groupId]);

  return { members, loading, error, setMembers };
};

