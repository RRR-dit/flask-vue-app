const { createApp } = Vue;

// Render のベースURL（デプロイ先に合わせて変える）
const API_BASE = 'https://flask-vue-app.onrender.com';

createApp({
  delimiters: ['[[', ']]'],
  data() {
    return {
      users: [],
      newUsername: '',
      editingId: null,
      editedName: '',
    };
  },
  methods: {
    // ユーザー一覧取得
    fetchUsers() {
      fetch(`${API_BASE}/api/users`)
        .then((res) => res.json())
        .then((data) => {
          this.users = data;
        });
    },
    // ユーザー追加
    addUser() {
      const username = this.newUsername.trim();
      if (!username) return;

      fetch(`${API_BASE}/api/add_user`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.user) {
            this.users.push(data.user);
            this.newUsername = '';
          }
        });
    },
    // ユーザー削除
    deleteUser(id) {
      if (!confirm('本当に削除しますか？')) return;

      fetch(`${API_BASE}/api/delete/${id}`, { method: 'DELETE' }).then(() => {
        this.users = this.users.filter((u) => u.id !== id);
      });
    },
    // 編集開始
    startEdit(user) {
      this.editingId = user.id;
      this.editedName = user.username;
    },
    // 編集キャンセル
    cancelEdit() {
      this.editingId = null;
      this.editedName = '';
    },
    // 名前を更新
    updateUser(id) {
      const newName = this.editedName.trim();
      if (!newName) return;

      fetch(`${API_BASE}/api/update/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: newName }),
      })
        .then((res) => res.json())
        .then((data) => {
          const updated = data.user;
          const target = this.users.find((u) => u.id === id);
          if (target) target.username = updated.username;
          this.cancelEdit();
        });
    },
  },
  mounted() {
    this.fetchUsers(); // ページ読み込み時に一覧取得
  },
}).mount('#app');
