const USER_CACHE_KEY = 'splitchek.current_user';
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

console.log('🔧 API Base URL:', API_BASE_URL);

function getTelegramId() {
  // 1. Из Telegram WebApp
  const tgWebAppId = window?.Telegram?.WebApp?.initDataUnsafe?.user?.id;
  if (tgWebAppId) return Number(tgWebAppId);

  // 2. Из URL параметров
  const params = new URLSearchParams(window.location.search);
  const fromQuery = params.get('telegram_id') || params.get('tg_id');
  if (fromQuery) {
    const id = Number(fromQuery);
    if (!Number.isNaN(id)) {
      localStorage.setItem('splitchek.telegram_id', String(id));
      return id;
    }
  }

  // 3. Из localStorage
  const fromStorage = localStorage.getItem('splitchek.telegram_id');
  if (fromStorage) {
    const id = Number(fromStorage);
    if (!Number.isNaN(id)) return id;
  }

  // 4. Из env (только для разработки)
  const fromEnv = import.meta.env.VITE_TELEGRAM_ID;
  console.log('VITE_TELEGRAM_ID:', fromEnv);
  if (fromEnv && !Number.isNaN(Number(fromEnv)) && Number(fromEnv) > 0) return Number(fromEnv);

  return null;
}

function normalizeGroup(group) {
  return { ...group, chatId: group.chat_id, members: group.members ?? group.members_count ?? 0, balance: group.balance ?? 0 };
}

function normalizeShoppingItem(item) {
  return { ...item, name: item.product_name, storage_id: item.storage_location_id, unit: item.unit || 'pcs', storage_name: item.storage_name || null };
}

class APIClient {
  constructor(baseUrl = API_BASE_URL) {
    this.baseUrl = baseUrl;
    this.currentUserPromise = null;
  }

  async request(path, options = {}) {
    const url = `${this.baseUrl}${path}`;
    const method = (options.method || 'GET').toUpperCase();
    const hasBody = options.body !== undefined && options.body !== null;
    const headers = { Accept: 'application/json', ...options.headers };
    if (hasBody && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json';
    }
    const response = await fetch(url, { method, headers, body: options.body });
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    if (response.status === 204) return null;
    const text = await response.text();
    if (!text) return null;
    try { return JSON.parse(text); } catch { return text; }
  }

  async ensureCurrentUser() {
    if (this.currentUserPromise) return this.currentUserPromise;
    this.currentUserPromise = (async () => {
      const telegramId = getTelegramId();
      if (!telegramId) throw new Error('Не найден telegram_id');
      try {
        const user = await this.request(`/api/me?telegram_id=${telegramId}`);
        localStorage.setItem(USER_CACHE_KEY, JSON.stringify(user));
        return user;
      } catch (err) {
        const fallbackName = window?.Telegram?.WebApp?.initDataUnsafe?.user?.first_name || 'Web User';
        const fallbackUsername = window?.Telegram?.WebApp?.initDataUnsafe?.user?.username || null;
        const created = await this.request('/api/users', { method: 'POST', body: JSON.stringify({ telegram_id: telegramId, name: fallbackName, username: fallbackUsername }) });
        localStorage.setItem(USER_CACHE_KEY, JSON.stringify(created));
        return created;
      }
    })();
    try { return await this.currentUserPromise; } finally { this.currentUserPromise = null; }
  }

  async getCurrentUser() { return this.request('/api/me'); }

  async getGroups() {
    const user = await this.ensureCurrentUser();
    const groups = await this.request(`/api/groups?user_id=${user.id}`);
    return Array.isArray(groups) ? groups.map(normalizeGroup) : [];
  }

  async createGroup(data) {
    const user = await this.ensureCurrentUser().catch(err => {
      console.error('Failed to get user:', err);
      return null;
    });
    if (!user?.id) throw new Error('Пользователь не авторизован');
    return this.request(`/api/groups?owner_user_id=${user.id}`, { method: 'POST', body: JSON.stringify({ chat_id: Number(data.chat_id ?? data.chatId), name: data.name, mode: data.mode }) });
  }

  async getMembers(groupId) { return this.request(`/api/groups/${groupId}/members`); }
  async addMember(groupId, userId, role = 'member') { return this.request(`/api/groups/${groupId}/members`, { method: 'POST', body: JSON.stringify({ user_id: userId, role }) }); }
  async removeMember(groupId, userId) { return this.request(`/api/groups/${groupId}/members/${userId}`, { method: 'DELETE' }); }
  async updateMemberRole(groupId, userId, role) { return this.request(`/api/groups/${groupId}/members/${userId}`, { method: 'PATCH', body: JSON.stringify({ role }) }); }

  async getStorage(groupId) {
    const storage = await this.request(`/api/groups/${groupId}/storage`);
    return Array.isArray(storage) ? storage : [];
  }

  async getInventory(storageId) {
    const inventory = await this.request(`/api/storage/${storageId}/inventory`);
    return Array.isArray(inventory) ? inventory : [];
  }

  async addInventory(data) {
    return this.request('/api/inventory/add', {
      method: 'POST',
      body: JSON.stringify({
        storage_location_id: Number(data.storage_id),
        product_name: data.product_name,
        quantity: Number(data.quantity),
        unit: data.unit
      })
    });
  }

  async getShoppingList(groupId) {
    const items = await this.request(`/api/groups/${groupId}/shopping-list`);
    return Array.isArray(items) ? items.map(normalizeShoppingItem) : [];
  }

  async addToShoppingList(groupId, product_name, quantity = 1, unit = 'pcs') {
    return this.request('/api/shopping-list', {
      method: 'POST',
      body: JSON.stringify({ group_id: Number(groupId), product_name, quantity, unit })
    });
  }

  async getExpenses(groupId) {
    const expenses = await this.request(`/api/groups/${groupId}/expenses`);
    return Array.isArray(expenses) ? expenses : [];
  }

  async distributeExpense(expenseId, assignments) {
    return this.request(`/api/expenses/${expenseId}/distribute`, {
      method: 'POST',
      body: JSON.stringify({ assignments })
    });
  }

  async createManualExpense(data) {
    const user = await this.ensureCurrentUser();
    return this.request('/api/expenses/manual', { method: 'POST', body: JSON.stringify({ group_id: Number(data.group_id), uploaded_by_user_id: Number(data.uploaded_by_user_id ?? user.id), title: data.title ?? data.name, total_amount: Number(data.total_amount ?? data.amount), category: data.category, purchase_date: data.purchase_date ?? data.date ?? null, participant_ids: Array.isArray(data.participant_ids) ? data.participant_ids : [], is_grocery: Boolean(data.is_grocery), storage_location_id: data.storage_location_id ?? data.storage_id ?? null, items: Array.isArray(data.items) ? data.items : [], comment: data.comment ?? null }) });
  }

  async getDebts(groupId) {
    const debts = await this.request(`/api/groups/${groupId}/debts`);
    return Array.isArray(debts) ? debts : [];
  }

  async getBalance(groupId) {
    const user = await this.ensureCurrentUser();
    return this.request(`/api/groups/${groupId}/balance?user_id=${user.id}`);
  }

  async settleDebt(debtId, data = {}) {
    return this.request(`/api/debts/${debtId}/settle`, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }
}

export const apiClient = new APIClient();
export const api = apiClient;
export default apiClient;
